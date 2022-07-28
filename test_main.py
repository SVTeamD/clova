import asyncio
#import requests
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
    
<<<<<<< HEAD:test_main.py

def temp_replace_func(data):
    return data.replace(".","").replace(",","").replace(":","")

async def get_menu():
    # url = "http://image.auction.co.kr/itemimage/12/00/f4/1200f4a0f6.jpg"
    # clova = Clova()
    # x = await clova.ocr_transform(url) 
    # for data in x.data:
    #     lst.append(data.replace(".","").replace(",","").replace(":",""))

    temp_lst = ["짜장", "5,000", "짬뽕", "7000", "순두부", "6500", "제육볶음", "7300"]
    lst = [] -> 전체 데이터 저장 하는 배열
    price_lst = [] -> 가격 데이터 저장하는 배열 (인덱스 저장)


    for index, data in enumerate(temp_lst): 
        temp_var = temp_replace_func(data)

        lst.append(temp_var)
        if "00" in temp_var:
            price_lst.append(index)
    
    for x in price_lst:
        print(lst[x-1]) 
        print(lst[x])
        print("==========")

    
    # 형 변환
    

    # 코드 정리 (깔끔하게)
    # 값 -> menu 테이블에 넣어줘야 하니까 어떤식으로 넣어줄지!! (string, int)
    # 

asyncio.run(get_menu())


# 구현 순서
1. 전처리 (콤마/점/ 이런거 지우기) O
2. 전처리 된 데이터 배열에 저장 (1. 전체 저장 / 2. 가격 저장) O
3. 형변환 (가격만 정수형으로) 
4. DB에 저장하기 위해 넘겨줌

# 가게 간판까지 해야한다..!!
얘기 다시 해보기
=======



async def get_menu():
    url = "http://image.auction.co.kr/itemimage/12/00/f4/1200f4a0f6.jpg"
    clova = Clova()
    x = await clova.ocr_transform(url)  # url = s3버켓에 저장될 메뉴판 이미지 url
    lst = []
    for data in x.data: # 콤마 제거
        lst.append(data.replace(".","").replace(",","").replace(":",""))
    
    
    

    
    
    
    print(lst)
    print(x.status)
    print(x.message)
    print(x.data)

asyncio.run(get_menu())

# 삭제?

def temp_replace_func(data):
    return data.replace(".","").replace(",","").replace(":","")


temp_lst = ["짜장", "5,000", "짬뽕", "7000", "순두부", "6500", "제육볶음", "7300","500"]
lst = []
price_lst = []

for index, data in enumerate(temp_lst):
        temp_var  = temp_replace_func(data)

        lst.append(temp_var)
        if "00" in temp_var:
            price_lst.append(index)
for x in price_lst:
    if "00" not in lst[x-1]:
        print(lst[x-1])
        print(int(lst[x]))
        print("===============")

        


>>>>>>> b4f0a9419bb9e27b3ed216bc985818efc39bf1d8:main.py
