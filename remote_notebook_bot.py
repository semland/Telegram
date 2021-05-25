import telebot
import datetime

#get a token from @fatherbot in Telegram
API_TOKEN = 'YOUR_TOKEN' 

bot = telebot.TeleBot(API_TOKEN)
    
# when you have write '/notebook' bot shows you a message and puts in control mode (see: def get_nb)
@bot.message_handler(commands=['notebook'])
def start(message):
    bot.send_message(message.from_user.id, """Remote Notebook: \n /show - show all notes \n /write - create a new note
/remove - clear the notebook \n /out - go out""")
    bot.register_next_step_handler(message, get_nb)

# get_nb opens after command '/notebook' and closes after '/out'
def get_nb(message):
    
    name = message.text
    
    if name == '/out':
        bot.send_message(message.from_user.id, 'You have exit from Remote Notebook. To enter write /notebook')
    elif name == '/show':
        file_nb = open('notebook.txt', mode='r+')
        bot.send_message(message.from_user.id, 'Notes in Remote Notenook: \n\n'+file_nb.read())
        bot.register_next_step_handler(message, get_nb)
        file_nb.close()
    elif name == '/write':
        bot.send_message(message.from_user.id, 'Send a message and it will be saved in the Remote Notebook')
        bot.register_next_step_handler(message, get_writer)
    elif name == '/remove':
        bot.send_message(message.from_user.id, 'Enter password to clear')
        bot.register_next_step_handler(message, get_remover)
    else:
        bot.send_message(message.from_user.id, """Remote Notebook: \n /show - show all notes \n /write - create a new note
/remove - clear the notebook \n /out - go out""")
        bot.register_next_step_handler(message, get_nb)

# get_writed opens a 'notebook.txt' in directory with *.py file and adds a your note
def get_writer(message):

    txt = message.text
    
    file_nb = open('notebook.txt', mode='a')
    file_nb.write('\n{}\n'.format(str(datetime.datetime.now())))
    file_nb.write(txt+'\n')
    bot.send_message(message.from_user.id, 'A note have been successfully added!')
    bot.register_next_step_handler(message, get_nb)
    file_nb.close()

def get_remover(message): #this function clear a notebook

    if message.text == 'aboba2021':
        file_nb = open('notebook.txt', mode='rb')
        file_nb.close()
        bot.send_message(message.from_user.id, 'Remote Notebook have been successfully cleared!')
    else:
        bot.send_message(message.from_user.id, 'Incorrect password')
        bot.register_next_step_handler(message, get_nb)

# when receiving any message, bot suggests to go to the notebook
@bot.message_handler(func=lambda message: True)
def send_welcome(message):
    bot.send_message(message.from_user.id, "/notebook - open the Remote Notebook")
    
bot.polling()
