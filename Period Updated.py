import datetime
import requests
import json


from airtable import Airtable

my_key = 'keyuZ9jZifvOzDgPO'

base = 'appES8GEarVJWxjxC'

airtable_period = Airtable(base, 'Period',api_key=my_key)


URL = 'https://api.airtable.com/v0/'

withholding_base = 'https://api.airtable.com/v0/appES8GEarVJWxjxC/'

URL_period = withholding_base+'Period'+'?api_key='+my_key+'&sort[0][field]=Period'
period = requests.get(URL_period).json()

period_record = period['records']
# create_period = requests.post(URL_period).json()

date=datetime.datetime.now()
#DDMMYYY
dates  = date.strftime("%d")+" "+date.strftime("%b")+" "+date.strftime("%Y")
years_period = date.strftime("%Y-%m")

print(dates+': '+years_period)
print("Lated period: "+period_record[len(period_record)-1]['fields']['Period'])

if period_record[len(period_record)-1]['fields']['Period'] != years_period:
    airtable_period.insert({'Period':str(years_period)})



        
    
