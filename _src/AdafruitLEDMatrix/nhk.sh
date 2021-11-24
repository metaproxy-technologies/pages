#!/bin/sh
#Copyright (c) 2017 Tomohiko Araki
#Released under the MIT license
#http://opensource.org/licenses/mit-license.php
URL="hls://nhkradioakr1-i.akamaihd.net/hls/live/511633/1-r1/1-r1-01.m3u8"
livestreamer --yes-run-as-root $URL best -p mplayer &

