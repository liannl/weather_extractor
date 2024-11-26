import requests
import pandas as pd

key = '9494b0bea8844870b61162453242511'
city = 'Moscow'
url = f'http://api.weatherapi.com/v1/current.json?key={key}&q={city}'

response = requests.get(url)
data = response.json()

result= pd.DataFrame(data)

if response.status_code == 200:

    print(result)
    # print(data['current']['temp_c'])
    # print(data['current']['condition']['text'])
else:
    print('Error {response.status_code}')