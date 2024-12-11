from bs4 import BeautifulSoup
import requests
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables
YOUR_SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")
YOUR_EMAIL = os.getenv("EMAIL_ADDRESS")
YOUR_PASSWORD = os.getenv("EMAIL_PASSWORD")

practice_url = "https://appbrewery.github.io/instant_pot/"
live_url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

response = requests.get(live_url, headers={
    'Accept-Language':'en-IN',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    })

html_content = response.text
print(html_content)
soup = BeautifulSoup(html_content, "html.parser")

# Get the product price and title
title = soup.find(id="productTitle").get_text().strip()
price_text = soup.find(class_="aok-offscreen").get_text()
price = float(price_text.strip()[1:])

# This is the threshold price below which I want to be notified
BUY_PRICE = 100

if price < BUY_PRICE:
    message = f"{title} is on sale for {price}!"
    print(message)
    
    try:
        with smtplib.SMTP(YOUR_SMTP_ADDRESS, port=587) as connection:
            connection.starttls()
            connection.login(YOUR_EMAIL, YOUR_PASSWORD)
            connection.sendmail(
                from_addr=YOUR_EMAIL,
                to_addrs=YOUR_EMAIL,
                msg=f"Subject: Amazon Price Alert!\n\n{message}\n{practice_url}".encode("utf-8")
            )
    except Exception as e:
        print(f"Error sending email: {e}")
