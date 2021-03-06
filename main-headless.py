from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from secrets import no_fly_zone, username, password
import random

birthday_ppl = []

class Bot ():

    def __init__(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.options.add_argument(f'user-agent={user_agent}')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--proxy-server='direct://'")
        self.options.add_argument("--proxy-bypass-list=*")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=self.options)

    def login(self):
        self.driver.get('https://www.facebook.com/')
        user = self.driver.find_elements_by_xpath('//*[@id="email"]')
        user[0].send_keys(username)
        pwd = self.driver.find_elements_by_xpath('//*[@id="pass"]')
        pwd[0].send_keys(password)
        pwd[0].send_keys(Keys.ENTER)
        sleep(3)


    def move_to_birth(self):
        sleep(2)
        self.driver.get('https://www.facebook.com/birthdays')


    def find_birthdays (self):
        sleep(3)
        cookies =  self.driver.find_elements_by_xpath("//*[contains(text(), 'Accept All')]")
        cookies[0].click()
        sleep(2)
        ancors = self.driver.find_elements_by_tag_name('a')
        ancors = [a.get_attribute ('href') for a in ancors]
        ancors = [a for a in ancors if str(a).endswith('?__tn__=%3C')]
        birthday_ppl.append(ancors)


    def bday_wish(self, name):
        messages= [
            f'Ciao {name}, tantissimi auguri di buon compleaanno!',
            f'Buon compleanno {name}!!',
            f'Augurissimi {name}, felice compleanno',
            f'Auguri di buon compleanno {name}',
        ]
        message = random.choice(messages)
        return message


    def happy_bday (self):
        print ('executing happy bday')
        try:
            for i in birthday_ppl[0]:
                self.driver.get(str(i))
                sleep(3)
                name_lastname = self.driver.find_elements_by_tag_name('h1')[0]
                if (name_lastname.text) in no_fly_zone:
                    print(name_lastname.text + ' is in no fly zone')
                    pass
                else:
                    name = (name_lastname.text).split(' ')[0]
                    bday_button = self.driver.find_elements_by_xpath(("//*[contains(text(), 'a happy birthday...')]"))
                    bday_button[0].click()
                    sleep(3)
                    bday_box = self.driver.find_elements_by_xpath('//*[@role="textbox"]')
                    bday_wish = self.bday_wish(name=name)
                    bday_box[-1].send_keys(bday_wish)
                    # birthday_messages[(name_lastname.text)] = bday_wish # this line appends to a temporary dict full name and message sent to each person
                    sleep(3)
                    post = self.driver.find_elements_by_xpath("//*[contains(text(),'Post')]")
                    post[2].click()
                    print(bday_wish)
                    sleep(5)
        except Exception:
            print('there are no other bday boys&girls for today')
            self.driver.quit()


run = Bot ()
run.login()
run.move_to_birth()
run.find_birthdays()
run.happy_bday()

