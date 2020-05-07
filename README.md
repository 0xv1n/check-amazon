# checkamazon.py

Simple python script to automate the checking of whether or not an Amazon product is in stock, and to send me an e-mail if it's in stock and priced at or below a given price threshold.

Libraries Used:

* BeautifulSoup4 to parse the html
* schedule/time to prevent getting locked out by Amazon's API for request spamming
* smtplib to send myself encrypted e-mails.
