# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
import sys
import RPi.GPIO as GPIO
from random import randrange
 
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
 
 
# Configure the count of pixels:
PIXEL_COUNT = 150
 
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)
 
 
# Define the wheel function to interpolate between different hues.
def wheel(pos):
    if pos < 85:
        return Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Adafruit_WS2801.RGB_to_color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Adafruit_WS2801.RGB_to_color(0, pos * 3, 255 - pos * 3)
 
# Define rainbow cycle function to do a cycle of all hues.
def rainbow_cycle_successive(pixels, wait=0.1):
    for i in range(pixels.count()):
        # tricky math! we use each pixel as a fraction of the full 96-color wheel
        # (thats the i / strip.numPixels() part)
        # Then add in j which makes the colors go around per pixel
        # the % 96 is to make the wheel cycle around
        pixels.set_pixel(i, wheel(((i * 256 // pixels.count())) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def rainbow_cycle(pixels, wait=0.005):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((i * 256 // pixels.count()) + j) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def rainbow_colors(pixels, wait=0.05):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((256 // pixels.count() + j)) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def brightness_decrease(pixels, wait=0.01, step=1):
    for j in range(int(256 // step)):
        for i in range(pixels.count()):
            r, g, b = pixels.get_pixel_rgb(i)
            r = int(max(0, r - step))
            g = int(max(0, g - step))
            b = int(max(0, b - step))
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( r, g, b ))
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def blink_color(pixels, blink_times=5, wait=0.5, color=(255,0,0)):
    for i in range(blink_times):
        # blink two times, then wait
        pixels.clear()
        for j in range(2):
            for k in range(pixels.count()):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            pixels.show()
            time.sleep(0.08)
            pixels.clear()
            pixels.show()
            time.sleep(0.08)
        time.sleep(wait)
 
def appear_from_back(pixels, color=(255, 0, 0)):
    pos = 0
    for i in range(pixels.count()):
        for j in reversed(range(i, pixels.count())):
            pixels.clear()
            # first set all pixels at the begin
            for k in range(i):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            # set then the pixel at position j
            pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            pixels.show()
            time.sleep(0.02)

def turnOff(pixels):
    pixels.clear()        

def setOneColorForAll(pixels, color = (255, 0, 0)):
    pixels.clear()
    for i in range(pixels.count()):
        pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(color[0], color[1], color[2]))
    pixels.show()

def setHalfColors(pixels, colorA = (255, 0, 0), colorB = (0, 0, 255)):
    pixels.clear()
    for i in range(pixels.count()):
        if (pixels.count() / 2) > i:
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(colorA[0], colorA[1], colorA[2]))
        else:
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(colorB[0], colorB[1], colorB[2]))
    pixels.show() 

def setAllPixelsRandom(pixels):
    pixels.clear()
    for i in range(pixels.count()):
        r, g, b = randrange(256), randrange(256), randrange(256)
        pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(r, g, b))
    pixels.show()

def setTwoColorsCycle(pixels, colorA = (255, 0, 0), colorB = (0, 0, 255)):
    pixels.clear()
    for i in range(pixels.count()):
        if i % 2 == 0:
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(colorA[0], colorA[1], colorA[2]))
        else:
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(colorB[0], colorB[1], colorB[2]))
    pixels.show()

def runningColorsRight(pixels, loops = 1):
    for i in range(loops * pixels.count()):
	rLast, gLast, bLast = pixels.get_pixel_rgb(pixels.count()-1)
	for j in range(pixels.count()-1, -1, -1):
	    r, g, b = pixels.get_pixel_rgb(j-1) if j-1 != -1 else pixels.get_pixel_rgb(pixels.count()-1)
	    pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(r, g, b))
	pixels.set_pixel(0, Adafruit_WS2801.RGB_to_color(rLast, gLast, bLast))
   	pixels.show()
	time.sleep(0.08)

def runningColorsLeft(pixels, loops = 1):
    for i in range(loops * pixels.count()):
	rFirst, gFirst, bFirst = pixels.get_pixel_rgb(0)
	for j in range(pixels.count()-1):
	    r, g, b = pixels.get_pixel_rgb(j+1)
            pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(r, g, b))
	pixels.set_pixel(pixels.count()-1, Adafruit_WS2801.RGB_to_color(rFirst, gFirst, bFirst))
	pixels.show()
	time.sleep(0.08)

def onePixelRunning(pixels, direction = "left", color = (255, 0, 0)):
    index = 0 if direction == "left" else pixels.count()-1
    pixels.clear()
    pixels.set_pixel(index, Adafruit_WS2801.RGB_to_color(color[0], color[1], color[2]))
    if direction == "left": runningColorsLeft(pixels, 3)
    else: runningColorsRight(pixels, 3)

