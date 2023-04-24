import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class Election:

    # creating a constructor
    def __init__(self, link, headless=True):
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                         "(KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")

        #It uses the ChromeDriverManager module to automatically download and install ChromeDriver.
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        self.link = link

    def data_scrapt(self):
        link = self.link
        #URL open, initialize
        self.browser.get(link)
        # waiting a randomly time
        time.sleep(random.randint(1, 5))
        # Retrieval of the relevant parts of the table to be scraping process
        votes = self.browser.find_elements(by=By.XPATH, value='//*[@id="mw-content-text"]/div[1]/table[2]/tbody/'
                                                              'tr[(position() >= 4 and position() <= 9) or'
                                                              '(position() >= 14 and position() <= 25)]')
        data = []
        #A for loop that traverses line by line and collects data
        for v in votes:
            survey_company = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(2) > a')
            sample = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(3)')
            votes_per_akp = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(4)')
            votes_per_mhp = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(5)')
            votes_per_bbp = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(6)')
            votes_per_yrp = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(7)')
            votes_per_chp = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(9)')
            votes_per_iyi = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(10)')
            votes_per_deva = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(11)')
            votes_per_gp = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(12)')
            votes_per_sp = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(13)')
            votes_per_dp = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(14)')
            votes_per_ysgp = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(16)')
            votes_per_tip = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(17)')
            votes_per_zp = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(19)')
            votes_per_mp = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(20)')
            votes_per_tdp = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(21)')
            votes_per_btp = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(22)')
            votes_per_others = v.find_elements(by=By.CSS_SELECTOR, value='td:nth-child(23)')
            data.append(
                {
                    'company': survey_company[0].text,
                    'sample': convert(sample[0].text),
                    'akp_vote': realvote(convert(sample[0].text), votes_per_akp[0].text),
                    'mhp_vote': realvote(convert(sample[0].text), votes_per_mhp[0].text),
                    'bbp_vote': realvote(convert(sample[0].text), votes_per_bbp[0].text),
                    'yrp_vote': realvote(convert(sample[0].text), votes_per_yrp[0].text),
                    'chp_vote': realvote(convert(sample[0].text), votes_per_chp[0].text),
                    'iyi_vote': realvote(convert(sample[0].text), votes_per_iyi[0].text),
                    'deva_vote': realvote(convert(sample[0].text), votes_per_deva[0].text),
                    'gp_vote': realvote(convert(sample[0].text), votes_per_gp[0].text),
                    'sp_vote': realvote(convert(sample[0].text), votes_per_sp[0].text),
                    'dp_vote': realvote(convert(sample[0].text), votes_per_dp[0].text),
                    'ysgp_vote': realvote(convert(sample[0].text), votes_per_ysgp[0].text),
                    'tip_vote': realvote(convert(sample[0].text), votes_per_tip[0].text),
                    'zp_vote': realvote(convert(sample[0].text), votes_per_zp[0].text),
                    'mp_vote': realvote(convert(sample[0].text), votes_per_mp[0].text),
                    'tdp_vote': realvote(convert(sample[0].text), votes_per_tdp[0].text),
                    'btp_vote': realvote(convert(sample[0].text), votes_per_btp[0].text),
                    'others_vote': realvote(convert(sample[0].text), votes_per_others[0].text)
                }
            )
        #Closing a URL
        self.browser.close()
        return data


def realvote(sample, votes_per):
    #float doesn't accept comma ",". This why, we convert all percentiles into dot ".".
    #After this process, the number of people who voted is found.
    if ',' in votes_per:
        votes_per = votes_per.replace(',', '.')
        vote_count = round((sample * float(votes_per)) / 100)
        return vote_count
    return 0

#We need to remove the dot symbol in order to use the sample as an integer value
def convert(sample):
    first_part = int(sample.split(".")[0])
    second_part = int(sample.split(".")[1])
    result = first_part * 1000 + second_part
    return result


if __name__ == "__main__": #This module will be used as the main program
    elections = Election(
        #The URL of the site where the scraping will be done
        link="https://tr.wikipedia.org/wiki/%C3%9Clke_%C3%A7ap%C4%B1nda_2023_T%C3%BCrkiye_genel_"
             "se%C3%A7imleri_i%C3%A7in_yap%C4%B1lan_anketler",
        #The web browser is clearly displayed.
        headless=False
    )
    elections.data_scrapt()