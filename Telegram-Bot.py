from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import os
import csv


file_name = 'Pizza.csv'
headers = ['pizza', 'size', 'price'] 


pizza_quantity = 'pizza_quantity.csv'
headers1 = ['pizza', 'size', 'price', 'quantity']

pizzas = [
        ['Margarita', 'small', '135',10],
        ['Margarita', 'medium', '200',10],
        ['Margarita', 'big', '315',10],


        ['Gavayska', 'small', '135',10],
        ['Gavayska', 'medium', '200',10],
        ['Gavayska', 'big', '315',10],


        ['Sicilian', 'small', '135',10],
        ['Sicilian', 'medium', '200',10],
        ['Sicilian', 'big', '315',10]
    ]  

# створює файл з поатковими даними
def created_pizza():
    global file_name, headers
    pizza = [
        ['Margarita', 'small', '135'],
        ['Gavayska', 'medium', '200'],
        ['Sicilian', 'small', '155']
    ]  

    with open(file_name, 'w', encoding='UTF8', newline='') as p:
        writer = csv.writer(p)
        writer.writerow(headers)
        writer.writerows(pizza)


def created_pizza_quantity():
    global pizza_quantity, headers1
    global pizzas

    with open(pizza_quantity, 'w', encoding='UTF8', newline='') as pq:
        writer = csv.writer(pq)
        writer.writerow(headers1)
        writer.writerows(pizzas)


created_pizza_quantity()
# відповідь на неіснуючу команду боту
def error_input(update, context):
    message = '''Введеної команди немає:
    /help - для перегляду доступних команд'''
    update.message.reply_text(message)



# обробка команди /start
def start(update, context):
    global file_name
    message = '''Вас вітає бот-піцерія:
    /help - для перегляду доступних команд'''

    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text = message)



# обробка команди /help
def bot_commands(update, context):   
    message = '''Основні команди [та їх параметри]:
        /posters_list - перегляд фільмів в прокаті
        /buy_pizza - замовити піццу
        /posters_remove [назва] - зняти фільм з прокату'''

    chat = update.effective_chat
    context.bot.send_message(chat_id = chat.id, text = message) 


def buy_pizza(update, context):
    global file_name, headers

    buy_pizza = update.message.text
    buy_pizza = buy_pizza.split()
    pizza = dict()
    pizza['pizza'] = buy_pizza[1]
    pizza['size'] = buy_pizza[2]
    pizza['price'] = buy_pizza[3]


    with open('pizza_quantity.csv', 'r', encoding='UTF8',) as pq1:
        reader = pizzas
        for i in reader:
            if buy_pizza[1] and buy_pizza[2] in pizzas:
                message1 = '''Піцца успішно замовлена, чекайте на дзвінок!'''

                chat = update.effective_chat
                context.bot.send_message(chat_id=chat.id, text = message1) 

            else:
                message="Такої піцци не існує"
                chat = update.effective_chat
                context.bot.send_message(chat_id=chat.id, text = message) 
                break
            x = i.index(buy_pizza[1]) + 3
            pizza_quantity = list()
            y = pizza_quantity.pop(x)
            if y>0:
                with open(file_name, 'a', encoding='UTF8', newline='') as file:
                    writer = csv.DictWriter(file, headers)
                    writer.writerow(pizza)

                message1 = '''Піцца успішно замовлена, чекайте на дзвінок!'''

                chat = update.effective_chat
                context.bot.send_message(chat_id=chat.id, text = message1) 
            

            else:
                message="Такої піцци не має в наявності"
                chat = update.effective_chat
                context.bot.send_message(chat_id=chat.id, text = message) 


    chat = update.effective_chat
    context.bot.send_message(chat_id = chat.id, text = message) 



#створюємо класи для взаємодії з ботом
updater = Updater("5032733497:AAFUZOMYInbUpq5ZRQ2rsGBU3KES6t6Uia8")
dispatcher = updater.dispatcher

#створюємо обробники подій (команд)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", bot_commands))
dispatcher.add_handler(CommandHandler("buy_pizza", buy_pizza))

#все, що не потрапляє в команди бота
dispatcher.add_handler(MessageHandler(Filters.all, error_input))


updater.start_polling()
updater.idle()