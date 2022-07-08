from bs4 import BeautifulSoup
import os,sys
import requests

class Weather():

	def getWeather(self):
		url="http://qq.ip138.com/weather/guangdong/ShenZhen.htm"
		print(url)
		 
		debug = {'verbose': sys.stderr}
		headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'}
		page = requests.get(url,headers=headers)
		page.encoding = 'utf-8'
		soup = BeautifulSoup(page.text, 'html.parser')

		title =  soup.find("h1")
		dates  =  soup.find_all("tr", class_="bg5")
		weathers = soup.find_all("tr",attrs={'class': None,'height':None})
		print(title.string)

		weather_list = []
		for date in dates:
			dateText = date.find("td").string
			weather_tuple = ()
			weather_tuple=weather_tuple+(dateText,"")
			weather_list.append(weather_tuple)
			print(dateText)

		idx=0
		for weather in weathers:
			weatherText = weather.text.rstrip().lstrip().replace("\n","   ")
			weather_tuple = weather_list[idx]
			weather_date  = weather_tuple[0]
			weather_tuple = (weather_date,weatherText)
			weather_list[idx] = weather_tuple
			print(weather_tuple)
			idx=idx+1

		weatherText = ""
		for w in weather_list:
			weatherTextOneRow = w[0]+" "+w[1]
			weatherText = weatherText + "\n"+weatherTextOneRow

		return weatherText