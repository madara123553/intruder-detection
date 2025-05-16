import cv2
import face_recognition
import webbrowser
import asyncio
from telegram import Bot

# === Configuration ===
TELEGRAM_BOT_TOKEN = ''
TELEGRAM_CHAT_ID = ''
KNOWN_USER_IMAGE = 'known_face.jpg'

# === Load Known Face ===
print("[INFO] Loading known face...")
known_image = face_recognition.load_image_file(KNOWN_USER_IMAGE)
known_encoding = face_recognition.face_encodings(known_image)[0]

# === Initialize Telegram Bot ===
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_telegram_alert():
    try:
        message = "🚨 Intruder Detected!"
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print("[ALERT] Intruder message sent to Telegram.")
    except Exception as e:
        print(f"[ERROR] Failed to send Telegram message: {e}")

# === Start Camera ===
print("[INFO] Starting camera...")
video = cv2.VideoCapture(0)

detected = False

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Convert the frame from BGR (OpenCV) to RGB (face_recognition)
    rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB
    
    # Resize frame for faster processing
    small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)
    
    # Detect faces
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    match_found = False  # Flag to track if a known user is detected

    for encoding in face_encodings:
        match = face_recognition.compare_faces([known_encoding], encoding)
        print(f"[DEBUG] Match result: {match}")  # Debugging: See the result of face comparison

        if True in match:
            print("[ACCESS GRANTED] Known user detected.")
            webbrowser.open('https://www.google.com')  # or os.system("start chrome")
            match_found = True
            break
        else:
            print("[ACCESS DENIED] Intruder detected.")
            asyncio.run(send_telegram_alert())

    if match_found:
        break

    # Draw rectangles around faces (for visual debugging)
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Camera Feed', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
print("[INFO] Program ended.")
