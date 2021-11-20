---
title: "Raspberry Pi のネットワークが不安定"
date: 2019-02-27 21:00
tags: RaspberryPi
---

二年間くらい（僕の観測範囲では）WIFI通信が安定しない。
いい加減うんざりしているので少し調べて調べたことを記録することにする。
　（解決しました。結局iwconfigでOK）

<img src="./RPi-Logo-Landscape-SCREEN.png" style="width:300px;margin-left:1em;" />

## 現象
- 起動後は、外部からRaspberry Piへのアクセスが可能
    - hostname.localへのpingや、sshも可能
    - IPはDHCPで配布（ルータ側でのIP固定なし）
    - WIFI接続
- しかし、暫く経過すると、外部からのping/sshに一切応答がなくなる。
    - 解決するには電源Off/Onが必要


## NG①：　省電力モードなるものをOff
- 挙動に何の変化も見られず
- コマンドは
```
sudo iwconfig wlan0 power off
```

## NG②： ネットワーク断を検知して対応
- 挙動に何の変化もみられず
- raspi->外部へpingを打ち続け、ネットワーク断ならばifdown/ifupするはずであるが、ログをみるとそもそも自分から外にはずっと通信できているようにみえる。
- つまり、外->RaspiからがNGなのであって、Raspi->外はOK
-- [ここの議論で紹介されているもの；Persistent/reconnecting wifi](https://www.raspberrypi.org/forums/viewtopic.php?t=54001)

** sample script **
```
echo "Performing Network check for $wlan"
/bin/ping -c 2 -I $wlan $pingip > /dev/null 2> /dev/null
if [ $? -ge 1 ] ; then
    echo "Network connection down! Attempting reconnection."
    /sbin/ifdown $wlan
    sleep 5
    /sbin/ifup --force $wlan
else
    echo "Network is Okay"	
fi
```

## NG？③： static ARPを切って見る
- 改善あり
- 外->内の通信がNGということはARPに応答してくれない虞がある。なので以下のように切って見ると通信がOKとなった
    - これをssh元のPC/macにおいて実施する
```
sudo arp -s RaspiのIPアドレス RaspiのMACアドレス
```
    - ただ、こんなやり方する位ならIP固定とか、DHCPが強制的に割り当てた方がマシ

## NG④：modprobeで省電力機能を切る
　これがうまくいく方法にみえていたがやっぱり再発した気配がする。。。
- macでarpを打つとやっぱりarp応答がもらえていない気配。
    - incomplete の部分から
            hostname:~ loginid$ arp -a
            xxx.xxx (192.168.1.1) at 10:4b:46:4f:f1:1d on en0 ifscope [ethernet]
            ? (192.168.1.22) at (incomplete) on en0 ifscope [ethernet]

- 私の環境では、以下の方法ではダメであった
```
sudo vi /etc/modprobe.d/8192cu.conf
#viの画面で以下を入力
options 8192cu rtw_power_mgnt=0 rtw_enusbss=1 rtw_ips_mode=1
#viを閉じた後再起動
sudo shutdown -r now
```
    - [min117さんの日記](http://min117.hatenablog.com/entry/2017/10/09/163052)
        - > RaspberryPi 3 無線LANが寸断するのは /etc/modprobe.d/8192cu.conf に「options 8192cu rtw_power_mgnt=0 rtw_enusbss=1 rtw_ips_mode=1」を書いて解決
    - [Adafruitの記事中の記載](https://learn.adafruit.com/pi-wifi-radio/raspberry-pi-setup-1-of-3)
        - > if using a WiFi adapter based on the popular Realtek 8192CU chipset, disabling WiFi power management seems to help with reliability:
```
echo "options 8192cu rtw_power_mgnt=0 rtw_enusbss=0" | sudo tee --append /etc/modprobe.d/8192cu.conf
```

## 確認中： 結局iwconfigなのか。。->解決
　今度はどうだ
- ここで解説されていたもの
    - [Disable power management in Stretch](https://www.raspberrypi.org/forums/viewtopic.php?t=194619)
- まずインタフェースの設定を変更し、再起動する
```
sudo vi /etc/rc.local
#viの画面でexit文の前に以下を入力
sudo iwconfig wlan0 power off

#viを閉じた後再起動
sudo shutdown -r now
```
- 再起動後に、iwconfigの出力に“Power Management:off”が入っているか確認
    - iwconfig




## 参考にさせていただいたサイト
- [(本文中に記載)]()
- [The image of Raspberry Pi logo is licensed under CC BY-SA 4.0 ](https://commons.wikimedia.org/wiki/Raspberry_Pi_logos)

