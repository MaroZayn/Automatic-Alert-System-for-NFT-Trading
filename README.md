# Automatic-Alert-System-for-NFT-Trading
## Overview
This project is an automatic alert system developed using Python and web scraping to monitor NFT (non-fungible token) projects. The system notifies users via a Telegram bot when the price of an NFT reaches a predefined threshold, helping users identify profitable trading opportunities in the digital asset space.

## Features
- **Real-time alerts**: Sends notifications to users when an NFT price hits the specified target.
- **Telegram integration**: Uses a Telegram bot to deliver price alerts directly to users.
- **Custom price thresholds**: Users can set custom price thresholds to get alerts for specific NFTs.
- **Web scraping**: Automatically scrapes data from various NFT platforms to track price changes in real-time.

## Technologies Used
- **Python**: Core programming language for the development of the system.
- **Web Scraping**: Utilized to collect real-time data on NFT prices.
- **Telegram Bot API**: To send automated alerts to users via Telegram.
- **Libraries**:
  - `BeautifulSoup` for web scraping.
  - `Requests` for HTTP requests.
  - `python-telegram-bot` for interacting with the Telegram API.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/MaroZayn/nft-alert-system.git
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Telegram bot:
    - Create a bot on [Telegram BotFather](https://core.telegram.org/bots#botfather).
    - Obtain your bot API token and add it to the `config.py` file.

4. Run the application:
    ```bash
    python app.py
    ```

## How It Works

1. **Data Scraping**: The system uses web scraping to fetch real-time NFT price data from specified NFT platforms.
2. **Price Monitoring**: The user sets predefined price thresholds. The system continuously monitors price fluctuations.
3. **Alert System**: When the price meets or surpasses the defined threshold, a notification is sent via the Telegram bot, providing users with timely information on profitable opportunities.

## Usage
- Set the desired NFT price threshold within the configuration.
- Use the Telegram bot to receive real-time alerts on price changes.

## Future Enhancements
- **Multiple NFT Platforms Support**: Expanding to track more NFT marketplaces.
- **User Management**: Adding multi-user support with personalized alert settings.
- **Enhanced Data Visualization**: Providing graphical representation of NFT price trends.

## Contributions
Feel free to contribute to this project by submitting issues or pull requests. Any improvements, bug fixes, or feature additions are welcome.
