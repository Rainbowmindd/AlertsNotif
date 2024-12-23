# Price Alert Bot

This project monitors the price of a specific product on the website [answear.com](https://answear.com/). It uses Selenium WebDriver for automating browsing and price checking, and sends an email notification when the price changes. The bot runs every hour to check for price changes and sends an email notification if the price has changed.

## Features

- Automatically checks the price of a product on **answear.com**.
- Sends an email notification when the price changes.
- Runs the checking process every hour.
- Saves the previous price in a text file for comparison.

## Requirements

- Python 3.6.9
- Selenium
- WebDriver Manager (to manage ChromeDriver)
- `schedule` to schedule periodic checks
- SMTP server data (e.g., Gmail account for email notifications)

### Required Python Libraries

To install the required libraries, use the following `pip` command:

```bash
pip install selenium schedule webdriver-manager
```

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/Rainbowmindd/AlertsNotif.git
   ```

2. **Configure email sending data**:
   - In the code, find the `send_email_notif` function and replace the `sender` and `password` variables with your email account details and password.
   - **Note**: If you're using Gmail, you might need to enable "Less secure apps" in your Google account settings or use an **App Password** for better security.

3. **Run the script**:
   - You can run the bot by using the following command:
     ```bash
     python3 main.py
     ```

4. The script will automatically open the browser, search for the specified product, and check the price. If the price has changed compared to the previous one, you will receive an email notification.

## How It Works

- The script opens the browser and navigates to [answear.com](https://answear.com/).
- It accepts the cookie policy and navigates to the **women's clothing** category.
- The bot then searches for a product named "Converse" (you can change this).
- After finding the product, it opens the product page, retrieves the current price, and compares it to the previous price saved in a file (`prices.txt`).
- If the price has changed, it sends an email notification with the price change details. If the price remains the same, it sends a notification stating that the price hasn't changed.
- The bot checks the price every hour and sends a new notification if the price has changed.

## Troubleshooting

If you encounter issues with the bot or have trouble sending email notifications, ensure that:

- Your email server (Gmail) is configured correctly with the right credentials.
- The `prices.txt` file exists in the same directory as the script and contains the previous price of the product (initially, the bot will create this file).
- If the bot fails to load the product page or find elements, check your internet connection or the website's structure, as it may have changed.
