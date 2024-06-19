### Step-by-Step Guide for Your Project

#### Project Overview

This project involves creating a powerful bot using Python, which fetches real-time cryptocurrency prices and delivers them through Telegram. The bot is deployed on an AWS EC2 instance to ensure continuous operation, leveraging PuTTY and Ubuntu for setup and management.

---

### 1. **Project Description and Technologies Used**

1. **Telegram API**: Used to create and manage the bot that interacts with users.
2. **Crypto API**: Fetches real-time cryptocurrency prices.
3. **Python**: Programming language used to develop the bot.
4. **AWS EC2**: Cloud service used to deploy and run the bot 24/7.
5. **PuTTY**: SSH client used to manage the EC2 instance.
6. **Ubuntu**: Operating system used on the EC2 instance for running the bot.

---

### 2. **Setting Up the Telegram Bot**

#### 2.1. **Creating the Telegram Bot**

1. **Create a Telegram Bot**:
   - Open Telegram and search for "BotFather".
   - Start a chat with BotFather and use the command `/newbot` to create a new bot.
   - Follow the prompts to give your bot a name and username.
   - BotFather will provide you with a token. Save this token; you will need it later.

2. **Get Your Chat ID**:
   - Start a chat with your bot and send a message.
   - Visit `https://api.telegram.org/bot<YourBOTToken>/getUpdates` in a web browser, replacing `<YourBOTToken>` with your actual bot token.
   - Look for `"chat": {"id": <YourChatID>}` in the JSON response to find your chat ID.

#### 2.2. **Coding the Telegram Bot**

1. **Install Required Libraries**:
   ```sh
   pip install python-telegram-bot aiohttp python-dotenv
   ```

2. **Create the Python Script**:
   - Here is an example script:
     ```python
     import telegram
     import asyncio
     import os
     from aiohttp import ClientSession
     from dotenv import load_dotenv

     # Load environment variables
     load_dotenv()

     # Your Telegram credentials
     CHAT_ID = os.getenv('CHAT_ID', 'your-chat-id')
     BOT_TOKEN = os.getenv('BOT_TOKEN', 'your-bot-token')
     bot = telegram.Bot(token=BOT_TOKEN)

     # Crypto symbols
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
                     await bot.send_message(chat_id=CHAT_ID, text=message)
                 except telegram.error.BadRequest as e:
                     print(f"Failed to send message: {e}")

                 await asyncio.sleep(60)  # Adjust the sleep time as needed

     async def main():
         await fetch_prices_and_send()

     if __name__ == '__main__':
         asyncio.run(main())
     ```

3. **Store Environment Variables**:
   - Create a `.env` file in the same directory as your script with the following content:
     ```
     BOT_TOKEN=your-bot-token
     CHAT_ID=your-chat-id
     ```

4. **Create `requirements.txt`**:
   - List the dependencies in a `requirements.txt` file:
     ```
     python-telegram-bot==13.7
     aiohttp==3.8.1
     python-dotenv==0.19.2
     ```

---

### 3. **Fetching Cryptocurrency Prices with the Crypto API**

1. **API Endpoint**:
   - Use the `bitget` API to fetch cryptocurrency prices. The endpoint used in the script is `https://capi.bitget.com/api/mix/v1/market/ticker`.

2. **Fetching Data**:
   - The function `fetch_price(session, symbol)` in the script sends an asynchronous request to fetch the price for a given cryptocurrency symbol.

3. **Handling Data**:
   - The function processes the JSON response and extracts the relevant price data.

---

### 4. **Deploying the Bot on AWS EC2**

#### 4.1. **Creating an AWS Account**

1. **Sign Up for AWS**:
   - Visit [AWS](https://aws.amazon.com/) and create an account.

#### 4.2. **Launching an EC2 Instance**

1. **Open the EC2 Dashboard**:
   - In the AWS Management Console, navigate to EC2.

2. **Launch a New Instance**:
   - Click on "Launch Instance".
   - Choose an Amazon Linux 2 AMI (or Ubuntu).
   - Select an instance type (e.g., t2.micro for free tier).
   - Configure instance details and add storage.
   - Configure the security group to allow SSH (port 22).
   - Review and launch the instance.
   - Download the key pair (`.pem` file) and store it securely.

#### 4.3. **Connecting to Your EC2 Instance Using PuTTY**

1. **Convert the `.pem` File to `.ppk` Using PuTTYgen**

   - Open PuTTYgen.
   - Load your `.pem` file and save the private key as a `.ppk` file.

2. **Download and Install PuTTY**

   - Download PuTTY from [here](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) and install it.

3. **Connect Using PuTTY**

   - Open PuTTY.
   - Enter the Public DNS of your EC2 instance.
   - Navigate to `Connection -> SSH -> Auth` and browse for your `.ppk` file.
   - Click `Open` and log in as `ubuntu`.

#### 4.4. **Setting Up Your Environment on EC2**

1. **Update and Install Required Packages**:
   ```sh
   sudo apt update
   sudo apt install python3-pip git -y
   ```

2. **Clone Your GitHub Repository**:
   ```sh
   git clone https://github.com/your-username/CherzyCoinBot.git
   cd CherzyCoinBot
   ```

3. **Set Up Virtual Environment**:
   ```sh
   sudo apt install python3-venv -y
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

#### 4.5. **Running Your Script in a Screen Session**

1. **Install `screen`**:
   ```sh
   sudo apt install screen -y
   ```

2. **Start a Screen Session and Run Your Script**:
   ```sh
   screen
   python Cherzy_Coin_Bot.py
   # To detach from screen, press Ctrl + A, then D
   ```

#### 4.6. **Setting Up a Cron Job to Start on Reboot (Optional)**

1. **Edit the Crontab**:
   ```sh
   crontab -e
   ```

2. **Add the Following Line**:
   ```sh
   @reboot /home/ubuntu/CherzyCoinBot/venv/bin/python /home/ubuntu/CherzyCoinBot/Cherzy_Coin_Bot.py
   ```

---

### Conclusion

By following this guide, you will have successfully created a Telegram bot that fetches real-time cryptocurrency prices, deployed it on AWS EC2 for continuous operation, and managed the entire setup using PuTTY and Ubuntu. This comprehensive approach ensures that your bot runs reliably and efficiently, providing users with timely updates. If you have any questions or need further assistance, feel free to ask!
