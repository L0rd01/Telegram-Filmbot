import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup

# Устанавливаем токен бота
TOKEN = 'your_token_here'
bot = telegram.Bot(token=TOKEN)

# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я могу найти фильм по его коду. Введите код фильма, чтобы начать поиск.")

# Обработчик сообщений с текстом
def search_movie(update, context):
    # Получаем код фильма из сообщения пользователя
    code = update.message.text

    # Формируем URL-адрес сайта для поиска фильма
    url = f'https://www.kinopoisk.ru/index.php?kp_query={code}'

    # Получаем страницу с результатами поиска
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем название фильма на странице
    title_element = soup.find('div', {'class': 'element most_wanted'})
    if title_element is not None:
        title = title_element.find('div', {'class': 'name'}).text.strip()
        rating = title_element.find('span', {'class': 'rating_ball'}).text.strip()
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Название фильма: {title}, Рейтинг: {rating}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Фильм не найден")

# Создаем обработчики команд и сообщений
start_handler = CommandHandler('start', start)
search_handler = MessageHandler(Filters.text, search_movie)

# Добавляем обработчики в диспетчер сообщений
dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(search_handler)

# Запускаем бота
updater.start_polling()
updater.idle()