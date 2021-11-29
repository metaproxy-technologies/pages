---
title: "Webpageをgithub pagesでつくる"
date: 2021-11-28
classes: wide
---

動的に記事が追加編集可能で、でも出力は静的なwordpress代替をgithub pagesで試してみた。

## 背景

動的なCMSは便利。でも、update時に本番が死ぬんじゃないかとの不安がつきまとう。実際お問合せフォームが死んだりレイアウトが崩れたり。いずれも細かい話ですぐ直るけれども本番だとご法度。ユーザ自身が更新できるのはいいんだけれども。wordpress,sharepointいずれもいつもこの恐怖との戦いになる。

では、静的CMSはどうか。前述の不安はないけれども、カスタマイズの結果は記事を更新するユーザのデスクトップにあるし、ビルド環境を構築したデスクトップが結局準本番サーバのような扱いが必要になってきてしまう。標準で使えるテーマがあまりない気もする。

## github pagesがある

github pagesはこんな特徴がある
- github上にwebsiteを作ることができる
    - repository上にマークダウンを配置してcommitすると自動でビルドしてくれ、変更反映
    - 戻しもマークダウンを戻すだけ
    - 自動ビルドに失敗してもページが壊れない。エラー修正してからcommitすればよい
- 独自ドメインを割り当てることができる
- テーマ多数。カスタマイズ可能
    - テーマをforkしてからカスタマイズすれば自由自在に変更可能

よさそうな感じではないだろうか。
私は移行した。このブログはgithub pagesのリポジトリへcommitしたmarkdownで出来ており、テーマはminimal mistakeというテーマをforkしてカスタマイズしたものを使っている。

- ブログのレポジトリ <https://github.com/metaproxy-technologies/pages>
- ブログが利用しているテーマ(forkしてカスタマイズしたもの)<https://github.com/metaproxy-technologies/minimal-mistakes>


## 作り方(概略)

概略は以下の通り
- github pagesのチュートリアルを行う
- repositoryを作り試しに公開してみる
- テーマを設定する
    - github pages組込のテーマ使う
    - 独自テーマを使う/カスタマイズする
- 独自ドメインを割り当てる
- repositoryを非公開にする

## 作り方(詳細)

詳しくはこちらの公式を読み進めてゆくと作ることができる。
<https://docs.github.com/ja/pages/getting-started-with-github-pages/about-github-pages>

## 補足

テーマのカスタマイズ方法が分からなかった。大体ローカルに持ってきてビルド環境を作るべし、というアドバイスが多かったからだ。ただ、github pagesの利点はローカルにビルド環境を作らないことが利点だと思うので、そうならないようにこのようにした

- 使いたいテーマをforkし、変更を加えたい箇所を変更する
![fork!](../assets/2021-11-28-fork.jpeg)

- _config.ymlで指定する

```yaml
remote_theme: metaproxy-technologies/minimal-mistakes
plugins:
  - 他のプラグイン
  - jekyll-remote-theme
```

- ブログ側のrepositoryを更新して反映する




