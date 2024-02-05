import os
import sys
import telegram.ext
import subprocess

api_key = ""

try:
    with open(os.path.join(sys.path[2], "api_key.txt"), "r") as file:
        api_key += file.read()
        file.close()
except FileNotFoundError:
    with open(os.path.join(sys.path[0], "api_key.txt"), "r") as file:
        api_key += file.read()
        file.close()

def handle_message(update, context):
    usr = update.message.text
    usr = usr.split(" ")
    try:
        result = subprocess.run(usr, shell=True, capture_output=True, text=True)
        if len(result.stdout) <= 4000:
            if result.stdout != "":
                update.message.reply_text(result.stdout)
            elif result.stderr != "":
                update.message.reply_text(result.stderr)
            else:
                update.message.reply_text("Done!")
        else:
            update.message.reply_text("The Output Is Too Long!")
    except Exception as error:
        print(error)
        update.message.reply_text("Some Error Happend!")


Token = api_key
updater = telegram.ext.Updater(api_key, use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
updater.start_polling()
updater.idle()
