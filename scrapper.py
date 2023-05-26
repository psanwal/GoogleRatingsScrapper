from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os

def main():
    try:

        # renaming the stale ratings file if it exists.
        if os.path.exists('ratings.csv'):
            os.rename('ratings.csv', 'ratings_old.csv')

        # Setting Chrome Options
        options = Options()
        options.add_argument("--lang=en")
        driver = webdriver.Chrome(options=options)

        # Reading Google maps reviews URL from clientlist.txt
        # Using "|" separated file because reviews URL will have "," in it.
        clients = open('clientlist.txt', "r")
        clientreader = csv.reader(clients, delimiter='|')

        # bypassing the header row
        next(clientreader)

        # Opening rathings files to populate ratings
        ratings = open('ratings.csv', "w",newline='', encoding='utf-8')
        populaterating = csv.writer(ratings)

        # Writing header
        populaterating.writerow(['ClientName','ClientWebsite','TotalRatings','R5','R4','R3','R2','R1'])

        # Looping on each client
        for row in clientreader:
            ClientName = row[0]
            ClientWebsite='Website not available' if row[1] == '' else row[1]
            url = row[2]

            # launching driver Google maps reviews URL.
            driver.get(url)

            # Implementing wait until "Reviews" button is clickable
            wait = WebDriverWait(driver, 10)
            menu_bt = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label,"Reviews for ")]'))) 
            menu_bt.click()

            # sleep for reviews to load
            time.sleep(5)

            # Getting rathing data
            element5s = driver.find_element(By.XPATH,'//tr[contains(@aria-label,"5 stars, ")]') 
            element4s = driver.find_element(By.XPATH,'//tr[contains(@aria-label,"4 stars, ")]')
            element3s = driver.find_element(By.XPATH,'//tr[contains(@aria-label,"3 stars, ")]') 
            element2s = driver.find_element(By.XPATH,'//tr[contains(@aria-label,"2 stars, ")]') 
            element1s = driver.find_element(By.XPATH,'//tr[contains(@aria-label,"1 stars, ")]')

            # Calculate Total ratings
            TotalRatings = int(element5s.get_attribute('aria-label').split(',')[1][1:].split(" ")[0])+ \
            int(element4s.get_attribute('aria-label').split(',')[1][1:].split(" ")[0])+ \
            int(element3s.get_attribute('aria-label').split(',')[1][1:].split(" ")[0])+ \
            int(element2s.get_attribute('aria-label').split(',')[1][1:].split(" ")[0])+ \
            int(element1s.get_attribute('aria-label').split(',')[1][1:].split(" ")[0])

            # Populating ratings data into csv 
            populaterating.writerow([ClientName,ClientWebsite,TotalRatings,
                                    element5s.get_attribute('aria-label').split(',')[1][1:].split(" ")[0],element4s.get_attribute('aria-label').split(',')[1][1:].split(" ")[0],
                                    element3s.get_attribute('aria-label').split(',')[1][1:].split(" ")[0],element2s.get_attribute('aria-label').split(',')[1][1:].split(" ")[0],
                                    element1s.get_attribute('aria-label').split(',')[1][1:].split(" ")[0]])
        
        # Closing the driver
        driver.quit()

        # If there is no exception till here and an old rating file exists, we need to drop it.
        if os.path.exists('ratings_old.csv'):
            os.remove('ratings_old.csv')

        # CLosing file handels.
        clients.close()
        ratings.close()

    except:

        # if exception occured after the rating file is created , data in ratings file might not be usable. Therefore removing the ratings file.
        if os.path.exists('ratings.csv'):
            ratings.close()
            os.remove('ratings.csv')

        # Restoring old ratings file.    
        print('Exception occured, restoring old ratings')

        if os.path.exists('ratings_old.csv'):
            os.rename('ratings_old.csv', 'ratings.csv')

if __name__ == "__main__":
    main()

