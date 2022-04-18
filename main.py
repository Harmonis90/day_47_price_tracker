import requests
from bs4 import BeautifulSoup
from smtplib import SMTP
import config
TARGET_PRICE = 1000



product_url = "https://www.amazon.com/Apple-MacBook-14-inch-8%E2%80%91core-14%E2%80%91core/dp/B09JQL8KP9/ref=sr_1_2?crid=167PW2ACYG4BP&keywords=MKGR3LL%2FA&qid=1650242398&sprefix=mkgr3ll%2Fa%2Caps%2C323&sr=8-2"
HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"

}

response = requests.get(url=product_url, headers=HEADER)
response.raise_for_status()
site_data = response.text

soup = BeautifulSoup(site_data, "html.parser")
result_set = soup.select_one("#corePrice_feature_div .a-price-whole").get_text()

str_price = result_set.strip(".").replace(",", "")

try:
    price = int(str_price)
    if price <= TARGET_PRICE:
        with SMTP("smtp.gmail.com", port=587) as instance:
            instance.starttls()
            instance.login(user=config.FROM_ADDRESS, password=config.PASSWORD)
            instance.sendmail(from_addr=config.FROM_ADDRESS, to_addrs=config.TO_ADDRESS,
                              msg=f"Subject: New Price from Amazon!\n\n"
                                  f"The configured item is now below ${TARGET_PRICE} target price."
                                  f"\nBuy Now!"
                                  f"\nFrom,\n\t-Past Me")

            print("Successful")
    else:
        print("cannot connect")
except ValueError:
    print("Could not get a correct value for the current product.")
except IndexError:
    print("Can not find the current item. Please relocate it and use the new url.")




