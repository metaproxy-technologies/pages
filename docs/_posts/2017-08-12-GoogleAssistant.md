---
title: "Raspberry Pi へGoogleAssistant導入"
date: 2017-08-12 01:53:45
---

Raspberry Piへ人工知能の相棒（Google Assistant）を導入した。こいつにいろいろ付けて街へ出よう一緒に。
<https://www.youtube.com/watch?v=V-1AkxU_EPo>

## 1) 物品の準備
- Raspi関連
    - [Raspberry Pi3 Model B](http://amzn.to/2wPTEbc)
    - [Raspi の電源アダプタ](http://amzn.to/2wBwkyz)
    - [マイクロSDカード(SDカードにするアダプタ付き)](http://amzn.to/2vuox5O)
    - [SDカードリーダ](http://amzn.to/2vMjdx2)
    - [USBスピーカ](https://www.amazon.co.jp/dp/B00ID0EDRU?tag=arakiejiscom-22)
        手のひらに収まるくらい小さいUSBスピーカー。Bluetooth接続できるし軽いので、持ち運びしやすい。

- LED Matrix関連
    - [Pimoroni Unicorn HAT HD](https://www.switch-science.com/catalog/3336/)
    このPimoroniのMatrixは、HATというRaspiにすぐに差せる規格物なので楽。大抵ピンヘッダは自分で半田付けしなければならないんだけれど、これはその必要もなくてなおのこと楽（AdafruitのLED Matrixは綺麗で大きく、ひょっとしたらどこかに組んだやつ売れちゃうんじゃないかという位プロ用の雰囲気がするけどRaspiへの接続が若干面倒。。。）なお、これはAmazonでも売ってるけどスイッチサイエンスの３倍くらいの値がついているので、絶対に買ってはダメだと思う。

## 2) Raspberry Piのセットアップ
- 割愛。メモだけ記載する
    - OS導入
        - raspbianダウンロード
        - MicroSDをカードリーダでマウントしてから、etcher というアプリで焼く＠OSX
        - ディスプレイ・マウスなしで導入するためにWifi/SSH有効化
        - OSを焼いた後一度カードリーダを抜いて、もう一度挿してからマウント
            - SSH: bootフォルダ直下にsshという空ファイルを作成
            - Wifi: bootフォルダ直下にwpa_supplicant.confというファイルを作成
```shell
network={
       ssid="WIFIのSSID"
       psk="WIFIのパスワード"
       key_mgmt=WPA-PSK
    }
network={
       ssid="iPhoneのテザリングなど、外用WIFIのSSID"
       psk="WIFIのパスワード"
       key_mgmt=WPA-PSK
    }
```
    - SSHでアクセスする
        - SDカードを挿してRaspiを起動
            - ping raspberrypi.localが通るようになるのを待つ
            - ローカルのターミナルでssh pi@raspberrypi.local
            - パスワードは　raspberry
        - いつもの色々な設定
```shell
        apt-get install vim
        apt-get install git
        sudo raspi-config
```
でホスト名変更、パスワード変更、ディスクサイズを合わせる、タイムゾーン設定、カメラ有効化、WIFIの国をJPにsshdのポートなどセキュア化の設定外出時はテザリングのwifiで自動的に繋いでくれるようにする<https://www.thepolyglotdeveloper.com/2016/08/connect-multiple-wireless-networks-raspberry-pi/>
        - wifiが切れないようにするためのいろいろな手立て。ただし未だに不安定。。。

## 3) Google Assistantのセットアップ
　これはGoogle先生のサイトで間違いない。わかりにくいRasiでの音出し・マイク設定もさらりとまとめてあって言うことなし。ただ、OS導入部分はわかりにくいので途中のここから始めるのがいい
　　<https://developers.google.com/assistant/sdk/develop/python/hardware/audio>

## 4) 周辺機器のセットアップ
- 4-1) Pimoroni Unicorn HAT HD
    - ここに書いてある通りにやる
    <https://github.com/pimoroni/unicorn-hat-hd>
    - ただし、それだけだとGoogle Assistant のVirtual（＝パッケージを自分専用に仕立てた環境）から使えないので、こうやる。多分本来のPythonのVirtual環境のやりかたと違っているような気もするが、Symbolic Linkではなくきちんとモジュールをコピーしているので、意図はちゃんと忖度しているだろう。。。
```shell
cp -rp /usr/lib/python3/dist-packages/unicornhathd /home/pi/env/lib/python3.4/site-packages/
cp -rp /usr/lib/python3/dist-packages/spidev.cpython-34m-arm-linux-gnueabihf.so /home/pi/env/lib/python3.4/site-packages/
cp -rp /usr/lib/python3/dist-packages/numpy /home/pi/env/lib/python3.4/site-packages/
cp -rp /usr/lib/python3/dist-packages/PIL /home/pi/env/lib/python3.4/site-packages/
cp -rp /usr/lib/python3/dist-packages/picamera /home/pi/env/lib/python3.4/site-packages/
```
- 4-2) Bluetooth Speaker
    - ここに書いてある通りにやる
    <http://qiita.com/nattof/items/3db73a95e63100d7580a>
    - ただし、それだけだと最後にpulseaudioが起動できぬと文句を言われるので、以下を実行
```shell
sudo gpasswd -a pi pulse-access
```

## 5) Raspiカメラの追加

- 仕掛中

## 6) いろいろ繋ぎあわせる

- 仕掛中。ただ、画面表示用にまずは自分直下のsourcesフォルダに突っ込まれた画像またはテキストを（偽）リアルタイム表示するufeederというものを作った

** ufeed.py **
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#This software is released in MIT License.
#MIT License
#
#Copyright (c) 2017 Tomohiko Araki for this delivertive work.
#Copyright (c) 2017 Pimoroni Ltd.  for original work.
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import random
import time
import sys
import os
import glob
from subprocess import call,check_output
import colorsys
import signal
import time
from sys import exit
from PIL import Image, ImageDraw, ImageFont
import unicornhathd

class InputSourceDir:
    def __init__(self, path):
        if len(path)==0:
            self.srcdir = os.path.abspath(os.path.dirname(__file__)) + "/source"
        else:
            self.srcdir = path
        if not(os.path.isdir(self.srcdir)):
            print("Error: no source dir.")
            sys.exit(0)
        self.removeOldSrc()
        
    def getLatestFile(self):
        files = glob.glob(self.srcdir + "/*")
        if len(files)==0:
            return ""
        else:
            return max(files, key=os.path.getctime)

    def getInput(self):
        self.current = self.getLatestFile()
        self.currenttime = os.stat(self.current).st_mtime

        if len(self.current) == 0:
            self.currentType = ""
        else:
            if (self.current[-4:] == '.ppm') or (self.current[-4:] == '.png') or (self.current[-4:] == '.bmp') or (self.current[-4:] == '.jpg'):
                self.currentType = "image"
            elif self.current[-4:] == '.txt':
                self.currentType = "text"
            else:
                printf("Error: Please do not include non-ppm|jpg|png|bmp or non-txt files.")
                sys.exit(0)

    def checkCurrentIsLatest(self):
        if self.current == self.getLatestFile():
            if self.currenttime == os.stat(self.current).st_mtime:
                return True
            else:
                return False
        else:
            return False

    def removeOldSrc(self):
        #remove files more than 1 days before.
        if not(self.srcdir=="") and not(self.srcdir=="/")and not(self.srcdir=="."): 
            now = time.time()
            for f in os.listdir(self.srcdir):
                if (f[-4:] == '.ppm') or (f[-4:] == '.png') or (f[-4:] == '.bmp') or (f[-4:] == '.jpg'):
                    f = os.path.join(self.srcdir, f)
                    if os.stat(f).st_mtime < now - 0.5 * 86400:
                        if os.path.isfile(f):
                            os.remove(f)

def showImageFromFile(srcdir, unicornhathd):
    unicornhathd.rotation(0)
    unicornhathd.brightness(0.6)
    width, height = unicornhathd.get_shape()
    img = Image.open(srcdir.current)
    while True:
        for o_x in range(int(img.size[0]/width)):
            for o_y in range(int(img.size[1]/height)):
                valid = False
                for x in range(width):
                    for y in range(height):
                        pixel = img.getpixel(((o_x*width)+y,(o_y*height)+x))
                        r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
                        if r or g or b:
                            valid = True
                        unicornhathd.set_pixel(x, y, r, g, b)
                if valid:
                    unicornhathd.show()
                    if not(srcdir.checkCurrentIsLatest()):
                        unicornhathd.off()
                        return
                    time.sleep(0.8)
    return

def showImageFromTextFile(srcdir, unicornhathd):
    unicornhathd.rotation(-90)
    unicornhathd.brightness(0.6)
    f = open(srcdir.current)
    text = f.read()
    f.close()
    lines = [text]
    colors  = [(255,0,255),
                (0,255,255),
                (255,255,0),
                (0,255,0),
                (255,255,255)]
    FONT = ("/usr/share/fonts/truetype/droid/DroidSans.ttf", 10)

    width, height = unicornhathd.get_shape()
    text_x = width
    text_y = 2
    font_file, font_size = FONT
    font = ImageFont.truetype(font_file, font_size)

    text_width, text_height = width, 0

    for line in lines:
        w, h = font.getsize(line)
        text_width += w + width
        text_height = max(text_height,h)

    text_width += width + text_x + 1

    image = Image.new("RGB", (text_width,max(16, text_height)), (0,0,0))
    draw = ImageDraw.Draw(image)

    offset_left = 0

    for index, line in enumerate(lines):
        draw.text((text_x + offset_left, text_y), line, random.choice(colors), font=font)
        offset_left += font.getsize(line)[0] + width

    for scroll in range(text_width - width):
        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x+scroll, y))
                r, g, b = [int(n) for n in pixel]
                unicornhathd.set_pixel(width-1-x, y, r, g, b)
        unicornhathd.show()
        if not(srcdir.checkCurrentIsLatest()):
            unicornhathd.off()
            return
        time.sleep(0.01)
    unicornhathd.off()

#check -> show, while checking new input

srcdir = InputSourceDir(os.path.abspath(os.path.dirname(__file__)) + "/sources")
unicornhathd.rotation(-90)
unicornhathd.brightness(0.3)

while True:
    srcdir.getInput()
    if len(srcdir.current)==0:
        #print("Warning: nothing to display, I am going to wait news to come.")
        time.sleep(0.03)
    else:
        try:
            if srcdir.currentType      == "image":
                showImageFromFile(srcdir, unicornhathd)
            elif srcdir.currentType    == "text" :
                showImageFromTextFile(srcdir, unicornhathd)
        except IOError:
            pass
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)
        time.sleep(0.03)
```

## 参考にさせていただいたサイト
- []()




