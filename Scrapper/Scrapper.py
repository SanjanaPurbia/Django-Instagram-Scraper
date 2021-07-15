#!/usr/bin/env python
# coding: utf-8

# In[4]:


from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

class Instagram:
    def scrap( username, password):
        #driver_path = "D:\\Learning\\College Section\\Setup\\Drivers\\chromedriver_win32\\chromedriver.exe"
        #brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        #option = webdriver.ChromeOptions()
        #option.binary_location = brave_path
        #browser = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
        browser = webdriver.Chrome("D:\\Setup\\driver\\chromedriver_win32\\chromedriver.exe")
        browser.fullscreen_window()
        browser.get("https://www.instagram.com/")
        sleep(5)
        
        try:
            #Login'',""
            browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(username)
            browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password)
            browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
            sleep(3)

            browser.get("https://www.instagram.com/" + username)
            sleep(2)

            #Number of posts........................................

            post = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text
            fol_num = int(browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text)
            fng_num = int(browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text)
            user_info = [browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/div/div/div/button/img').get_attribute('src'),
                         browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h2').text,
                         browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/h1').text
                         
                        ]
                                                                                                                                                                                                              
            #Fetching follower section........................................

            browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
            sleep(2)
            for i in range(fol_num*5):
                browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', browser.find_element_by_class_name('isgrP')) 
            follower = BeautifulSoup(browser.find_element_by_class_name("isgrP").get_attribute("innerHTML"),"html.parser")
            try:
                browser.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]').click()
            except:
                browser.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]').click()
            sleep(2)

            #Fetching following section........................................
            browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
            sleep(3)
            for i in range(fng_num*5):
                browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', browser.find_element_by_class_name('isgrP')) 
            following = BeautifulSoup(browser.find_element_by_class_name("isgrP").get_attribute("innerHTML"),"html.parser")

            browser.close()
        #..........................................................................
            # Post --> post
            # Follower number --> flo_num
            # Following number --> fng_num
            # follwer data --> follower
            # following number --> following 
            # who is not following you  -->  NotFolYou
            # who you are not following  --> 
            # Clear data data --> ClearDataFollower,ClearDataFollowing

            # [username, fullname, imagelink , profilelink ]
            ClearDataFollower = []
            ClearDataFollowing = []
            YouFol = []
            YouFon = []


            # Cleaning following data
            cf = follower.find_all('li')
            for i in cf:
                temp =[]
                temp.append(i.find_all("div")[4].find("a").text)
                YouFon.append(i.find_all("div")[4].find("a").text)
                temp.append(i.find_all("div")[-2].text)
                temp.append(i.find("img")["src"])
                temp.append("https://www.instagram.com"+i.find_all("div")[4].find("a")["href"])
                ClearDataFollower.append(temp)

            cf = following.find_all("li")
            for i in cf:
                temp =[]
                temp.append(i.find_all("div")[4].find("a").text)
                YouFol.append(i.find_all("div")[4].find("a").text)
                temp.append(i.find_all("div")[-2].text)
                temp.append(i.find("img")["src"])
                temp.append("https://www.instagram.com"+i.find_all("div")[4].find("a")["href"])
                ClearDataFollowing.append(temp)
            follower = []
            for i in range(len(YouFol)):
                if YouFol[i] not in YouFon:
                    for j in ClearDataFollowing:
                        if j[0] == YouFol[i]:
                            follower.append(j)
                            break
            following= []
            for i in range(len(YouFon)):
                if YouFon[i] not in YouFol:
                    for j in ClearDataFollower:
                        if j[0] == YouFon[i]:
                            following.append(j)
                            break   
            DataDict = {
                "post" :post,
                "user_info" : user_info,
                "follower_count" : fol_num,
                "following_count" : fng_num,
                "follower_data" : ClearDataFollower,
                "following_data" : ClearDataFollowing,
                "non_followers" : follower,
                "not_following" : following
            }
            return (DataDict,True)
        except:
            return False
            
    

