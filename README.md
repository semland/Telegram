# Telegram bots by semland

**remote_notebook_bot.py** - this telegram bot allows you to remotely keep a notebook on your PC or laptop

You can view the notebook and add notes to it. All records are dated using the datetime library. You can also clear the book at a convenient moment. A password is required to clear the book (default: aboba2021). You can change it in code.

/notebook - enter Remote Notebook mode

/show - show everything in 'notebook.txt' on your PC

/write - add new entry with date and time in 'notebook.txt'

/remove - clear 'notebook.txt'

/out - exit Remote Notebook mode

**cleaning-face_bot.py** (raw) - this telegram bot finds people's faces in the photo (using OpenCV) and fills them with an average color

For the bot to work, you need to upload a photo as a document, then it will send the processed photo.
