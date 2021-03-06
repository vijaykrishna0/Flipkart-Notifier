import requests
import urllib3
from bs4 import BeautifulSoup
from pyrogram import Client
import time
import sys
from __banner__.banner import banner
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


######## This is only for educational purpose ########
######## I'm not responsible for any loss or damage caused to you ########
######## using this script. ########
######## YOU ARE USING THIS SCRIPT ON YOUR OWN RISK ########

def ordinal(n):
    suffix = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']

    if n < 0:
        n *= -1

    n = int(n)

    if n % 100 in (11,12,13):
        s = 'th'
    else:
        s = suffix[n % 10]

    return str(n) + s

def main():
    sys.stdout.write(banner())

    time.sleep(0.8)
    ######## Add api_id and api_hash from my.telegram.org ########

    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }

    chk_list_urls = []
    no = 1
    input_an = True

    while input_an != False:
        inp_urls = input('Paste ' + ordinal(no) + ' url, When you are done adding urls input "next" to start script: ')
        no += 1
        if inp_urls != 'next':
            chk_list_urls.append(inp_urls)
        else:
            input_an = False

    if len(chk_list_urls) < 1:
        print('\nInput atleast one url to start')
    else:
        pincode = input('Enter Your Pincode: ')
        pincode_url = 'https://rome.api.flipkart.com/api/4/page/fetch'
        pincode_data = '{"pageUri":"' + chk_list_urls[0] + '","locationContext":{"pincode":"' + str(pincode) + '"},"pageContext":{"pageNumber":1,"fetchSeoData":true}}'
        
        r2 = requests.post(pincode_url, headers={'X-user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 FKUA/website/42/website/Desktop',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}, data=pincode_data, verify=False)
        
        try:       
            jss = r2.json()
            c_sn = jss['SESSION']['sn']
        except:
            print('Some error on server side')
            exit()

        head['Cookie'] = 'SN=' + c_sn
        last_l = len(chk_list_urls)
        while True:
            for index, url in enumerate(chk_list_urls):
                r = requests.get(url, headers=head, verify=False)
                soup = BeautifulSoup(r.content, 'html.parser')

                try:
                    if soup.find('button', class_ = '_2AkmmA _3-iCOr wvj5kH').text == 'NOTIFY ME':
                        title = soup.find('span', class_ = '_35KyD6').text
                        print(title + ' is oos')
                        if index == last_l - 1:
                            time.sleep(300)
                        # product is oos
                except:
                    try:
                        if soup.find('button', class_ = '_2AkmmA _2Npkh4 _2MWPVK').text == ' ADD TO CART':
                            title = soup.find('span', class_ = '_35KyD6').text
                            print(title + ' is in stock')
                            # print('in stock')
                            ######## SENDING A MESSAGE TO YOUR TELEGEGRAM ########
                            ######## Get below details from my.telegram.org ########

                            app = Client(
                                "tg_ac",
                                api_id=1234567, ######## YOUR API_ID ########
                                api_hash="xxxxxxxxxx" ######## YOUR API_HASH ########
                            )

                            msg = title + ' is in stock LINK - ' + url ######## You can customize this ########

                            with app:
                                app.send_message("your_tg_username", msg)  ######## Sending msg To @your_tg_username (set urs) ########
                                if index == last_l - 1:
                                    time.sleep(300)
                    except:
                        if soup.find('button', class_ = '_2AkmmA _2Npkh4 _2MWPVK _18WSRq')['disabled']:
                            print('disabled')

if __name__ == '__main__':
    main()