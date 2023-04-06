import numpy as np


from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime

# fecha y nombre del archivo



more = True

name_csv = '../output/data.csv'

more_pages = True
page = 1

columns = ['date', 'grade', 'name', 'station']
df = pd.DataFrame(columns=columns)

while more_pages == True:
	print(page)
	if page == 1:
		url_name = "https://www.carabineros.cl/detalleMemorial.php"
	else:
		url_name = "https://www.carabineros.cl/detalleMartir.php?pagina=" + str(page)

	url = requests.get(url_name)


	soup = BeautifulSoup(url.text, "html.parser")


	profiles = soup.find_all("div", attrs={"class": "card-content-index"})
		       



	for profile in profiles:
		grade = profile.findChildren('h2')[0].get_text()
		name = profile.findChildren('h1')[0].get_text()
		date = profile.findChildren('strong')[0].get_text()
		station= profile.findChildren('strong')[1].get_text()
		
		date = date.replace('-','').replace(' ', '')
		day = int(date[:2])
		month = int(date[2:4])
		year = int(date[4:8])
		
		date = datetime.datetime(year, month, day)
		new_row = {
		"date": date,
		"grade": grade,
		"name": name,
		"station": station}
		
		df = pd.concat([df, pd.DataFrame([new_row])], axis=0, ignore_index=True)
		print(df)
	if profiles == []:
		more_pages = False
	page += 1


df.to_csv(name_csv, index=False)
