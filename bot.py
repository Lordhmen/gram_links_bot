from aiogram import types
from aiogram.types import WebAppInfo
from aiogram.utils import executor
import sqlite3
from config import dp, bot

DATABASE_NAME = "users_bd"


def create_database():
    conn = sqlite3.connect(f"{DATABASE_NAME}.sqlite")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, username TEXT, first_name TEXT)''')
    conn.commit()
    conn.close()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Получаем информацию о пользователе
    user_id = str(message.from_user.id)
    username = message.from_user.username
    first_name = message.from_user.first_name

    # Подключаемся к базе данных
    conn = sqlite3.connect(f"{DATABASE_NAME}.sqlite")
    cursor = conn.cursor()

    # Проверяем, есть ли пользователь в базе данных
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        # Добавляем пользователя в базу данных
        cursor.execute("INSERT INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
                       (user_id, username, first_name))
        conn.commit()

    # Закрываем соединение с базой данных
    conn.close()
    keyboard = types.InlineKeyboardMarkup()

    gram_base_button = types.InlineKeyboardButton(text="Gram Base", url="https://t.me/grambase")
    gram_chat_button = types.InlineKeyboardButton(text="Gram Chat", url="https://t.me/tonbasechat")
    gram_community_button = types.InlineKeyboardButton(text="Gram Community", url="https://t.me/gramcommunity")
    gram_official_button = types.InlineKeyboardButton(text="Gram Official", url="https://t.me/gramcoinorg")
    purchase_exchange_button = types.InlineKeyboardButton(text="Purchase and exchange",
                                                          callback_data="purchase_exchange")
    liquidity_pool_button = types.InlineKeyboardButton(text="Liquidity pool", callback_data="liquidity_pool")
    gram_mining_button = types.InlineKeyboardButton(text="Gram Mining", callback_data="gram_mining")
    gram_dns_button = types.InlineKeyboardButton(text="Gram DNS", web_app=WebAppInfo(url="https://dns.gramcoin.org/"))

    keyboard.add(gram_base_button, gram_chat_button)
    keyboard.add(gram_community_button, gram_official_button)
    keyboard.add(purchase_exchange_button, liquidity_pool_button)
    keyboard.add(gram_mining_button, gram_dns_button)

    await message.answer("Navigation menu", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'back_to_menu')
async def back_to_menu_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await start_command(callback_query.message)


@dp.callback_query_handler(lambda c: c.data == 'purchase_exchange')
async def purchase_exchange_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    keyboard = types.InlineKeyboardMarkup()

    cryptobot_button = types.InlineKeyboardButton(text="CryptoBot", url="https://t.me/CryptoBot?start=market")
    mexc_button = types.InlineKeyboardButton(text="Mexc", url="https://www.mexc.com/ru-RU/exchange/GRAM_USDT")
    bitget_button = types.InlineKeyboardButton(text="BitGet", url="https://www.bitget.com/spot/GRAMUSDT")
    stonfi_button = types.InlineKeyboardButton(text="Ston.FI", web_app=WebAppInfo(
        url="https://app.ston.fi/swap?chartVisible=false&ft=TON&fa=1&tt=GRAM"))
    dedust_button = types.InlineKeyboardButton(text="DeDust", web_app=WebAppInfo(url="https://dedust.io/swap/TON/GRAM"))
    ton_diamonds_button = types.InlineKeyboardButton(text="TON Diamonds", web_app=WebAppInfo(
        url="https://ton.diamonds/dex/swap?inputToken=TON&outputToken=GRAM"))
    ton_planets_button = types.InlineKeyboardButton(text="TON Planets", web_app=WebAppInfo(
        url="https://mars.tonplanets.com/en/dex/?from=TON&to=EQC47093oX5Xhb0xuk2lCr2RhS8rj-vul61u4W2UH5ORmG_O"))
    back_button = types.InlineKeyboardButton(text="Back to Menu", callback_data="back_to_menu")

    keyboard.add(cryptobot_button)
    keyboard.add(mexc_button, bitget_button)
    keyboard.add(stonfi_button, dedust_button)
    keyboard.add(ton_diamonds_button, ton_planets_button)
    keyboard.add(back_button)
    await callback_query.message.answer("Choose an option:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'liquidity_pool')
async def liquidity_pool_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    keyboard = types.InlineKeyboardMarkup()

    stonfi_button = types.InlineKeyboardButton(text="Ston.FI", web_app=WebAppInfo(
        url="https://app.ston.fi/liquidity/provide?ft=GRAM&tt=TON"))
    stonfi_instructions_button = types.InlineKeyboardButton(text="Instructions",
                                                            url="https://guide.ston.fi/ru/kak-postavit-likvidnost-na-ston.fi")
    dedust_button = types.InlineKeyboardButton(text="DeDust", web_app=WebAppInfo(
        url="https://dedust.io/pools/EQAZZXXhnoNGCzIlSKYqY4vL-hHqdIAuNQXEgqMKg-CYCs1u/deposit"))
    dedust_instructions_button = types.InlineKeyboardButton(text="Instructions",
                                                            url="https://telegra.ph/Dobavlenie-v-pul-likvidnosti-DeDustio-03-02")
    back_button = types.InlineKeyboardButton(text="Back to Menu", callback_data="back_to_menu")

    keyboard.add(stonfi_button, stonfi_instructions_button)
    keyboard.add(dedust_button, dedust_instructions_button)
    keyboard.add(back_button)

    await callback_query.message.answer("Choose an option:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'gram_mining')
async def gram_mining_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    keyboard = types.InlineKeyboardMarkup()

    gram_mining_site_button = types.InlineKeyboardButton(text="Site",
                                                         web_app=WebAppInfo(url="https://pool.gramcoin.org/"))
    gram_mining_news_button = types.InlineKeyboardButton(text="News", url="https://t.me/GramMiningPool")
    gram_mining_chat_button = types.InlineKeyboardButton(text="Chat", url="https://t.me/GramMiningChat")
    back_button = types.InlineKeyboardButton(text="Back to Menu", callback_data="back_to_menu")

    keyboard.add(gram_mining_site_button)
    keyboard.add(gram_mining_news_button, gram_mining_chat_button)
    keyboard.add(back_button)

    await callback_query.message.answer("Choose an option:", reply_markup=keyboard)


async def startup(dp):
    create_database()
    print("Бот запущен!")


async def shutdown(dp):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
