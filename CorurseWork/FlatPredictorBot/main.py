import telebot
from LinearRegrModel import predict_flat_cost
from FlatDataReader import read_data_from_doc

bot = telebot.TeleBot(token='6103182133:AAG_eAFF7a38PFhA6q19V_lvw7DVSGtKYIk')
MY_ID = 407742044


@bot.message_handler(commands=['start'])
def handle_start(message):
    text = 'Привет! Я могу предсказать цену на твою квартиру, если ты мне пришлешь данные о ней😎'
    bot.send_message(message.chat.id, text)
    text = 'Ты можешь заполнить этот файл, скинуть его мне, а я отправлю тебе цену твоей картины. Приступим!'
    bot.send_document(chat_id=message.chat.id, data=open(r'YourFlatData.xlsx', 'rb'), caption=text)


@bot.message_handler(commands=['help'])
def handle_start(message):
    text = 'Спешу на помощь!\nЯ работаю предельно просто: ты заполняешь прикрепленный файл данными своей квартиры, присылаешь этот файл мне, а я тебе говорю цену квартиры. Ничего сложного😊'
    bot.send_document(chat_id=message.chat.id, data=open(r'YourFlatData.xlsx', 'rb'), caption=text)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'C:\\Users\\ilyak\\PycharmProjects\\FlatCostPredictorBot\\' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        flat_data = read_data_from_doc(src)
        pred_cost = str(predict_flat_cost(flat_data))

        i = 1
        spaces_added = 0
        while i <= len(pred_cost):
            if (i - spaces_added) % 3 == 0:
                pred_cost = pred_cost[:-i] + ' ' + pred_cost[-i:]
                spaces_added += 1
                i += 1
            i += 1
        pred_cost = pred_cost.strip()

        bot.send_message(chat_id=message.chat.id,
                         text=f'По нашим оценкам, стоимость Вашей квартиры - приблизительно {pred_cost} рублей!')
    except Exception as err:
        print(err)
        bot.send_message(chat_id=message.chat.id,
                         text='Боюсь, файл, который Вы прислали, некорректный( Попробуйте внести данные своей квартиры в колонку "Ваши данные:", следуя примеру в столбце "Пояснение к полю:". Финальный файл должен иметь расширение .csv или .xlsx')


@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'text', 'location', 'contact', 'sticker'])
def handle_other_messages(message):
    bot.send_document(chat_id=message.chat.id,
                      data=open(r'YourFlatData.xlsx', 'rb'),
                      caption='Чтобы узнать цену своей квартиры, Вам нужно заполнить прикрепленный файл и прислать его мне')


bot.infinity_polling()
