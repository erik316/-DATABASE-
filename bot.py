import logging
import sqlite3
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from config import telegram_token, database
from db_manager import DB_Manager

# Apply nest_asyncio to allow nested use of asyncio.run
nest_asyncio.apply()

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize the database
db_manager = DB_Manager(database)
db_manager.create_tables()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! I am your bot.')

async def add_car(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 3:
        await update.message.reply_text('Usage: /add_car <car_brand> <color> <year>')
        return

    try:
        car_brand = context.args[0]
        color = context.args[1]
        year = int(context.args[2])
        
        if year < 1886 or year > 2024:  # Validate the year range
            await update.message.reply_text('Year must be between 1886 and 2024.')
            return

        with sqlite3.connect(database) as con:
            con.execute('INSERT INTO Car (car_brand, color, year) VALUES (?, ?, ?)', (car_brand, color, year))
        await update.message.reply_text(f'Car added: {car_brand}, {color}, {year}')
        logger.info(f'Car added: {car_brand}, {color}, {year}')
    except ValueError:
        await update.message.reply_text('Year must be an integer.')
        logger.error('ValueError: Year must be an integer.')
    except sqlite3.Error as e:
        await update.message.reply_text(f"An error occurred: {e}")
        logger.error(f"SQLite error: {e}")

async def delete_car(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 1:
        await update.message.reply_text('Usage: /delete_car <car_id>')
        return

    try:
        car_id = int(context.args[0])
        
        with sqlite3.connect(database) as con:
            result = con.execute('DELETE FROM Car WHERE car_id = ?', (car_id,))
            if result.rowcount == 0:
                await update.message.reply_text(f'No car found with car_id: {car_id}')
            else:
                await update.message.reply_text(f'Car with car_id {car_id} has been deleted.')
        logger.info(f'Car with car_id {car_id} deleted.')
    except ValueError:
        await update.message.reply_text('Car ID must be an integer.')
        logger.error('ValueError: Car ID must be an integer.')
    except sqlite3.Error as e:
        await update.message.reply_text(f"An error occurred: {e}")
        logger.error(f"SQLite error: {e}")

async def view_cars(update: Update, context: CallbackContext) -> None:
    try:
        with sqlite3.connect(database) as con:
            con.row_factory = sqlite3.Row
            cursor = con.execute('SELECT car_id, car_brand, color, year FROM Car')
            rows = cursor.fetchall()

        if rows:
            message = "Here are the cars in the database:\n\n"
            for row in rows:
                message += f"ID: {row['car_id']}, Brand: {row['car_brand']}, Color: {row['color']}, Year: {row['year']}\n"
        else:
            message = "No cars found in the database."

        await update.message.reply_text(message)
        logger.info('Cars viewed.')
    except sqlite3.Error as e:
        await update.message.reply_text(f"An error occurred: {e}")
        logger.error(f"SQLite error: {e}")

async def main() -> None:
    # Create the Application and pass it your bot's token
    application = Application.builder().token(telegram_token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_car", add_car))
    application.add_handler(CommandHandler("delete_car", delete_car))
    application.add_handler(CommandHandler("view_cars", view_cars))

    # Start the Bot
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())