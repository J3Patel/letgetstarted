import threading
import time
import RPi.GPIO as GPIO
import snowboydecoder
import sys
import signal
import os

interrupted = False
threads = list()

def playgoca():
    time.sleep(2)
    os.system('aplay -d 20 goca.wav')

def lightsStartEffect():
    c = 0;
    while c != 20:
        c += 1
        GPIO.output(25, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(25, GPIO.LOW)
        time.sleep(0.05)
    GPIO.output(25, GPIO.LOW)

def confetti():
    GPIO.output(25, GPIO.LOW)

def angleg():
    GPIO.output(25, GPIO.LOW)

def drill():
    GPIO.output(25, GPIO.LOW)

def lights():
    while not interrupted:
        GPIO.output(25, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(25, GPIO.LOW)
        time.sleep(0.05)
example=0

def detected():
    x = threading.Thread(target=playgoca, args=())
    threads.append(x)
    x.start()

    y = threading.Thread(target=lightsStartEffect, args=())
    threads.append(y)
    y.start()


def signal_handler(signal, frame):
    # example.stop()
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)
GPIO.setup(25, GPIO.OUT)
GPIO.output(25, GPIO.LOW)
TRIG=23
ECHO=24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
time.sleep(2)

def disponce():
    GPIO.output(18, GPIO.LOW)
    GPIO.output(25, GPIO.HIGH)
    time.sleep(0.15)
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(25, GPIO.LOW)
    time.sleep(5)

def readDistace():
    while not interrupted:
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        while GPIO.input(ECHO)==0:
           pulse_start = time.time()

        while GPIO.input(ECHO)==1:
           pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print "Distance:",distance,"cm"
        time.sleep(0.3)
        if distance < 10:
            disponce()


y = threading.Thread(target=readDistace, args=())
threads.append(y)
y.start()


model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=detected,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
