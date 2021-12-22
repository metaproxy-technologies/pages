---
title: "各種サーバ内の通知をSlackへ通知する"
date: 2021-12-09
classes: wide
---

サーバ内のイベントをSlackへ通知するための簡易メモです。

## はじめに：どういうイベントが対象になるか

発生ー＞即インシデント　のような異常系のイベントについては、これは当然行動に移して対応する必要がありますから、メールや人間によるコールなど、処理しないといつまでも残り続けるものである必要があると思います。

一方、例えば週一回程度や月一回程度、正常に進んでいることを確認すればよいようなものもあろうかと思います。

このあたりいつも監視設計をすると結局メールBOXに流し込んだうえで何となく日々眺めるか、もしくは行動がないのだから受信すらしないという形に落ち着いていると思いますが、Slackに流し込んでみて監視がどのようになるのか試験してみたいと思います。

## 仕組み

サーバ内の通知を一度メールとして集め、集めたメールをSlack AppのWebhook URLでSlackAppに引き渡し、最後にSlack AppがChannelに書き込みます。
![Label](../assets/2021-12-09-notifytoslack.drawio.svg)

## 仕掛け方

### MTA(postfix)を導入します

<https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postfix-as-a-send-only-smtp-server-on-ubuntu-20-04>

### 各種サービスの通知をメールでどこかに集めます

いったん<root@localhost>などに集約してしまってよいと思います。通知といえばメールの時代が長らく続きましたから、たいていのサービスはメールで通知することができます（ただでさえrootには何かとお知らせが集まってくるので）

### Slack App & WebHook受付用のURLを作ります

"Incoming Webhook"と呼ばれているそうです。こちらのガイドに従ってSlackのAppをつくると、そのURLを発行することができます。
<https://api.slack.com/messaging/webhooks>

いろいろと記載がありますが、"Create your Slack app"ボタンをいきなり押してから、各ページにあるガイドに従ってゆくと特に苦労なく作ることができます。

![Label](../assets/2021-12-09-slackapp00.drawio.svg)

![Label](../assets/2021-12-09-slackapp01.drawio.svg)

![Label](../assets/2021-12-09-slackapp03.drawio.svg)

![Label](../assets/2021-12-09-slackapp05.drawio.svg)

![Label](../assets/2021-12-09-slackapp07.drawio.svg)

### メール転送用のシェルスクリプトをつくります

たとえばuserAのhomeに、パイプで受け取った入力をSlackのWebhookへ叩き込むようなスクリプトを作成します

```shell
vi /home/userA/notify.sh
```

```shell
#!/bin/bash

#URLはこのようなものです
#  "https://hooks.slack.com/services/XX12345789/XXX12345678/abcd1253745489124"
URL="先ほど作成したWEBHOOKのURL"  
LF=$'\n'

concat=""
while read line
do
  concat=$concat$(echo $line | sed 's|["'\''`|><;:/=@\*?{}-~#]| |g')$LF
done

curl -X POST \
  -H 'Content-type: application/json' \
  -d '{"text":"'"$concat"'"}' \
  $URL
```

### メールを先ほど作ったScriptへ転送します

/etc/aliasesを編集します。

```shell
sudo vi /etc/aliases
```

このように、各種通知をrootへ集めたのちに、先ほど作成した「/home/userA/notify.sh」へパイプで渡します

```shell
#/etc/aliasesの中身
# /etc/aliases
postmaster: root
root: "| /home/userA/notify.sh"
```

編集後にaliasesのDBを作り直します

```shell
sudo newaliases
```

### メールを作ってテストします

mailコマンドでrootへメールを投入します

```shell
 echo "This is the body of the email" | mail -s "This is the subject line" root@localhost
```

いけましたね

<img src="../assets/2021-12-09-result.png" width="55%" />

## 本番適用時の注意点

スクリプト側で何のサニタイズもしていないので、恐らくメールを着信させるなどの方法で任意のリモートコードを実行する脆弱性が含まれているはずです。　本格的に利用する場合はnotify.shの中身をきちんとしたプログラミング言語で置き換えた後にサニタイズを行い、curlではなく当該言語のやり方でjsonをpostするようにいたしましょう。何事にも完璧はないと思いますが最低限その対策は必要なはずです。
