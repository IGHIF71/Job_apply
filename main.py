from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException
import json
import time
import re
class EasyApply:
    
    def __init__(self,data):
        """Parameter initiazation"""
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver = webdriver.Edge(data['driver_path'])
        
    def login(self):
        """this function login"""
        
        #make driver go to Linkedin login page
        self.driver.get('https://www.linkedin.com/uas/login')
        
        # make the driver put in logi information and hit enter button
        login_email = self.driver.find_element_by_name("session_key")
        login_email.clear()
        login_email.send_keys(self.email)
        login_password = self.driver.find_element_by_name("session_password")
        login_password.clear()
        login_password.send_keys(self.password)
        login_password.send_keys(Keys.RETURN)
    def job_search(self):
        job_link = self.driver.find_element_by_link_text("Jobs")
        job_link.click()
        
        #introduce keyword and location and hit enter button
        time.sleep(1)
        search_keyword = self.driver.find_element_by_css_selector("input.jobs-search-box__text-input")
        search_keyword.clear()
        search_keyword.send_keys(self.keywords)
        search_keyword.send_keys(Keys.RETURN)
        time.sleep(1)
        """"
        search_location = self.driver.find_element_by_css_selector("input.jobs-search-box__text-input")
        search_location.clear()
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)
        """
    def clickeasyapply(self):
        time.sleep(2)
        click_easyapply = self.driver.find_element_by_xpath("/html/body/div[5]/div[3]/div[3]/section/div/div/div/ul/li[8]/div/button")
        click_easyapply.click()
        time.sleep(1)
    def find_offers(self): 
        time.sleep(1)
        total_results = self.driver.find_element_by_class_name("display-flex.t-12.t-black--light.t-normal")
        total_results_int = int(total_results.text.split(' ',1)[0].replace(",",""))
        print(total_results_int)
        time.sleep(1)
        # get results of current page
        current_page = self.driver.current_url
        results = self.driver.find_elements_by_class_name("jobs-search-results__list-item.occludable-update.p0.relative.ember-view")
        
        # for each job add submit application is no questions are asked
        for result in results:
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()
            titles = result.find_elements_by_class_name('job-card-search__title.artdeco-entity-lockup__title.ember-view')
            for title in titles:
                self.submit(title)
                
        if total_results_int > 24:
            time.sleep(2)

            # find the last page and construct url of each page based on the total amount of pages
            find_pages = self.driver.find_elements_by_class_name("artdeco-pagination__indicator.artdeco-pagination__indicator--number.ember-view")
            total_pages = find_pages[len(find_pages)-1].text
            total_pages_int = int(re.sub(r"[^\d.]", "", total_pages))
            print(total_pages_int)
            get_last_page = self.driver.find_element_by_xpath("//button[@aria-label='Page "+str(total_pages_int)+"']")
            get_last_page.send_keys(Keys.RETURN)
            time.sleep(2)
            last_page = self.driver.current_url
            total_jobs = int(last_page.split('start=',1)[1])

            # go through all available pages and job offers and apply
            for page_number in range(25,total_jobs+25,25):
                self.driver.get(current_page+'&start='+str(page_number))
                time.sleep(2)
                results_ext = self.driver.find_elements_by_class_name("jobs-search-results__list-item.occludable-update.p0.relative.ember-view")
                for result_ext in results_ext:
                    hover_ext = ActionChains(self.driver).move_to_element(result_ext)
                   
                    titles_ext = result_ext.find_elements_by_class_name('disabled.ember-view.job-card-container__link.job-card-list__title')
                    print(titles_ext)
                    for title_ext in titles_ext:
                       
                        self.submit(title_ext)
                    hover_ext.perform()
                   
        else:
            self.close_session()
    def submit(self,job_ad):
        time.sleep(2)
        try:
            job_ad.click()
        except ElementClickInterceptedException:
            time.sleep(10)
            discard_popup = self.driver.find_element_by_class_name("artdeco-toast-item__dismiss.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--1.artdeco-button--tertiary.ember-view")
            hover = ActionChains(self.driver).move_to_element(discard_popup)
            hover.perform()
            discard_popup.send_keys(Keys.RETURN)
            print("discarding popup")
        time.sleep(2)
        
        #click on apply
        try:
            in_apply = self.driver.find_element_by_class_name("jobs-apply-button.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view")
                                                             
            in_apply.click()
            print("entering application")
        except NoSuchElementException:
            print('you aready applied to this job go to the next job ...')
            pass
        time.sleep(1)
        
        # try to submit application
        try:
            time.sleep(2)
            submit = self.driver.find_element_by_class_name("artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view")
            submit.click()
            time.sleep(2) 
            finish = self.driver.find_element_by_class_name("artdeco-modal__dismiss.artdeco-button.artdeco-button--circleartdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view")
            finish.click()
            print("applied")

           # if it is not aviable discard application
        except NoSuchElementException:
            print("not direct application")
            try:
                discard = self.driver.find_element_by_xpath("/html/body/div[3]/div/div/button")
                discard.send_keys(Keys.RETURN)
                time.sleep(1)
                discard_confirm = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[3]/button[1]")
                discard_confirm.send_keys(Keys.RETURN)
                time.sleep(1)
            except NoSuchElementException:
                pass
        except AttributeError:
            pass
        except ElementNotInteractableException:
            pass
        except ElementClickInterceptedException:
            time.sleep(10)
            
            discard_popup = self.driver.find_element_by_class_name("artdeco-toast-item__dismiss.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--1.artdeco-button--tertiary.ember-view")
            hover = ActionChains(self.driver).move_to_element(discard_popup)
            hover.perform()
            discard_popup.send_keys(Keys.RETURN)
            print("discarding popup")
            pass
    def close_connection(self):
        self.driver.close()
        
    def apply(self):
        self.driver.maximize_window()
        self.login()
        time.sleep(2)
        self.job_search()
        time.sleep(2)
        self.clickeasyapply()
        time.sleep(2)
        self.find_offers()
        time.sleep(2)
        self.close_connection()
                

if __name__ == '__main__':
    
    with open('config.json') as config_file:
        data = json.load(config_file)
    
    bot = EasyApply(data)
    bot.apply()