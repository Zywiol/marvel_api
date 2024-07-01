import requests as r
import hashlib
import pandas as pd
import dotenv
import os



developer = 'https://developer.marvel.com/docs#!/public/getCreatorCollection_get_0'

dotenv.load_dotenv()

public_api_key = os.getenv('PUBLIC_API_KEY')
private_api_key = os.getenv('PRIVATE_API_KEY')


ts = '1'
string_full = ts + private_api_key + public_api_key

# Generowanie hash w formacie heksadecymalnym
hash_done = hashlib.md5(string_full.encode()).hexdigest()

def api_response(public_api_key,ts,hash_done, end_point, limit=100,offset=0):
    url = f'http://gateway.marvel.com/v1/public/{end_point}?limit={limit}&offset={offset}&ts={ts}&apikey={public_api_key}&hash={hash_done}'
    response = r.get(url)
    status = response.status_code
    response = response.json()
    response = response['data']['results']
    return response,status

def download_characters():
    try:
        for i in range(0,4000,100):
            response_def = api_response(public_api_key,ts,hash_done,'characters',limit=100,offset=i)
            response = response_def[0]
            response_status = response_def[1]
        
            if response_status == 200:

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
                print('Something went wrong', print(response_status))
    except ConnectionError:
        print('Connection Error')
    except KeyError:
        print('Every characters has been downloaded',i)




def download_comics(character_id,limit=1,offset=0):

    response_def = api_response(public_api_key,ts,hash_done,f'characters/{character_id}/comics',limit=limit,offset=offset)
    response = response_def[0]
    response_status = response_def[1]
    print(response_status)

    data_full = []

    for item in response:
        diction = {}
        for key,value in item.items():
            if key in ['id','title','modified','format','pageCount']:
                diction['character_id'] = character_id
                diction[key] = value
        data_full.append(diction)

    data_full = pd.DataFrame(data_full)
    data_full.to_csv('comics.csv',mode='a',index=False,header=False)
    

characters = pd.read_csv('characters.csv')
characters = pd.DataFrame(characters)
characters_id = characters[['id','comics']]

df_comics = pd.read_csv('comics.csv')
df_cmoics_character_id = df_comics['character_id']

charater_id_temporary = 0
for index,row in characters_id.iterrows():
    charater_id_temporary = row['id']
    print(charater_id_temporary,' ','Ten juz istanieje, nie dodaje')
    if charater_id_temporary not in df_cmoics_character_id.values:
        print("Dodam teraz",' ',charater_id_temporary)
        if row['comics'] > 0:
            if row['comics'] < 100:
                data_full = download_comics(row['id'],limit=row['comics'])
            else:
                for i in range(0,row['comics'],100):
                    data_full = download_comics(row['id'],limit=100,offset=i)
                    if KeyError:
                        continue

