---
title: "serverbuild cheat sheet"
date: 2017-01-01
---

Raspberry Pi利用開始時に実施することあれこれをとりまとめてゆきます

## Setup

RaspberryPi OSをMicroSDへbananaEtcherで焼き、ネット接続などの基本設定をしていきます。

ディスプレイ＆マウス＆キーボード＆有線LANでセットアップすることがおすすめです。

勿論、ディスプレイ無し & 無線LAN & SSH接続でセットアップも可能ですが、知識を背景にしたTry&Errorが必要なので初回は用意することをお勧めします。


## 外付けSSD/HDDで運用する

小型サーバ的な利用を検討されている方は、bananaEthcerで焼いたSSDの内容をSSD/HDDへコピーして、それを/へマウントするのがおすすめです。

この方のガイドがわかりやすいと思います。
<https://www.pragmaticlinux.com/2020/08/move-the-raspberry-pi-root-file-system-to-a-usb-drive/>


### その他通常のサーバと共通な設定

こちらをご覧ください。
<https://metaproxy.co/serverbuild/>
