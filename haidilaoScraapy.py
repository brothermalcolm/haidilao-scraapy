# scrape for all cities and store as json files in hourly buckets
import pandas as pd
import requests
import time
from datetime import datetime
import os

# get city list from local json file
CityList = pd.read_json('/Users/malcom/Downloads/getCityList.json')
cities = pd.DataFrame(data=CityList.data[0])

# create file directories
dateTimeObj = datetime.utcnow()
dateBucket = dateTimeObj.strftime("%Y-%m-%d")
hourBucket = dateTimeObj.strftime("%H")
path = '/Users/malcom/Downloads/haidilao/%s/%s/' % (dateBucket, hourBucket)
os.makedirs(path, exist_ok=True)
print(dateTimeObj)
print('creating %s' % path)

# make http post requests for all cities
url = 'https://superapp.kiwa-tech.com/app/v2/getStoreList'
for city in cities['cityId']:
    try:
        print('requesting %s store list...' % city)
        params = {"customerId": "",
                  "coordinate": "114.217261, 22.380012",
                  "cityId": city,
                  "regionId": "",
                  "sort": ""
                 }

        r = requests.post(url, json = params)
        outfile = '/Users/malcom/Downloads/haidilao/%s/%s/%s.json' % (dateBucket, hourBucket, city)
        fhand = open(outfile, 'x')
        fhand.write(r.text)
        fhand.close()
        time.sleep(5)
    except FileExistsError:
        pass
