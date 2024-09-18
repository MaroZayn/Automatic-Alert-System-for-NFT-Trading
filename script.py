# import all the modules that we will need
import re
import requests  
from bs4 import BeautifulSoup  
import csv     
import time
import json 
from time import sleep
from random import randint

# the page that we gonna request data from
page = requests.get("https://howrare.is/drops")
# define the main function that gonna containe all the functions
def main(page):  

    src = page.content                             #get the content of page and save it on src
    soup = BeautifulSoup(src, "html.parser")       #get the HTML code using "html.parser" 

    project_details = []           #a liste of dictionnary for all the projects
    project_details_10K_only = []  #a liste of dictionnary for the interesting projects

    dates = soup.find_all("div", {'class':'table_wrap'})  #get all the dates   
    
    def get_project_info(dates):       #first function to get the project info for each date

        date_details = dates.contents[1].text.strip()  #get the date for each project (found on the second element of content)
        
        all_projects = dates.contents[3].find_all('tr')            #all project is a liste each tr correspond to a project, except the first one
        
        all_project = all_projects[1:]     # get just the projects  
        
        number_of_projects = len(all_project)   # the number of projects
        
        for i in range(number_of_projects):  # go throw each project
            
            # get projects names
            projects_names = all_project[i].find('div',{'class': 'tab_collection'}).text.strip() 
            # get Twitter username
            projects_link = all_project[i].find('div',{'class': 'links'})
            for link in projects_link.find_all('a'):          # all the links
                link = link.get('href')                      #get a specific link
                if 'twitter' in link:
                    twitter = str(link)[20:]
            # get project details        
            details = all_project[i].find_all('td')
            # get the supply
            count = details[1].text.strip()
            # get the price
            price = details[2].text.strip() 
            
            
            # FOllowers Scraper from bing
             
            # creating custom bing url 
            target_url = "https://www.bing.com/search?q=site%3Atwitter.com+"+twitter#+"&qs=HS&sk=HS3&sc=10-0&cvid=DF487E35E8A64AD9B1A579B843491E40&FORM=QBLH&sp=4&lq=0"
            # headers that will be used in making request
            
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
                'cache-control': 'max-age=0',
                'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
            }

            # making bing resquest for getting results/followers 
            resp = requests.get(target_url,headers=headers)
            
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            twitter_followers = ''
            try:
                try:
                    # TRY 1
                    # Scraping only twitter followers 
                    #creating custom element finder for that specific twitter account
                    ELEment = 'a[href*="twitter.com/'+twitter+'"]'
                    # getting first result having twitter link and getting followers from that element
                    bing_Result = soup.select(ELEment)[0]
                    bing_Result = bing_Result.parent.parent
                    bing_Result_E = bing_Result
                    if 'Followers:' in str(bing_Result_E):
                        # getting twitter followers
                        twitter_followers = str(str(str(str(bing_Result))).split('Followers:</strong>')[1].split('<')[0])
                except:
                    # TRY 2
                    # Scraping only twitter followers 
                    #creating custom element finder for that specific twitter account
                    ELEment = 'a[href*="twitter.com/'+twitter.lower()+'"]'
                    # getting first result having twitter link and getting followers from that element
                    bing_Result = soup.select(ELEment)[0]
                    bing_Result = bing_Result.parent.parent
                    bing_Result_E = bing_Result
                    if 'Followers:' in str(bing_Result_E):
                        # getting twitter followers
                        twitter_followers = str(str(str(str(bing_Result))).split('Followers:</strong>')[1].split('<')[0])
                        
            except:
                twitter_followers = ''
            
            if twitter_followers == '':
                # Scraping followers if not scraped using twitter link find element
                # checking only the element without sepcifing twitter 
                try:
                    # Try 1
                    ELEment = 'div[class="b_factBlock"]'
                    # getting followers from that element
                    bing_Result = soup.select_one(ELEment)
                    twitter_followers = str(bing_Result).split('Followers</strong>:</strong>')[1].split('<')[0]
                    
                except:
                    try:
                        # Try 2
                        ELEment='div[class="b_vlist2col"]'
                        # getting followers from that element
                        twitter_followers = str(soup.select_one(ELEment)).split('Followers:')[1].split('<')[0]   
                    except:
                        twitter_followers = ''
            try:
                if twitter_followers[0] == ' ':
                    twitter_followers = twitter_followers[1:]
            except:
                pass
                    
            # add project info to the var project_details
            print(target_url)
            print({"    day     ":date_details,"   project name    ":projects_names,"    price    ":price,"   supply     ":count," Twitter Username":twitter," Twitter Followers":twitter_followers})
            project_details.append({"    day     ":date_details,"   project name    ":projects_names,"    price    ":price,"   supply     ":count," Twitter Username":twitter," Twitter Followers":twitter_followers})
            
            # Filtering accounts having more then 10K data.
            try:
                if twitter_followers != '':
                    if '.' in twitter_followers:
                        twitter_followers_I = twitter_followers.replace('K','00').replace('.','')
                    if '.' not in twitter_followers:
                        twitter_followers_I = twitter_followers.replace('K','000').replace(',','')
                    try:
                        twitter_followers_I=int(twitter_followers_I)
                    except:
                        twitter_followers_I=int(twitter_followers_I.replace(' ',''))
                    if twitter_followers_I >= 10000:       #if it didnt work try 100000
                        project_details_10K_only.append({"    day     ":date_details,"   project name    ":projects_names,"    price    ":price,"   supply     ":count," Twitter Username":twitter," Twitter Followers":twitter_followers})
                
            except:
                pass
         
    for i in range(len(dates)):      # go throw all the dates  
        (get_project_info(dates[i]))
    keys = project_details[0].keys() 
    
    with open('all the projects.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(project_details)
    print('file created')
    
    # separate file for 10K followers accounts only
    with open('interesting projects.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(project_details_10K_only)
    print('file created')
#------------------------------------------------------------------
    
    bot_key = '6271212992:AAG3L819O88h1OpfhxFM2-bauUuD1Sa-2zs'
    chat_id = '1855555802'
#------------------------------------------------------------------
    limit = 42   # the seuil need to be changed in function of each of the 2 scenario  
    time_interval = 5 
#------------------------------------------------------------------

    project = input(" Which project are you interested in ? : ")


    def get_price(symbol):

        url = "http://api-mainnet.magiceden.dev/v2/collections/{symbol}/stats".format(symbol=symbol.lower().replace(" ", "_"))

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        nft_price = response['floorPrice'] / 1000000000 
        return nft_price, symbol  

    def send_update(chat_id, msg):
        url = f"https://api.telegram.org/bot{bot_key}/sendMessage?chat_id={chat_id}&text={msg}"
        requests.get(url)

    def run():
            while True:
        
                floor_price, name = get_price(project)
                print(name)
                print(floor_price)
                if floor_price <= limit:  # applicated for the seller and the buyer, if i am a seller and the floor price get closer to the limit i will rise the price
                    send_update(chat_id, f" Take Your Chance ! The Price Of The NFT Collection {name} is : {floor_price} sol ")
                else:
                    send_update(chat_id, f" The Price Of The NFT Collection {name} is : {floor_price} sol ")  # can work with it if i need to know if the price of my collection is still above the mint price

                time.sleep(time_interval)
    run()

main(page)

