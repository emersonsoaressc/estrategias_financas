import telebot


CHAVE_API = "7197484389:AAFZdSidg5N5RQobjLKPK-Ra6ZT6bew6sSI"
bot = telebot.TeleBot(CHAVE_API)




def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    bot.reply_to(mensagem, "Olá Mundo!")











bot.polling()