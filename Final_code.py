import cv2
import torch
import threading
import time
import RPi.GPIO as GPIO
import os
from ultralytics import YOLO
from smbus2 import SMBus
from RPLCD.i2c import CharLCD
import BlynkLib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client

# Twilio Credentials
ACCOUNT_SID = "your_account_sid"
ACCOUNT_AUTH = "your_account_auth_token"
TWILIO_NUMBER = "your_twilio_number"
TARGET_NUMBER = "target_phone_number"
WHATSAPP_NUMBER = "whatsapp_phone_number"

# SMTP Credentials
SENDER_MAIL = "your_email@gmail.com"
APP_PASSWORD = "your_email_app_password"
RECEIVERS_MAIL = "receiver_email@gmail.com"

# Blynk Credentials
BLYNK_AUTH = "your_blynk_auth_token"
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Audio files
AUDIO_FILES = {
    "bird": "/home/pi/Digital_Scarecrow_Project/Audio/birds_voice.mp3",
    "monkey": "/home/pi/Digital_Scarecrow_Project/Audio/monkeys_voice.mp3",
    "wildboar": "/home/pi/Digital_Scarecrow_Project/Audio/wildboar_voice.mp3",
}

# Load YOLOv8 model
model = YOLO("/home/pi/Digital_Scarecrow_Project/best.pt")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)

# Class labels
class_names = ["bird", "monkey", "wildboar"]

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# Initialize Twilio client
client = Client(ACCOUNT_SID, ACCOUNT_AUTH)

# GPIO setup
BUZZER_PIN = 6
LED_PIN = 23
SERVO_PIN = 18
GREEN_LED_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)

# Servo motor setup
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(7.5)

# LCD setup
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)
lcd.write_string("DigitalScarecrow")
time.sleep(10)
lcd.clear()

frame_lock = threading.Lock()
latest_frame = None
running = True
object_detected_time = None
buzzer_active = False
servo_active = False
last_display_message = ""
detection_log = {}

# Blynk Control Variables
blynk_buzzer = True
blynk_servo = True

# FPS Variables
fps_counter = 0
fps_start_time = time.time()
fps = 0

# Capture Frames
def capture_frames():
    global latest_frame, running
    while running:
        ret, frame = cap.read()
        if ret:
            with frame_lock:
                latest_frame = frame
        time.sleep(0.01)

thread = threading.Thread(target=capture_frames, daemon=True)
thread.start()

def rotate_servo():
    while servo_active:
        for duty_cycle in range(25, 125, 2):
            servo.ChangeDutyCycle(duty_cycle / 18 + 2.5)
            time.sleep(0.05)
        for duty_cycle in range(125, 25, -2):
            servo.ChangeDutyCycle(duty_cycle / 18 + 2.5)
            time.sleep(0.05)
    servo.ChangeDutyCycle(7.5)

def send_whatsapp_notification(detected_class):
    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886',  # Your Twilio WhatsApp number
            body=f'{detected_class.upper()} DETECTED IN YOUR FARM!', # Dynamic content
            to=f'whatsapp:{WHATSAPP_NUMBER}' # Recipient's WhatsApp number
        )
        print(f"WhatsApp notification sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"WhatsApp notification failed: {e}")
        

def send_sms_notification(detected_class):
    try:
        message = client.messages.create(
            body=f"A {detected_class} has been detected by the Digital Scarecrow.",
            from_=TWILIO_NUMBER,
            to=TARGET_NUMBER
        )
        print(f"SMS notification sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"SMS notification failed: {e}")

def send_email_notification(detected_class):
    message = MIMEMultipart()
    message['From'] = SENDER_MAIL
    message['To'] = RECEIVERS_MAIL
    message['Subject'] = f"Object Detected: {detected_class.upper()}"

    body = f"A {detected_class} has been detected by the Digital Scarecrow."
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_MAIL, APP_PASSWORD)
            server.sendmail(SENDER_MAIL, RECEIVERS_MAIL, message.as_string())
        print("Email notification sent successfully!")
    except Exception as e:
        print(f"Email notification failed: {e}")

def activate_buzzer_audio_servo(detected_class):
    global buzzer_active, servo_active
    if not blynk_buzzer:
        print("Buzzer is OFF via Blynk, skipping activation.")
        return  

    print("Activating Buzzer, LED, and Servo.")
    
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    GPIO.output(LED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    
    if blynk_servo:
        servo_active = True
        servo_thread = threading.Thread(target=rotate_servo, daemon=True)
        servo_thread.start()
    
    audio_file = AUDIO_FILES.get(detected_class)
    if audio_file:
        os.system(f"ffplay -nodisp -autoexit {audio_file} &")
    
    time.sleep(20)

    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    buzzer_active = False
    servo_active = False

# Blynk Handlers
# Buzzer Control
# @blynk.on("V0")
# def v0_handler(value):
#     global blynk_buzzer
#     blynk_buzzer = bool(int(value[0]))
#     print(f"Buzzer control updated: {'ON' if blynk_buzzer else 'OFF'}")

# Servo Motor Control
@blynk.on("V1")
def v1_handler(value):
    global blynk_servo
    blynk_servo = bool(int(value[0]))

# Play Monkey Sound
@blynk.on("V2")
def v2_handler(value):
    if int(value[0]) == 1:
        os.system(f"ffplay -nodisp -autoexit {AUDIO_FILES['monkey']} &")

# Play Bird Sound
@blynk.on("V3")
def v3_handler(value):
    if int(value[0]) == 1:
        os.system(f"ffplay -nodisp -autoexit {AUDIO_FILES['bird']} &")

# Play Wild Boar Sound
@blynk.on("V4")
def v4_handler(value):
    if int(value[0]) == 1:
        os.system(f"ffplay -nodisp -autoexit {AUDIO_FILES['wildboar']} &")
        
# Text Data for Detected Object
@blynk.on("V5")
def v5_handler(value):
    blynk.virtual_write(5, detected_object)

GPIO.output(GREEN_LED_PIN, GPIO.HIGH)

while True:
    try:
        blynk.run()
    except Exception as e:
        print(f"Blynk Error: {e}")
    
    with frame_lock:
        if latest_frame is None:
            continue
        frame = latest_frame.copy()

    fps_counter += 1
    if time.time() - fps_start_time >= 1:
        fps = fps_counter
        fps_counter = 0
        fps_start_time = time.time()

    with torch.no_grad():
        results = model(frame, imgsz=256, verbose=False)

    object_present = False
    detected_object = "SAFE"
    detected_class = None

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            
            if conf > 0.3:
                object_present = True
                detected_class = class_names[cls]
                detected_object = f"{detected_class.upper()} DETECTED"
                label = f"{detected_class}: {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                detection_log[detected_class] = detection_log.get(detected_class, 0) + 1

    if object_present:
        if object_detected_time is None:
            object_detected_time = time.time()
        elif time.time() - object_detected_time >= 5 and not buzzer_active:
            buzzer_active = True
            threading.Thread(target=activate_buzzer_audio_servo, args=(detected_class,), daemon=True).start()
            send_email_notification(detected_class) # Send email notification
            send_sms_notification(detected_class) # Send sms notification
            send_whatsapp_notification(detected_class) # Send whatsapp
    else:
        object_detected_time = None

    if detected_object != last_display_message:
        lcd.clear()
        lcd.write_string(detected_object)
        last_display_message = detected_object

    # Display FPS on the frame
    cv2.putText(frame, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display object status
    blynk.virtual_write(5, detected_object)  

    # Show the frame
    cv2.imshow("YOLOv8 Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        running = False
        break

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
servo.stop()