def runningToMiddle(pixels, loops = 1, colorA = (255, 0, 0), colorB = (0, 0, 255)):
    mid = pixels.count() / 2
    pixels.clear()
    for i in range(pixels.count()): pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(colorA[0], colorA[1], colorA[2]))
    for loop in range(loops):
        pixels.set_pixel(mid-1, Adafruit_WS2801.RGB_to_color(colorB[0], colorB[1], colorB[2]))
        pixels.show()
        for i in range(mid):
	    if (i != mid-1): pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(colorB[0], colorB[1], colorB[2]))
	    pixels.set_pixel(pixels.count()-1-i, Adafruit_WS2801.RGB_to_color(colorB[0], colorB[1], colorB[2]))
            pixels.show()
	    time.sleep(0.08)
        pixels.set_pixel(mid-1, Adafruit_WS2801.RGB_to_color(colorA[0], colorA[1], colorA[2]))
        pixels.show()
        for i in range(mid):
	    if (i != 0): pixels.set_pixel(mid-1-i, Adafruit_WS2801.RGB_to_color(colorA[0], colorA[1], colorA[2]))
	    pixels.set_pixel(mid+i, Adafruit_WS2801.RGB_to_color(colorA[0], colorA[1], colorA[2]))
            pixels.show()
	    time.sleep(0.08)

def xMasMode(pixels):
    r, g, w = (255, 0, 0), (0, 128, 0), (255, 255, 255)
    blinkTime, waitTime = 20, 0.1
    for k in range(blinkTime):
        pixels.clear()
        for j in range(2):
            for i in range(pixels.count()):
                if i > 2*(pixels.count() / 3):
                    pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(g[0], g[1], g[2]))
                elif i > (pixels.count() / 3):
                    pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(w[0], w[1], w[2]))
                else:
                    pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(r[0], r[1], r[2]))
            pixels.show()
            time.sleep(0.08)
            pixels.clear()
            pixels.show()
            time.sleep(0.08)
        time.sleep(waitTime) 

def help():
    print("LED Control Help")
    print("----------------")
    print("One Color Light: oneColor-redness-greeness-blueness\nExample (blue): oneColor-0-255-0")
    print("----------------")

def callMappedFunctionWithArgs(pixels, args):
    functionMapper = {
		      "xMas" : lambda: xMasMode(pixels), 
		      "oneColor" : lambda: setOneColorForAll(pixels, color = (int(args[1]), int(args[2]), int(args[3]))),
		      "off" : lambda: turnOff(pixels),
		      "help" : lambda: help(),
		      "random" : lambda: setAllPixelsRandom(pixels),
		      "2Cycle" : lambda: setTwoColorsCycle(pixels, colorA = (int(args[1]), int(args[2]), int(args[3])), colorB = (int(args[4]), int(args[5]), int(args[6]))),
		      "half" : lambda: setHalfColors(pixels, colorA = (int(args[1]), int(args[2]), int(args[3])), colorB = (int(args[4]), int(args[5]), int(args[6]))),
		      "rainbow" : lambda: rainbow_cycle(pixels, float(args[1])),
		      "oneRun" : lambda: onePixelRunning(pixels, args[1], color = (int(args[2]), int(args[3]), int(args[4]))),
		      "runMiddle" : lambda: runningToMiddle(pixels, int(args[1]), colorA = (int(args[2]), int(args[3]), int(args[4])), colorB = (int(args[5]), int(args[6]), int(args[7])))
		     }
    functionMapper[args[0]]()

def test(arg):
    print(arg[0])
    print(arg)
    print(arg[1:])

def test2(x):
    mid = len(x) / 2
    halfA, halfB, rhA, rhB = list(), list(), list(), list()
    for i in range(mid):
	if (i != mid-1): halfA.append(x[i])
	halfB.append(x[len(x)-1-i])
	if (i != 0): rhA.append(x[mid-1-i])
	rhB.append(x[mid+i])
    print("mid:", mid)
    print("Mid Element:", x[mid-1])
    print("First Half:", halfA)
    print("Second Half:", halfB)
    print(rhA)
    print(rhB)

if __name__ == "__main__":
    contents = sys.argv[1].split('-')
    
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!
    
    """rainbow_cycle_successive(pixels, wait=0.1)
    rainbow_cycle(pixels, wait=0.01)
 
    brightness_decrease(pixels)
    
    appear_from_back(pixels)"""
    
    """for i in range(3):
        blink_color(pixels, blink_times = 2, color=(255, 0, 0))
        blink_color(pixels, blink_times = 2, color=(0, 255, 0))
        blink_color(pixels, blink_times = 2, color=(0, 0, 255))"""
    
    #setOneColorForAll(pixels, color = (255, 69, 0))
    #setHalfColors(pixels, colorA = (255, 0, 0), colorB = (0, 255, 0))
    #setAllPixelsRandom(pixels)
    #xMasMode(pixels)
    #setTwoColorsCycle(pixels, colorA = (255, 0, 0), colorB = (0, 0, 255))
    #runningColorsRight(pixels, loops = 10)
    #runningColorsLeft(pixels, loops = 10)
    #turnOff(pixels)
    
    test(contents)
    print("")
    test2([1, 2, 3, 4, 5, 6])
    callMappedFunctionWithArgs(pixels, contents) 

    #rainbow_colors(pixels)
    
    #brightness_decrease(pixels)
