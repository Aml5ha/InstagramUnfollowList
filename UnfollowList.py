import os.path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


### This method waits for al elements on the page to load

def WaitForLoad(driver):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located
        )
    finally:
        time.sleep(.5)

### This method does the setup by handling the login
def Setup():
    #the following two lines asks the user for username and password and keeps it for later use
    username = input("Enter Username: ")
    password = input("Enter password: ")

    directory = os.path.dirname(os.path.abspath(__file__))  # gets the path of where this file is saved
    location_of_driver = (os.path.join(directory,'chromedriver'))  # appends 'chromedriver' to the current file path - make sure chrome driver is in same directory as this file

    #print(locationOfDriver)

    driver = webdriver.Chrome(location_of_driver)

    driver.get("https://www.instagram.com/accounts/login/")
    WaitForLoad(driver)

    login_list = driver.find_elements_by_name("username") #finds the elements on the page that have a matching name

    login_box = login_list[0]                       #looking through the HTML, you can see that the second instance of "session[username_or_email]" corresponds to the actual login box
    login_box.send_keys(username, Keys.ARROW_DOWN)  #sending the username to the login box, and the down arrow key to indicate its finished


    password_list = driver.find_elements_by_name("password") #finds all elements relating to password
    password_box = password_list[0]                                   #second element mentioned on the page corresponds to the password box

    password_box.send_keys(password, Keys.ARROW_DOWN)  #send the password to the appropriate box

    password_box.send_keys(Keys.TAB, Keys.TAB, Keys.ENTER)       #navigating and 'clicking' the log in button

    time.sleep(2)



    return driver, username

### This method gets a list of followers
def GetFollowersList(driver, username):
    driver.get("https://www.instagram.com/" + username)
    WaitForLoad(driver)
    profile_info = driver.find_elements_by_class_name("-nal3") # finds the header

    number_text = profile_info[1].text.split() #get the header that has info for: posts, followers, following
    num_of_followers = int(number_text[0]) #get the number of followers

    profile_info[1].click() #click on the followers link
    time.sleep(1)

    time_to_scroll = 20

    scr1 = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]') #find the frame that shows the followers

    times_to_scroll = int(num_of_followers / 8 + 2) #an arbitrary decision for scrolling 1/8th times the number of followers (+2 for good measure)

    ## this block of code handles scrolling down
    times_scrolled = 0
    while times_scrolled < times_to_scroll:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
        time.sleep(.5)
        times_scrolled += 1

    followers_found = driver.find_elements_by_class_name("FsskP") #finds the users on the page


    extra_scrolls = 0
    ## This block of code below makes sure that the number of followers found on the page are similar to the number extracted from the profile page
    ## if not, the page scrolls some more
    while len(followers_found) + 1 < num_of_followers:
        extra_scrolls+=1
        for _ in range(100):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
            time.sleep(.5)
        followers_found = driver.find_elements_by_class_name("FsskP")
    print("Followers extra scrolls count: " + str(extra_scrolls))
    # NOTE: if the 'extra scrolls' is too high, try to raise the times_to_scroll variable by dividing by a smaller number

    final_list_of_followers = []
    for i in followers_found: #for each element in the list of followers found...
        final_list_of_followers.append(i.text) #add their instagram handle to the list

    return final_list_of_followers #return the list of followers


### This method gets a list of people you follow
def GetFollowingList(driver, username):
    driver.get("https://www.instagram.com/" + username) #navigates back to user's profile
    WaitForLoad(driver)
    profile_info = driver.find_elements_by_class_name("-nal3")#get the header that has info for: posts, followers, following
    number_text = profile_info[2].text.split() # splits the info the page has for users following
    num_of_following = int(number_text[0]) #extract the number of people you follow

    profile_info[2].click() #click on the following page to navigate there
    time.sleep(1)

    scr1 = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]') #find the frame with showing people you follow

    times_to_scroll = int(num_of_following/8 + 2) #an arbitrary decision for scrolling 1/8th times the number of followers (+2 for good measure)

    ## this block of code handles scrolling down
    times_scrolled = 0
    while times_scrolled < times_to_scroll:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
        time.sleep(.5)
        times_scrolled+=1


    following_found = driver.find_elements_by_class_name("FsskP") #finds the users on the page


    ## This block of code below makes sure that the number of following found on the page are similar to the number extracted from the profile page
    ## if not, the page scrolls some more
    extra_scrolls = 0
    while len(following_found) + 1 < num_of_following:
        extra_scrolls+=1
        for _ in range(100):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
            time.sleep(.5)
        following_found = driver.find_elements_by_class_name("FsskP")

    print("Following extra scrolls count: " + str(extra_scrolls))
    # NOTE: if the 'extra scrolls' is too high, try to raise the times_to_scroll variable by dividing by a smaller number

    final_list_of_following = []
    for i in following_found: #for each following profile in the list...
        final_list_of_following.append(i.text) #add their instagram handle to the list


    return final_list_of_following


### This method takes the two lists and compares them to see who you follow doesnt follow you back and prints them to a file
def people_to_unfollow(following, followers):
    file = open('People_to_unfollow.txt', 'w') #open file to write
    for f in following: #for each person you are following
        if (f not in followers): #if the person you are following is not in the list of people following you, write their handle to a file
            file.write(f + "\n")
    file.close()


start = time.time() #starts a timer to see how long it will take
driver, username = Setup() #sets driver, username to the results of the Setup method, which returns the driver and username to be used in another method
followers = GetFollowersList(driver, username) #gets a list of people that follow you
following = GetFollowingList(driver, username) #gets a list of people you are following
people_to_unfollow(following, followers) #compares the two lists and prints people that don't follow you to a file
print("Total time taken: " + str(time.time() - start)) #prints total time taken
driver.quit()