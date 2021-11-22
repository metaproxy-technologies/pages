

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



　 