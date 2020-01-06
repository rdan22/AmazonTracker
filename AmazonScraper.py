#we can access a url and pull data from that website
import requests
#we can parse and pull out individual items
from bs4 import BeautifulSoup
#simple mail protocol that enables you to send emails
import smtplib

#what site we want to monitor
#not every website works with web-scraping...hopefully this works
URL = 'https://www.amazon.com/Superior-Apparel-Crewneck-Sweatshirt-Medium/dp/B01HVQPHL2/ref=asc_df_B01HVQSUAC/?tag=&linkCode=df0&hvadid=312710944255&hvpos=1o1&hvnetw=g&hvrand=13124844832366850520&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9026847&hvtargid=pla-569254071740&ref=&adgrpid=63891281642&th=1&psc=1'

#dictionary that gives some info about our browser
#can search for your user agent and paste it here
#Example user agent
headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

def check_price(): 
	#make the call that returns all the web page data
	page = requests.get(URL, headers = headers)

	#parse the data with beautiful soup
	#.com makes the html code with javascript. You can trick them with using 2 soups. 
	#Load soup1. Then load soup2 with soup1.prettify(). Then you got 
	#soup2 loaded correctly.
	soup1 = BeautifulSoup(page.content, 'html.parser')
	soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

	title = soup2.find(id="productTitle").get_text()
	price = soup2.find(id="priceblock_ourprice").get_text()

	#price is a string, need to modify it
	#checks first five
	converted_price = float(price[1:6])
		
	print(title.strip())
	print(price.strip())
	print(converted_price)

	if(converted_price < 10.00):
		send_mail()

def send_mail():
	#use gmail
	#simpler way: google allow less secure apps
	server = smtplib.SMTP('smtp.gmail.com', 587)
	#Extended HELO (EHLO) is an extended simple mail transfer protocol
	#sent by an email server to identify itself when connecting to another 
	#email server to start the process of sending an email
	#followed with sending email server's domain name
	server.ehlo()
	#encrypts our connection
	server.starttls()
	server.ehlo()
	
	server.login('johnnydavid167@gmail.com', 'my_password')

	subject = 'Price went down!'
	body = 'Check the amazon link: https://www.amazon.com/Superior-Apparel-Crewneck-Sweatshirt-Medium/dp/B01HVQPHL2/ref=asc_df_B01HVQSUAC/?tag=&linkCode=df0&hvadid=312710944255&hvpos=1o1&hvnetw=g&hvrand=13124844832366850520&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9026847&hvtargid=pla-569254071740&ref=&adgrpid=63891281642&th=1&psc=1'

	msg = f"Subject: {subject}\n\n{body}"

	server.sendmail(
		'johnnydavid167@gmail.com',
		'johnnydavid167@gmail.com',
		msg
	)
	print('Email has been sent.')
	server.quit()



check_price()

