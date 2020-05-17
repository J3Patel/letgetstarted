import threading
import time
import RPi.GPIO as GPIO
# import snowboydecoder
import sys
import signal
import os
import pyaudio
import numpy as np

CHUNK = 2**11
RATE = 44100
interrupted = False
audDetected = False
shouldStop = False
threads = list()
p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)
example=0

def playintro():
    # time.sleep(2)
    os.system('aplay -d 20 new.wav')

def lightsStartEffect():
    c = 0
    GPIO.output(24, GPIO.LOW)
    time.sleep(2)
    roomf()
    while c != 80 and not interrupted:
        c += 1
        GPIO.output(24, GPIO.LOW)
        time.sleep(0.08)
        GPIO.output(24, GPIO.HIGH)
        time.sleep(0.08)
    # stopEverything()

def confetti():
    GPIO.output(1, GPIO.LOW)

def sinch():
    GPIO.output(7, GPIO.LOW)

def machineStart():
    GPIO.output(23, GPIO.LOW)
    time.sleep(0.8)
    GPIO.output(23, GPIO.HIGH)

def angleg():
    GPIO.output(25, GPIO.LOW)

def roomf():
    GPIO.output(8, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(8, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(8, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(8, GPIO.HIGH)
    time.sleep(0.5)

def drill():
    GPIO.output(25, GPIO.LOW)
    time.sleep(2)
    GPIO.output(25, GPIO.HIGH)

def audioDetect():
    global audDetected
    while not interrupted and not audDetected:
        data = np.fromstring(stream.read(CHUNK, exception_on_overflow = False),dtype=np.int16)
        peak=np.average(np.abs(data))*2
        if peak > 50000:
            # global audDetected
            detected()
        # bars="#"*int(50*peak/2**16)
        # print("%04d %05d %s"%(i,peak,bars))
    stream.stop_stream()
    stream.close()
    p.terminate()

def startOthers():
    time.sleep(4)
    angleg()
    confetti()

def stopEverything():
    global interrupted
    interrupted = True
    GPIO.output(25, GPIO.HIGH)
    GPIO.output(8, GPIO.HIGH)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(1, GPIO.HIGH)

    time.sleep(2)
    GPIO.output(7, GPIO.LOW)
    time.sleep(0.05)
    GPIO.output(7, GPIO.HIGH)

def detected():
    stream.stop_stream()
    stream.close()
    p.terminate()
    global audDetected
    audDetected = True
    x = threading.Thread(target=playintro, args=())
    threads.append(x)
    x.start()

    y = threading.Thread(target=lightsStartEffect, args=())
    threads.append(y)
    y.start()

    z = threading.Thread(target=startOthers, args=())
    threads.append(z)
    z.start()
    machineStart()

    time.sleep(10)
    stopEverything()

def signal_handler(signal, frame):
    # example.stop()
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.HIGH)
GPIO.setup(25, GPIO.OUT)
GPIO.output(25, GPIO.HIGH)
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, GPIO.HIGH)

GPIO.setup(8, GPIO.OUT)
GPIO.output(8, GPIO.HIGH)

GPIO.setup(7, GPIO.OUT)
GPIO.output(7, GPIO.HIGH)

GPIO.setup(1, GPIO.OUT)
GPIO.output(1, GPIO.HIGH)

time.sleep(2)



y = threading.Thread(target=audioDetect, args=())
threads.append(y)
y.start()

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)
