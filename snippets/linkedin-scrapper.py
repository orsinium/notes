"""
A simple Python script to scrape a company's LinkedIn profile for list of employees.
Outputs a CSV into stdout.

https://github.com/joeyism/linkedin_scraper
"""
import csv
import sys
from linkedin_scraper import Company
from linkedin_scraper import actions
from selenium import webdriver

email = '...'
password = '...'
company_url = 'https://www.linkedin.com/company/.../'

driver = webdriver.Chrome()
driver.implicitly_wait(3)
actions.login(driver, email, password)

c = Company(
    company_url,
    driver=driver,
    scrape=False,
    close_on_complete=False,
    get_employees=False,
)
employees = c.get_employees()
w = csv.writer(sys.stdout)
for employee in employees:
    if employee:
        w.writerow(list(employee.values()))
