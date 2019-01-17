import requests
import os

def download_sony_model():
    if not os.path.exists('model/Sony'):
        os.makedirs('model/Sony')

    print('Dowloading Sony Model (84Mb)')
    download_file_from_google_drive('1wmx7AM6XWHjHIvpErmIouQgbQoMxAymG', 'model/Sony/model.ckpt.data-00000-of-00001')
    download_file_from_google_drive('1OmrGMng1QuwUa8lf-_wBVvbRJwBr0ETr', 'model/Sony/model.ckpt.meta')

def download_sony_dataset():
    if not os.path.exists('dataset/Sony'):
        os.makedirs('dataset/Sony')

    print('Dowloading Sony subset... (25GB)')
    download_file_from_google_drive('10kpAcvldtcb9G2ze5hTcF1odzu4V_Zvh', 'dataset/Sony/Sony.zip')

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
