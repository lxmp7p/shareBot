import requests
import telebot
import re
import time
import sqlite3
import config
bot = telebot.TeleBot(config.token)

def connect_db():
	conn = sqlite3.connect('share.db')
	cur = conn.cursor()
	return cur, conn

@bot.message_handler(commands=['start'])
def start_message(message):
		bot.send_message(message.chat.id, "Добро пожаловать! \nС помощью данного бота вы можете осуществлять поиск необходимых курсов, которые были загружены участниками сообщества w2hack. \nДля добавление курса используйте команду /add 'URL' 'НАЗВАНИЕ' \nДля поиска курсов используйте команду /find 'НАЗВАНИЕ'.")


@bot.message_handler(commands=['add'])
def start_message(message):
	cur,conn = connect_db()
	words = []
	word = ''
	w = 0
	name_set = ""
	message.text += ' '
	for i in message.text:
		if (w == 0 or w == 1 ):
			if (i==" "):
				words.append(word)
				word = ''
				w += 1
			word += i
		else:
			name_set += i
	try:
		if (re.search(r'https:..*',words[1])):
			if (name_set!=""):
				cur.execute('INSERT INTO kurs(link,name,user_load,user_id_load) VALUES (?,?,?,?)', (words[1], name_set[:-1], message.chat.username, message.chat.id))
				conn.commit()
				bot.send_message(message.chat.id, "Курс добавлен!")
			else:
				bot.send_message(message.chat.id, "Вы забыли добавить название! \n Пример запроса: \n /add https://www.youtube.com/ Линукс для начинающих")
		else:
			bot.send_message(message.chat.id, "Проверьте ссылку!")
	except:
		bot.send_message(message.chat.id, "Неверный запрос!")

	cur.execute("SELECT rowid, link, name FROM kurs;")
	all_results = cur.fetchall()

@bot.message_handler(commands=['find'])
def start_message(message):
	cur,conn = connect_db()
	words = []
	word = ''
	message.text += ' '
	for i in message.text:
		if (i==" "):
			words.append(word)
			word = ''
		word += i
	try:
		name = words[1]
		name = name[1:]
		find_kurs = cur.execute('SELECT name,link FROM kurs WHERE name like ?' , ('%'+name+'%',))
		find = False
		for name,link in find_kurs:
			find = True
			if (find):
				bot.send_message(message.chat.id, 'Название курса: ' + name + '\nСсылка: ' +link)
		if (find == False):
			bot.send_message(message.chat.id, 'Ничего не найдено')
	except:
		bot.send_message(message.chat.id, "Неверный запрос!")

@bot.message_handler(commands=['statistic'])
def start_message(message):
	cur,conn = connect_db()
	count_kurs = cur.execute('SELECT COUNT(*) FROM kurs')
	bot.send_message(message.chat.id, 'Количество записей: ' + str(count_kurs.fetchall()))


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)

