import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import time
import xlsxwriter
import pandas as pd
import xlrd

options = webdriver.ChromeOptions()
options.add_argument('headless')  # to ensure an addiitional web window doesn't open
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

CHROMEDRIVER_PATH = 'FilePath'
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                          chrome_options=chrome_options
                         )

driver.get('https://www.target.com/p/unscented-aveeno-daily-moisturizing-lotion-for-dry-skin-18-fl-oz/-/A-10801059')


time.sleep(15)
plain_text = driver.page_source
soup = BeautifulSoup(plain_text, 'lxml')
details=[]
relevantDetails=[]

# div = soup.findAll('div',attrs={"class":"h-padding-b-tight"})
for div in soup.findAll('div',attrs={"class":"h-padding-b-tight"}):
    details.append(div.text)

# print(details)
# print(type(details))
# relevantData = ['TCIN','UPC','DPCI']
# relevantDetails = [s for s in details if any(xs in s for xs in relevantData)]

relevantDetails=pd.DataFrame(details)
# print(relevantDetails)
# print(details)
workbook=xlsxwriter.Workbook('Example1.xlsx')
worksheet=workbook.add_worksheet()

row=0
column=0

for item in details :
    worksheet.write(row,column,item)
    row+=1

workbook.close()                         

data=pd.read_excel("Example1.xlsx",header=None)
# data=relevantDetails.to_excel('FilePath')
new = data[0].str.split(":", n = 1, expand = True)
new.columns=['attribute','text']
# #new.set_index('attribute',inplace=True)
export_excel=new.to_excel('FilePath')
