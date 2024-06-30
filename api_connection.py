import requests as r
import hashlib
import pandas as pd

developer = 'https://developer.marvel.com/docs#!/public/getCreatorCollection_get_0'

#how to protect public and private api key

public_api_key = 'x'
private_api_key = 'x'
ts = '1'
string_full = ts + private_api_key + public_api_key

# Generowanie hash w formacie heksadecymalnym
hash_done = hashlib.md5(string_full.encode()).hexdigest()

try:
    for i in range(0,4000,100):

        # Tworzenie żądania z poprawnymi parametrami
        url = f'http://gateway.marvel.com/v1/public/characters?limit=100&offset={i}&ts={ts}&apikey={public_api_key}&hash={hash_done}'
        response = r.get(url)
        status = response.status_code

        response = response.json()
        response = response['data']['results']
        
        if status == 200:

            data_full = []

            for item in response:
                diction = {}
                for key,values in item.items():
                    if not isinstance(values,dict) and key !='urls':
                        diction[key] = values
                    elif isinstance(values,dict) and 'available' in values:
                        diction[key] = values['available']
                data_full.append(diction)

            df = pd.DataFrame(data_full)

            df = df[['id', 'name', 'modified', 'comics','series', 'stories', 'events']]

            df.to_csv('characters.csv',mode='a',index=False,header=False)
        else:
            print('Something went wrong', print(status))
except KeyError:
    print('Ok to koniec ',i)
