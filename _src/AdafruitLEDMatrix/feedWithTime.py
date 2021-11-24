#!/usr/bin/env python
# -*- encoding:utf8 -*-
# Copyright (C) 2013 Henner Zeller <h.zeller@acm.org> for original work.
# Copyright (C) 2017 Tomohiko Araki <arakitomohiko@gmail.com> for delivertive work.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation version 2.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://gnu.org/licenses/gpl-2.0.txt>

import time
import datetime
import argparse
import sys
import os
import random
import feedparser
from PIL import Image
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
#load Logger
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def getTime(fontsize):
    path = os.path.abspath(os.path.dirname(__file__))
    text = datetime.datetime.now().strftime('%H:%M')

    if fontsize == 8:
        font   = [ImageFont.truetype(path + '/font/ModernDOS9x14.ttf', 9),1]
        #font   = [ImageFont.truetype(path + '/font/misaki_gothic.ttf', fontsize),1]
    else:
        fontsize = 16
        font  = [ImageFont.truetype(path + '/font/mplus-2c-medium.ttf', fontsize),-2]
        #font  = [ImageFont.truetype(path + '/font/Makinas-Scrap-5.otf', fontsize),-2]
        #font  = [ImageFont.truetype(path + '/font/PixelMplus10-Regular.ttf', fontsize),1]

    color  = [(255 ,255, 0)]

    width, ignore = font[0].getsize(text)
    im = Image.new("RGB", (width + 30, fontsize), (15,15,15))
    draw = ImageDraw.Draw(im)
    draw.text((2, font[1]), text, random.choice(color), font=font[0])
    return im

def run(imText, matrix):
    print("Running")
    imTime = getTime(8)

    #image = Image.new('RGB', (imText.size[0], imText.size[1] + imTime.size[1]))
    #image.paste(imText, (0, 0))
    #image.paste(imTime, (0, imText.size[1]))
    ## *** image.resize((matrix.width, matrix.height), Image.ANTIALIAS)

    double_buffer = matrix.CreateFrameCanvas()
    img_width, img_height = imText.size
    # let's scroll
    xpos = 0
    while True:
        xpos += 1
        if (xpos > img_width):
            xpos = 0
            break
        
        double_buffer.SetImage(imText, -xpos)
        double_buffer.SetImage(imTime, 0, 8)
    
        double_buffer = matrix.SwapOnVSync(double_buffer)
        time.sleep(0.045) #===========modifled

def prepareMatrix(parser):
    args    = parser.parse_args()
    options = RGBMatrixOptions()
    if args.led_gpio_mapping != None:
      options.hardware_mapping = args.led_gpio_mapping
    options.rows = args.led_rows
    options.chain_length = args.led_chain
    options.parallel = args.led_parallel
    options.pwm_bits = args.led_pwm_bits
    options.brightness = args.led_brightness
    options.pwm_lsb_nanoseconds = args.led_pwm_lsb_nanoseconds
    if args.led_show_refresh:
      options.show_refresh_rate = 1
    if args.led_slowdown_gpio != None:
        options.gpio_slowdown = args.led_slowdown_gpio
    if args.led_no_hardware_pulse:
      options.disable_hardware_pulsing = True
    return RGBMatrix(options = options)

def getImageFromFile(path):
    image = Image.open(path).convert('RGB')
    return image

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--led-rows", action="store", help="Display rows. 16 for 16x32, 32 for 32x32. Default: 32", default=16, type=int)
parser.add_argument("-c", "--led-chain", action="store", help="Daisy-chained boards. Default: 1.", default=1, type=int)
parser.add_argument("-P", "--led-parallel", action="store", help="For Plus-models or RPi2: parallel chains. 1..3. Default: 1", default=1, type=int)
parser.add_argument("-p", "--led-pwm-bits", action="store", help="Bits used for PWM. Something between 1..11. Default: 11", default=11, type=int)
parser.add_argument("-b", "--led-brightness", action="store", help="Sets brightness level. Default: 100. Range: 1..100", default=10, type=int)
parser.add_argument("-m", "--led-gpio-mapping", help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm" , choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'], type=str)
parser.add_argument("--led-scan-mode", action="store", help="Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default)", default=1, choices=range(2), type=int)
parser.add_argument("--led-pwm-lsb-nanoseconds", action="store", help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130", default=130, type=int)
parser.add_argument("--led-show-refresh", action="store_true", help="Shows the current refresh rate of the LED panel")
parser.add_argument("--led-slowdown-gpio", action="store", help="Slow down writing to GPIO. Range: 1..100. Default: 1", choices=range(3), type=int)
parser.add_argument("--led-no-hardware-pulse", action="store", help="Don't use hardware pin-pulse generation")
parser.add_argument("-i", "--image", help="The image to display", default="./news.ppm")

imgdir = os.path.abspath(os.path.dirname(__file__)) + "/newsimg"
matrix = prepareMatrix(parser)

if not os.path.isdir(imgdir):
    print("Error: no img to display, no such directory.")
    sys.exit(0)
else:
    while True:
        files = os.listdir(imgdir)
        if len(files)==0:
            print("Warning: no img to display, I am going to wait news to come.")
            time.sleep(5.0)
        else:
            frnd = random.sample(files,len(files))
            for f in frnd:
                if f[-4:] == '.ppm':
                    f = os.path.join(imgdir, f)
                    try:
                        if os.path.exists(f):
                            run(getImageFromFile(f), matrix)
                        else:
                            print("Warning: no such file, next please...")
                    except IOError:
                        print("Warning: no such file, next please...")
                    except KeyboardInterrupt:
                        print("Exiting\n")
                        sys.exit(0)
                else:
                    printf("Warning: Please do not include non-ppm files.")
                    sys.exit(0)

