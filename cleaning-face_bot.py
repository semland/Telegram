import telebot
import cv2
import numpy

API_TOKEN = 'YOUR_TOKEN'

bot = telebot.TeleBot(API_TOKEN)

def delete_faces(detected, image, color: tuple):
    for (x, y, width, height) in detected:
        cv2.rectangle(
            image,
            (x, y),
            (x + width, y + height),
            color,
            thickness=-1
        )
        
@bot.message_handler(content_types=['document'])
def handle_file(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        original_image = cv2.imread(src)
        avg_color_per_row = numpy.average(original_image, axis=0)
        avg_color = tuple(numpy.average(avg_color_per_row, axis=0))
        
        if original_image is not None:
            # Convert image to grayscale
            image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

            # Create Cascade Classifiers
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
            
            # Detect faces using the classifiers
            detected_faces = face_cascade.detectMultiScale(image=image, scaleFactor=1.3, minNeighbors=4)
            detected_profiles = profile_cascade.detectMultiScale(image=image, scaleFactor=1.3, minNeighbors=4)

            # Filter out profiles
            profiles_not_faces = [x for x in detected_profiles if x not in detected_faces]

            # Draw rectangles around faces on the original, colored image
            delete_faces(detected_faces, original_image, avg_color) # RGB - green
            delete_faces(detected_profiles, original_image, avg_color) # RGB - red

            # The window will close as soon as any key is pressed (not a mouse click)
            cv2.imwrite('face-free.jpg', original_image)
        else:
            print(f'En error occurred while trying to load')

        photo = open('face-free.jpg', 'rb')
        bot.send_photo(message.from_user.id, photo)
        photo.close()
    except Exception as e:
        bot.reply_to(message, e)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_message(message.from_user.id, 'Отправь фотографию как документ, а я уберу на ней лица!')
    
bot.polling()
