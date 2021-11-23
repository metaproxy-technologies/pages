---
title: "Raspberry PiでArduino開発(Arduino IDE編)"
date: 2018-12-04 22:46:05
---

Raspberry Pi Zero W + Arduino で作ってみたいものがある。
ただ、わざわざSketchをPCから転送するのも面倒かつデバッグしにくい。。。。ので、Raspberry PiでArduino IDEを使えるようにしてみた。

<img src="../assets/2018-12-04-ok.png" style="width:500px;margin-left:1em;">

## 目指す構成
Raspberry Pi/Arduino共に、コードを試行錯誤しやすい構成を目指す。Arduino IDEをRaspberry Pi上で動作させれば、macからリモートでRaspberry Pi/Arduinoいずれも開発ができて良さそうである。

        mac(OSX) 
            |
          [XWindow] on WIFI 
            |
        Raspberry Pi Zero W
            |
          [USB] on /dev/ttyACM0 
            |
        Arduino Leonard

## ① Raspberry Piのセットアップ
ディスプレイやキーボード無しでもやれるやり方のメモ
- [Raspbian (with Desktop)](https://www.raspberrypi.org/downloads/raspbian/)を入手
    - Liteではなく、Desktopがあるものを選ぶこと
- [Etcher](https://www.balena.io/etcher/)でMicro SDにRaspbianを焼く
    - [Micro SDはこれを使った](https://www.amazon.co.jp/gp/product/B01FTF7EH2)
    - Micro SDは[こういうメモリカードリーダー](https://www.amazon.co.jp/dp/B009D79VH4/ref=psdc_2151953051_t1_B006WEP0E4)に差してからUSBにつなぐ
- 事前にMicro SD内に、ssh有効化と、WIFIの接続情報を書いておく
    - ディスプレイやキーボードなしでセットアップするために
    - 焼いた後挿し直してから以下を実行
```shell
cd /Volumes/boot
touch ssh
vi wpa_supplicant.conf
#vi内で以下を投入して保存
country=JP
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="WIFIのSSID"
    scan_ssid=1
    psk="WIFIのパスワード"
}
```
- Micro SDをRaspberry Piに差して起動させる
- Raspberry PiのIPを探す
    - 暫くしたらWIFIにRaspberry Piが繋がっているはず。なので、こんな方法でIPを特定する
        - 方法①：自宅ルーターの接続情報などを見る。見慣れないIPがRaspberry Piのもの
        - 方法②：arp -a で見慣れないIPがおそらくRaspberry Piのもの
        - 方法③：一応仕組み上はmacから「ping raspberrypi.local」が通るはず。。。
    - sshで接続
```shell
ssh pi@raspberrypi.local
```
- 初期セットアップ諸々
    - sudo raspi-config と入力して以下設定を行う
        - change password
        - change hostname
        - change timezone
        - change locale
            - en_GB.UTF-8 を選び直しておいた（ja_JPにするとコンソールが日本語化されてエラーを踏みやすそうなので。。。）
        - enable Camera
        - expand filesystem
{% comment %}
    - [WIFI接続が切れる問題対策]({% post_url 2019-02-27-raspberry-pi-network-issue %})
{% endcomment %}
    - 再起動(sudo shutdown -r now)
    - sshの設定
        - keygenしてauthorized_keys作成
        - そのほか設定
            - port番号変更／rootログイン禁止/パスワードログイン禁止
        - 設定が終わったらsshd再起動(sudo /etc/init.d/ssh restart)
    - ipv6の無効化
        - すみません。。。
        - https://www.leowkahman.com/2016/03/19/disable-ipv6-raspberry-raspbian/
    - アップデート
        - sudo apt-get update
        - sudo apt-get upgrade
        - 再起動(sudo shutdown -r now)
    - 必要最低限の追加パッケージ
        - sudo apt-get install vim

## ② XWindowの導入

- mac側
    - XQuartsを導入
        - [Mac に X11 (XQuartz) をインストール](https://macperson.net/mac-x11-xquartz/)
    - sshのクライアント側の設定
```shell
vi ~/.ssh/config
#vi内で以下を投入して保存
XAuthLocation /opt/X11/bin/xauth
ForwardX11 yes
ForwardX11Trusted yes
```
        - これをやらないと「No xauth data; using fake authentication data for X11 forwarding」と表示されうまく画面転送できない。ここに解決策があった：[Problem with "Warning: No xauth data; using fake authentication data for X11 forwarding."](https://www.linuxquestions.org/questions/linux-virtualization-and-cloud-90/problem-with-warning-no-xauth-data%3B-using-fake-authentication-data-for-x11-forwarding-4175614680/)
- Raspbery Pi側
    - Localeの設定をきちんとやっておく（何かとwarningが出るので）。常々解決したいと思っていたので、こちらの記事がありがたかった：[debian でロケールのエラーが出るときの対処法](https://qiita.com/d6rkaiz/items/c32f2b4772e25b1ba3ba)
```shell
export LANG=en_GB.UTF-8
export LC_ALL=$LANG
sudo locale-gen --purge $LANG
sudo dpkg-reconfigure -f noninteractive locales && sudo /usr/sbin/update-locale LANG=$LANG LC_ALL=$LANG
```
    - sshdの設定をやる
```shell
sudo vi /etc/ssh/sshd_config
#vi内で以下を投入して保存
X11Forwarding yes
X11UseLocalhost no
```
        - やらないとこれが出る：X11 forwarding request failed on channel 0。こちらに対応方法があった：[X11 forwarding request failed on channel 0 Error and Solution][https://www.cyberciti.biz/faq/how-to-fix-x11-forwarding-request-failed-on-channel-0/]
    - sshdを再起動（sudo /etc/init.d/ssh restart）
- つないでみる
    - このコマンドを入れた後、XQuartsが起動してデスクトップが表示されたらOK。以下macのターミナルで実行
```shell
ssh -X pi@remote_Raspberry_Pi_hostname
lxsession
```
    - 確認できたらctrl-cでデスクトップはけしておく。

## ③ Arduino IDEの導入
apt-getで入るVerは古いので、本家からARM用のバイナリを、Download & Uploadする。
<https://www.arduino.cc/download_handler.php?f=/arduino-1.8.7-r1-linuxarm.tar.xz>
- 展開して起動する。Raspberry Piのターミナルで実行
```
tar xf ./arduino-1.8.7-r1-linuxarm.tar.xz
cd arduino-1.8.7/
./arduino
```
- うまくいった！(XQuartsが起動し、その中で Arduino IDEの窓が立ち上がる)
    - <img src="../assets/2018-12-04-ok.png" style="width:600px;margin-left:1em;">
- 速度は（信じられないくらい）遅いが、外部Libraryも導入可能
    - <img src="../assets/2018-12-04-lib.png" style="width:600px;margin-left:1em;">
- 勿論問題なくArduinoへSketchを投入可能。DCモーターを動かして見た

## 感想
正直XWindow周りは仕組みを理解せずにやっているのでゴリ押し感が否めない。。。がひとまずはやりたいことができた。これでRaspberry Piに突っ込むコードはscpでUPしつつArduino側はIDEで突っ込めるはずである。WIFI経由で。

    
