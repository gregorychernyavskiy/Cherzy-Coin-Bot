import telegram
import asyncio
import os
from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()

chat_id = os.getenv('CHAT_ID', '7349055804')
bot_token = os.getenv('BOT_TOKEN', '7191322365:AAFj2ge-4Q1onaKqtAc3MPEc1QujYiOTuVM')
bot = telegram.Bot(token=bot_token)

symbols = {
    'Bitcoin': 'BTCUSDT_UMCBL',
    'Ethereum': 'ETHUSDT_UMCBL',
    'BNB': 'BNBUSDT_UMCBL',
    'Solana': 'SOLUSDT_UMCBL',
    'USD Coin': 'USDCUSDT_UMCBL',
    'XRP': 'XRPUSDT_UMCBL',
    'Dogecoin': 'DOGEUSDT_UMCBL',
    'Toncoin': 'TONUSDT_UMCBL',
    'Cardano': 'ADAUSDT_UMCBL',
    'Shiba Inu': 'SHIBUSDT_UMCBL'
}

async def fetch_price(session, symbol):
    marketprice = f'https://capi.bitget.com/api/mix/v1/market/ticker?symbol={symbol}'
    try:
        async with session.get(marketprice) as res:
            if res.status == 200:
                data = await res.json()
                if data and 'data' in data and 'last' in data['data']:
                    return float(data['data']['last'])
                else:
                    return 'Price data not available'
            else:
                return 'Failed to retrieve data'
    except Exception as e:
        return f'Error: {e}'

async def fetch_prices_and_send():
    async with ClientSession() as session:
        while True:
            message_lines = []

            for name, symbol in symbols.items():
                price = await fetch_price(session, symbol)
                if isinstance(price, float):
                    message_lines.append(f'{name}: ${price:,.8f}' if name == 'Shiba Inu' else f'{name}: ${price:,.2f}')
                else:
                    message_lines.append(f'{name}: {price}')

            message = '\n'.join(message_lines)
            print(message)

            try:
                await bot.send_message(chat_id=chat_id, text=message)
            except telegram.error.BadRequest as e:
                print(f"Failed to send message: {e}")

            await asyncio.sleep(60)  # Adjust the sleep time as needed

async def main():
    await fetch_prices_and_send()

if __name__ == '__main__':
    asyncio.run(main())