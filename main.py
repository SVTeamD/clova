import asyncio
import requests
import uuid
import time
import json
import config
from urllib.request import urlopen 

class ResponseClova:
    status: bool
    message: str
    data: list

    def __init__(self, status: bool, message: str, data: list):
        self.status = status
        self.message = message
        self.data = data


class Clova:
    def __init__(self): # self = class Clova  ->> 네이버에 보내주는 형식 세팅
        self.request_json = { # 네이버 clova 요청 형식
            'images': [
                {
                    'format': 'jpg',
                    'name': 'demo',
                }
            ],
            'requestId': str(uuid.uuid4()),
            'version': 'V2',
            'timestamp': int(round(time.time() * 1000))
        }
        self.payload = {'message': json.dumps(self.request_json).encode('UTF-8')} # payload=데이터 / request_json 에 있는 형식을 payload에 담음
        self.headers = {
        'X-OCR-SECRET': config.SECRET_KEY
        }
 
    async def __request_clova_api(self, url: str):
        try:
            file = urlopen(url).read()
            files = [('file', file)]
            response = requests.request('POST', config.API_URL, headers=self.headers, data = self.payload, files = files)
            res = json.loads(response.text.encode('utf8'))
            return res
        except:
            return False

        
    async def ocr_transform(self, image_url: str):
        '''
        image_url : s3 이미지 url 경로
        return : {status: boolean, data: list}
        '''
        res = await self.__request_clova_api(image_url)
        data = []

        # check s3 image url validate
        if not res:
            message = 's3 image url not validate'
            return ResponseClova(False, message, data)

        # check api_url validate
        if 'error' in res:
            return ResponseClova(False, res['error']['message'], data)

        # check secret_key
        if 'code' in res and res['code'] == '0002':
            return ResponseClova(False, res['message'], data)

        for field in res['images'][0]['fields']:
            data.append(field['inferText'])

        return ResponseClova(True, res['images'][0]['message'], data )


    #async def preprocessing(self):
         # 1. , 없애주는 기능 -완료
        #transformed_string = get_menu.x.data.replace(",","")
        #print(transformed_string)
        # 2. 홀/짝 구분
        # 3. 글자~~~~~숫자까지
        #4. int형 바꾸기
    



async def get_menu():
    url = "http://image.auction.co.kr/itemimage/12/00/f4/1200f4a0f6.jpg"
    clova = Clova()
    x = await clova.ocr_transform(url) 
    lst = []
    for data in x.data:
        lst.append(data.replace(".","").replace(",","").replace(":",""))
    

    
    
    
    
    
    #print(lst) -> 이거
    #print(x.status)
    #print(x.message)
    #print(x.data)

asyncio.run(get_menu())



