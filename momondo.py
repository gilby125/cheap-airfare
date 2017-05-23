import bs4 as bs 	# beautiful soup
import urllib.request
import time

urlFull = 'http://cfse.momondo.com/flightsearch/?Search=true&TripType=1&SegNo=1&SO0=NYC&SD0=TLV&SDP0=20-06-2017&AD=1&TK=ECO&DO=false&NA=false'
urlA = 'http://cfse.momondo.com/flightsearch/?Search=true&TripType=1&SegNo=1&SO0=NYC&SD0=TLV&SDP0='
urlB = '-06-2017&AD=1&TK=ECO&DO=false&NA=false'

from operator import itemgetter
from selenium import webdriver
from multiprocessing import Pool

def scraper(day):
	url = urlA + str(day) + urlB
	print('Opening browser window...')
	browser = webdriver.Chrome()		# for debugging - opens a browser window
	#browser = webdriver.PhantomJS()		# to run the real thing (browser windows don't open)
	browser.get(url)
	print("Loading website and waiting...")
	time.sleep(40)
	print("Scraping NOW")
	soup = bs.BeautifulSoup(browser.page_source, 'html5lib')
	browser.close()
	print(str(day) + " June 2017:")
	flight_arr = daily_flights(soup)
	#print(flight_arr)				# will print all flights found
	printed_notification(soup)
	ans = flight_selector(flight_arr)
	print("For the {} of June, these are the best flights:".format(day)) 
	for i in ans:
		print(i)
	print()

def daily_flights(soup):
	flights = []
	travel_times = []
	prices = []
	stops = []
	ratings = []
	airport = []
	ans = []
	for item in soup.find_all("div", class_="names"):
		flights.append(item.text)

	for item in soup.find_all("div", class_="travel-time"):
		travel_times.append(item.text)

	for item in soup.find_all("div", class_="floater"):
		prices.append(item.span.text)

	for item in soup.find_all("span", class_="total"):
		stops.append(item.text)

	for item in soup.find_all("div", class_="departure"):
		airport.append(item.span.text)

	for item in soup.find_all("div", class_="rating"):
		ratings.append(item.span.text)

	for i in zip(prices, flights, travel_times, stops, ratings, airport):
		ans.append(i)

	return ans

def printed_notification(soup):
	temp = soup.find("div", class_="progress")
	try:
		flights_found = temp.b.text 				# number of flights found
	except:
		flights_found = 1111
	temp = soup.find("div", class_="top")
	complete = temp.text 						# returns "Search complete" if complete.
	print("{} flights found; {}".format(flights_found, complete))

def flight_selector(arr):
	prices = []
	times = []
	stops = []
	for i in arr:
		if len(i[2]) == 7: times.append(int(i[2][:2]))
		else: times.append(int(i[2][0]))
		if i[3] == 'Non-stop': stops.append(0)
		else: stops.append(int(i[3][0]))
		if len(i[0]) == 7: prices.append(int(i[0][:3]))
		else: prices.append(999)
		times = sorted(times)
		stops = sorted(stops)
		prices = sorted(prices)
	time_standard = times[2]
	stop_standard = stops[1]
	prices_standard = prices[2]

	good_flights = []
	for i in arr:
		if len(i[2]) == 7: hours = int(i[2][:2])
		else: hours = int(i[2][0])
		
		if i[3] == 'Non-stop': flight_stops = 0
		else: flight_stops = int(i[3][0])
				
		if len(i[0]) == 7: price = int(i[0][:3])
		else: price = 999
		
		temp = 0
		if hours <= time_standard: temp += 1
		if hours >= 20: temp -= 1
		if flight_stops <= stop_standard: temp += 1
		if price <= prices_standard: temp += 1
		if temp >= 2: good_flights.append(i)

	return good_flights


if __name__ == "__main__":
	p = Pool(processes=9)
	data = p.map(scraper, [20, 21, 22, 23, 24, 25, 26, 27, 28])
	#scraper(20)
	print('*********Good Flights************')
	#print(data)
	#print('*********************************')
	#p.close()



# TO DO list:
# - easier interface
# - select best flight out of list based on my common sense
# - figure out a way to run this without opening new Chrome windows (V)
# - run script every 10 minutes and save results
# - 