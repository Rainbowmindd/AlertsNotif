from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
import time
import schedule


from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

def read_previous_price():
    try:
        with open('prices.txt', 'r') as file:
            previous_price = file.read().strip()
            if previous_price=="":
                return None
            return float(previous_price)
    except FileNotFoundError:
        return None

def send_email_notif(message):

    sender="martyna.kindrat"
    receiver="martynatestowymail@gmail.com"
    password=""

    #SMTP
    server=smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)

    #msg
    msg=MIMEMultipart()
    msg['From']=sender
    msg['To']=receiver
    msg['Subject']="ANSWEAR NOTIFICATION MAIL"



    body=f"{message}"
    msg.attach(MIMEText(body, 'plain'))

    server.sendmail(sender, receiver, msg.as_string())
    server.quit()

def price_checker():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.get("https://answear.com/")

    WebDriverWait(driver, 1)

    try:
        WebDriverWait(driver,20).until(
            lambda d: d.execute_script("return document.readyState;")=="complete"
        )


        cookies_button = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"button[data-test='cookiesAcceptButton']"))
        )

        cookies_button.click()


        #waiting for "Ona" icon
        female_icon=WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"a[href='/c/ona'].CategoriesSection__menuLink__CrqSv"))
        )

        driver.execute_script("arguments[0].click();", female_icon)



        search_input=WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"input[data-test='search_input']"))

        )

        search_input.click()


        #another search input
        search_input_inner=WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"input[data-test='search_input']"))
        )

        search_input_inner.click()


        search_input_inner.send_keys("Converse")
        search_input_inner.send_keys(Keys.ENTER)



        #searching for the product
        found_item=WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"a[data-test='productItem']"))
        )

        found_item.click()


        #closing pop up
        pop_up_exit=WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'div[data-test="modal-close-button"]'))
        )

        pop_up_exit.click()


        #current price
        current_price=WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"span.ProductCard__percentageDiscountColorRed__Qm8Eg"))
        )

        str_current_price=float(current_price.text.replace("zł","").strip())
        print(f"Current price: {str_current_price} pln")

        previous_price=read_previous_price()

        if previous_price is not None:
            print(f"Previous price: {previous_price} pln")

            if str_current_price < previous_price:
                send_email_notif(f"Change of price from {str_current_price} pln to {previous_price} pln")
            else:
                send_email_notif("Price hasn't changed.")
        else:
            with open('prices.txt', 'w') as file:
                file.write(str(str_current_price))


    except TimeoutException:
        print("Loading took too long")

    finally:
        time.sleep(2)
        driver.close()

def scheduled_checker():
    schedule.every(1).hour.do(price_checker)

    while True:
        schedule.run_pending()
        time.sleep(1)
scheduled_checker()





