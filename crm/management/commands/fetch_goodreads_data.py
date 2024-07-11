# crm/management/commands/fetch_goodreads_data.py

from django.core.management.base import BaseCommand, CommandError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os

class Command(BaseCommand):

    help = 'Fetch Goodreads data using provided credentials'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, required=True, help='Goodreads email')
        parser.add_argument('--password', type=str, required=True, help='Goodreads password')
        parser.add_argument('--driver-path', type=str, help='Path to ChromeDriver')

    def handle(self, *args, **options):

        email = options['email']
        password = options['password']
        driver_path = options.get('driver_path', None)

        if not email or not password:
            raise CommandError('Email and password must be provided')

        try:
           
            # Set up Selenium WebDriver
            if driver_path:
                chrome_service = Service(driver_path)
            else:
                chrome_service = Service(ChromeDriverManager().install())

            chrome_options = Options()
            #chrome_options.add_argument("--headless")  # Run in headless mode
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

            driver.get('https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads.com%2Fap-handler%2Fsign-in&siteState=eyJyZXR1cm5fdXJsIjoiaHR0cHM6Ly93d3cuZ29vZHJlYWRzLmNvbS8ifQ%3D%3D')
            time.sleep(3)  # Wait for the page to load

            # Fill in the login form
            email_input = driver.find_element(By.ID, 'ap_email')
            password_input = driver.find_element(By.ID, 'ap_password')

            email_input.send_keys(email)
            password_input.send_keys(password)

            # Submit the form
            submit_button = driver.find_element(By.ID, 'signInSubmit')
            submit_button.click()

            # Wait for the login process to complete
            time.sleep(5)

             # Check if logged in successfully
            self.stdout.write(self.style.SUCCESS('Successfully logged in to Goodreads'))

            # Navigate to the books read page
            challenge_link = driver.find_element(By.LINK_TEXT, 'View Challenge')
            challenge_link.click()
            time.sleep(1)

            books = driver.find_element(By.LINK_TEXT, 'view books')
            books.click()
            time.sleep(1)

            yearbooks = driver.find_element(By.LINK_TEXT, 'Go to My Books shelved in 2024')
            yearbooks.click()
            time.sleep(1)

            # Locate book elements within the 'booksBody' ID
            book_elements = driver.find_elements(By.CSS_SELECTOR, '#booksBody .bookalike.review')
            for book_element in book_elements:
                title_element = book_element.find_element(By.CSS_SELECTOR, 'a.field title')
               # author_element = book_element.find_element(By.CSS_SELECTOR, 'a.')
                title = title_element.text
                #author = author_element.text
                #print(f"Title: {title}, Author: {author}")
                self.stdout.write(self.style.SUCCESS('{title}'))

            # Optionally, save HTML content of the page
            with open('goodreads_books_read.html', 'w', encoding='utf-8') as file:
                file.write(driver.page_source)

            self.stdout.write(self.style.SUCCESS('Successfully fetched Goodreads data'))

            # Close the browser session
            driver.quit()

        except Exception as e:
            raise CommandError(f'Error occurred: {str(e)}')