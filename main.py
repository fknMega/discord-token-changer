import requests
import string
import secrets



def generate_password(length=12):
    # genereate random password without : and @
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if ':' not in password and '@' not in password:
            break
    return password


# export email:pass:token from tokens.txt
def export_tokens():
    with open('combo.txt', 'r') as f:
        tokens = f.readlines()
    tokens = [x.strip() for x in tokens]
    return tokens

combo = export_tokens()



# get cookies from discord.com
def get_cookies(s):
    # send get request to discord.com
    # https://discord.com/channels/@me
    headers = {
    'Content-Type': 'application/json',
    'X-Discord-Locale': 'en-US',
    'X-Discord-Timezone': 'Asia/Jerusalem',
    'X-Debug-Options': 'bugReporterEnabled',
    'Origin': 'https://discord.com',
    'Connection': 'keep-alive',
    'Referer': 'https://discord.com/channels/@me',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.114 Safari/537.36',
    'JA3': '771,49162-49161-49160-159-158-107-106-105-104-103-64-63-62-61-60-53,0-29-23-24-25,0',
    'JA3S': 'ac598e3a3a9f2242de42c219be629cfd',
    }

    s.get('https://discord.com/channels/@me', headers=headers)




    
    



# change password and return new email:pass:token
def change_password(email, password, token):
    # make requests client
    s = requests.Session()

    # get cookies
    get_cookies(s)

    # login to discord.com
    # https://discord.com/channels/@me
    headers = {
    'Content-Type': 'application/json',
    'Authorization': token,
    'X-Discord-Locale': 'en-US',
    'X-Discord-Timezone': 'Asia/Jerusalem',
    'X-Debug-Options': 'bugReporterEnabled',
    'Origin': 'https://discord.com',
    'Connection': 'keep-alive',
    'Referer': 'https://discord.com/channels/@me',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.114 Safari/537.36',
    'JA3': '771,49162-49161-49160-159-158-107-106-105-104-103-64-63-62-61-60-53,0-29-23-24-25,0',
    'JA3S': 'ac598e3a3a9f2242de42c219be629cfd',
    }

    s.get('https://discord.com/channels/@me', headers=headers)
        
    

    # genereate random password
    new = generate_password()


    payload = {
        'password': password,
        'new_password': new,
    }
    try:
     r = s.patch('https://discord.com/api/v9/users/@me', headers=headers, json=payload)
     # get new token from r data
     new_token = r.json()['token']

     if r.status_code == 200:
         print(f'[{r.status_code}] Changed token for {email} to {new_token}')
         return f'1:{email}:{new}:{new_token}'
     else:
         print(f'[{r.status_code}] Failed to change token for {email}')
         return f'0:{email}:{password}:{token}'
    except Exception as e:
        print(f'Failed to change token for {email} due to {e}')
        return f'0:{email}:{password}:{token}'



def main():
    # loop through combo and change password
    for i in combo:
        # split combo into email, password, token
        email = i.split(':')[0]
        password = i.split(':')[1]
        token = i.split(':')[2]

        # change password and return new combo
        new_combo = change_password(email, password, token)

        # if newc_combo first var is 1, write to new file, if not write to failed.txt
        if new_combo.split(':')[0] == '1':
            with open('new_combo.txt', 'a') as f:
                f.write(new_combo.split(':')[1] + ':' + new_combo.split(':')[2] + ':' + new_combo.split(':')[3] + '\n')
        else:
            with open('failed.txt', 'a') as f:
                f.write(new_combo.split(':')[1] + ':' + new_combo.split(':')[2] + ':' + new_combo.split(':')[3] + '\n')

            

main()


