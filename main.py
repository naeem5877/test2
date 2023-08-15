import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = '6361667959:AAG-wlrZ33okHXHYTh-Myvs6lSPn0QoWuOU'

# Replace 'YOUR_GPLINK_API_KEY' with your actual GPLink API key
GPLINK_API_KEY = '6361667959:AAG-wlrZ33okHXHYTh-Myvs6lSPn0QoWuOU'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Movie Bot!")

def search_movie(update, context):
    query = update.message.text.split('/search ')[-1]
    movie_data = search_movie_api(query)
    if movie_data:
        movie_title = movie_data['title']
        movie_link = generate_download_link(movie_data['download_url'])
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Movie: {movie_title}\nDownload Link: {movie_link}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Movie not found.")

def search_movie_api(query):
    # Implement your movie search API logic here
    # This is just a placeholder function
    # You can replace this with your actual API integration code
    # Return movie data as a dictionary (e.g., {'title': 'Movie Title', 'download_url': 'https://example.com/movie'})
    # Return None if movie not found
    return None

def generate_download_link(movie_url):
    # Generate the download link using GPLink API
    gplink_url = f"https://gplinks.in/api?api={GPLINK_API_KEY}&url={movie_url}"
    response = requests.get(gplink_url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            return data['shortenedUrl']
    return movie_url

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    search_handler = MessageHandler(Filters.text & (~Filters.command), search_movie)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(search_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
