
from splinter import Browser
import json
import urllib
import requests


#callback URL is found at https://developer.tdameritrade.com/user/me/apps/Details after you create an app
callback_url = input(str(r'Enter Your Callback Url: eg. http://localhost:8080/ : '))

# consumer key is found at https://developer.tdameritrade.com/user/me/apps/Keys after you create an app
consumer_key = input(str(   'Enter Your Consumer Key : '))

#r"C:\Users\YOUR USERNAME\Desktop\chromedriver_win32\chromedriver"
path_to_chromedriver = input('Enter Path to Chromedriver: REMEMBER /chromedriver at the end')

# set the executable path to the Chrome Driver found at https://chromedriver.chromium.org/. 
executable_path = {'executable_path': path_to_chromedriver}

# make instance of the browser
browser = Browser('chrome', **executable_path, headless=False)


# Define the url get request
method = "GET"
url = "https://auth.tdameritrade.com/auth?"
client_code = consumer_key + '@AMER.OAUTHAP'
payload = {'response_type': 'code', 'redirect_uri': callback_url, 'client_id':client_code}

# building the URL
built_url = requests.Request(method, url, params=payload).prepare()
built_url = built_url.url
#starting the browser with the URL
browser.visit(built_url)

# making input to make sure the browser is loaded
input('Press Enter To Continue')

#getting the return url with the code returned in it.
new_url = browser.url

# Parse the URL to get the code.
parse_url = urllib.parse.unquote(new_url.split('code=')[1])

# Closing the Browser 
browser.quit()

#creating a json file to store the code
codes = {'code':parse_url,
        'callback_url':callback_url,
        'customer_key': consumer_key}

# creating a config json file to store the calback_URL, Customer_key
with open('config.json', 'w') as f:
    json.dump(codes, f, indent=2)

#setting the code to the first acces code to get auth_token
code = codes['code']
print(code)

# URl for the auth token https://developer.tdameritrade.com/authentication/apis/post/token-0
url = url = r'https://api.tdameritrade.com/v1/oauth2/token'
# 
headers = {'Content_Type':"application/x-www-form-urlencoded"}
data = {'grant_type':'authorization_code',
            'access_type': 'offline',
            'code': code,
            'client_id': consumer_key,
            'redirect_uri':callback_url}


#post the data to get the token
authReply = requests.post(url, headers= headers, data= data)
decode_content = authReply.json()


with open('auth_token.json', 'w') as f:
    json.dump(decode_content, f, indent=2)








