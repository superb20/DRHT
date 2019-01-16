import requests
import os

def download_sony_model(dir_model):
    if not os.path.exists(dir_model):
        os.makedirs(dir_model)

    print('Dowloading Sony Model (84Mb)')
    download_file_from_google_drive('1wmx7AM6XWHjHIvpErmIouQgbQoMxAymG', dir_model + 'model.ckpt.data-00000-of-00001')
    download_file_from_google_drive('1OmrGMng1QuwUa8lf-_wBVvbRJwBr0ETr', dir_model + 'model.ckpt.meta')

def download_sony_dataset(dir_dataset):
    if not os.path.exists('dataset/Sony'):
        os.makedirs('dataset/Sony')

    print('Dowloading Sony subset... (25GB)')
    download_file_from_google_drive('10kpAcvldtcb9G2ze5hTcF1odzu4V_Zvh', dir_dataset + 'Sony.zip')
    os.system('unzip ' + dir_dataset + 'Sony.zip -d ' + dir_dataset)

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
