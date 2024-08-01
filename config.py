import os

# Define the base directory as the current file's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the SQLite database file
database = os.path.join(BASE_DIR, 'database.db')

# Telegram bot token
telegram_token = '6546620115:AAGdbmi1dyqiJPinzHs8sRygOK6NMRILBBw'
