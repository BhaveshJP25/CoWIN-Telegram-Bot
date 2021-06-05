from telegram import Bot, Update
from telegram.ext import *
import time
from datetime import datetime
import requests

headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}

#Add your BotID here
bot = Bot("")

district_id = '371'     # Kolhapur
date = '07-06-2021'     # Optional. Default value is today's date
min_age_limit = 18      # 18 / 45

# Example Of District ID
# district_id = '373'     # Sangli
# district_id = '563'     # Erode
# date = '27-05-2021'

def available_center():
    response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id="+district_id+"&date="+date, headers=headers)
    if response.ok:
        res = response.json()

        center_list = [session for session in res['sessions']]
        age_center_list = [i for i in center_list if i["min_age_limit"] == min_age_limit]

        return age_center_list
    else:
        return -1

updater = Updater("1811097373:AAG5BNZVQfoX99cEcqhBuBh6w9YbZEXn67M", use_context=True)
dispatcher = updater.dispatcher

def get_chat_id(update, context):
    chat_id = -1
    if update.message is not None:
        # from a text message
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        # from a callback message
        chat_id = update.callback_query.message.chat.id
    return chat_id

def test_function(update:Update, context:CallbackContext):
    print("Started")
    while(True):
        print(datetime.now())
        address = available_center()
        if(address == -1):
            print("\n-----ERROR------\n")
            continue
        # Select Dose1 or Dose2
        available_seat = [center["available_capacity_dose2"] for center in address]

        for i, center in zip(available_seat, address):
            if (i != 0):
                print("Element Exists")
                msg = str("Center Name : " + center["name"] +
                          "\nDistrict : " + center["district_name"] +
                          "\nPincode : " + str(center["pincode"]) +
                          "\nFee Type : " + center["fee_type"] +
                          "\nDate : " + center["date"] +
                          "\nDose 1 Available : " + str(center["available_capacity_dose1"]) +
                          "\nDose 2 Available : " + str(center["available_capacity_dose2"]) +
                          "\nVaccine Type : " + center["vaccine"] + "\n")
                bot.send_message(
                    chat_id=get_chat_id(update, context),
                    text=msg,
                )
        time.sleep(10)

start_value = CommandHandler('start', test_function)
dispatcher.add_handler(start_value)
updater.start_polling()
