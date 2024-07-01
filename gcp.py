from google.cloud import storage

client = storage.Client()

print(client)


#upload file to gcp storage - blob = file
def list_buckets():
    buckets = client.list_buckets()
    for bucket in buckets:
        print(bucket.name)

def upload_blob(bucket_name, soruce_file_name, destination_blob_name):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(soruce_file_name)
    
    print('file sucsefully uploaded')


upload_blob('bkt-marvel','characters.csv','marvel_characters.csv')
