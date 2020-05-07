import requests
from time import sleep
import time
import schedule
import smtplib
from bs4 import BeautifulSoup

ProdID = ''
URL = "http://www.amazon.com/dp/" + ProdID

def check(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup.prettify(), "html.parser")
    product_title = soup2.find(id="productTitle").get_text()
    if soup2.find(id="availability") is not None:
        available = soup2.find(id="availability").get_text()
        if "stock" not in available:
            available = "Out of Stock"
    else:
        available = "Out of Stock"
    stock = available.strip()
    title_strip =product_title.strip()
    if soup2.find(id="price_inside_buybox") is not None:
        curprice = soup2.find(id="price_inside_buybox").get_text()
    else:
        curprice = "0"
    print("Current Availability status for " + title_strip + " is: " + stock)
    if curprice != "0":
        print("Current Price: " + curprice.strip())
    else:
        print("Current Price: Out of Stock")
    thresh = 0.00
    print("Our Price threshold is set to $" + str(thresh))
    if float(curprice.strip().strip("'").strip("$")) <= thresh and curprice != "0":
        print("Current Price is below our threshold, we're buying it.")
    else:
        print("Current Price is above our threshhold or it's out of stock, NOT buying.")
    return stock


def sendemail(result, product):
    GMAIL_U = "someone@gmail.com"
    GMAIL_P = "app-password-here"

    recipient = "sendto@gmail.com"

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    # start TLS for security
    s.starttls()
    s.ehlo()
    # Authentication
    s.login(GMAIL_U, GMAIL_P)

    # message to be sent
    subj = "It's in Stock on Amazon!"
    body = "Buy it here: " + URL
    msg = f"Subject: {subj}\n\n{body}"
    s.sendmail(GMAIL_U, recipient, msg)
    s.quit()


def ReadProd():
    print ("Processing: " + URL)
    result = check(URL)
    if "Out" not in result:
        print("In stock, Sending E-mail notification!")
        sendemail(result, ProdID)

def job():
    print("Running Again...")
    ReadProd()

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
