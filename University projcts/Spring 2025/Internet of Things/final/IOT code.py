import RPi.GPIO as GPIO
import Adafruit_DHT
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 17  # GPIO17 (Pin 11)

LED_PIN = 18  # GPIO18 (Pin 12)
GPIO.setup(LED_PIN, GPIO.OUT)

SERVO_PIN = 22  # GPIO22 (Pin 15)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz frequency
servo.start(0)

ROWS = [5, 6, 13, 19]       # GPIO Pins
COLS = [12, 16, 20, 21]     # GPIO Pins

KEYPAD = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

for row in ROWS:
    GPIO.setup(row, GPIO.OUT)
    GPIO.output(row, GPIO.LOW)

for col in COLS:
    GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def read_keypad():
    for i, row in enumerate(ROWS):
        GPIO.output(row, GPIO.HIGH)
        for j, col in enumerate(COLS):
            if GPIO.input(col) == GPIO.HIGH:
                GPIO.output(row, GPIO.LOW)
                return KEYPAD[i][j]
        GPIO.output(row, GPIO.LOW)
    return None

def control_servo(temp, key=None):
    if key == '0' or (temp and temp > 28):
        print("Opening ventilation (servo → 90°)")
        servo.ChangeDutyCycle(7.5)
    elif key == '1' or (temp and temp < 22):
        print("Closing ventilation (servo → 0°)")
        servo.ChangeDutyCycle(2.5)

def read_dht():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{now}] Temp = {temperature:.1f}°C, Humidity = {humidity:.1f}%")
        return temperature, humidity
    else:
        print("Failed to retrieve DHT11 data")
        return None, None

try:
    while True:
        key = read_keypad()
        temp, _ = read_dht()

        if key == 'A':
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("LED turned ON")
        elif key == 'B':
            GPIO.output(LED_PIN, GPIO.LOW)
            print("LED turned OFF")

        control_servo(temp, key)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nExiting safely...")
    servo.stop()
    GPIO.cleanup()