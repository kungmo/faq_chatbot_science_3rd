import urllib.request
import ssl
import json

def request(url):
    """지정한 url의 웹 문서를 요청하여, 본문을 반환한다."""
    response = urllib.request.urlopen(url)
    byte_data = response.read()
    text_data = byte_data.decode()
    return text_data

TOKEN = '1329952861:AAHduDQniVQxEkaeKLE-H0OETnNGkqS_zpk'

def build_url(method, query):
    """텔레그램 챗봇 웹 API에 요청을 보내기 위한 URL을 만들어 반환한다."""
    return f'https://api.telegram.org/bot{TOKEN}/{method}?{query}'

# print(build_url('getMe', ''))

context = ssl._create_unverified_context()
response = urllib.request.urlopen(build_url('getMe', ''), context=context)

#response = request(build_url('getMe', ''))

json.loads(str(response))