# crm/management/commands/fetch_goodreads_data.py

from django.core.management.base import BaseCommand, CommandError
import requests
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = 'Fetch Goodreads data using provided credentials'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, required=True, help='Goodreads email')
        parser.add_argument('--password', type=str, required=True, help='Goodreads password')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']

        if not email or not password:
            raise CommandError('Email and password must be provided')

        try:
            session = requests.Session()
            login_url = 'https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads.com%2Fap-handler%2Fsign-in&siteState=eyJyZXR1cm5fdXJsIjoiaHR0cHM6Ly93d3cuZ29vZHJlYWRzLmNvbS8ifQ%3D%3D'
            response = session.get(login_url)

            if response.status_code != 200:
                raise CommandError('Failed to load Goodreads login page')

            soup = BeautifulSoup(response.content, 'html.parser')

            # Debug: Print the HTML content
            with open('login_page.html', 'w', encoding='utf-8') as file:
                file.write(response.text)

            authenticity_token_input = soup.find('input', {'name': 'authenticity_token'})

            if authenticity_token_input:
                authenticity_token = authenticity_token_input.get('value')
            else:
                raise CommandError('authenticity_token not found in the login page')

            login_payload = {
                'user[email]': email,
                'user[password]': password,
                'authenticity_token': authenticity_token
            }

            post_response = session.post(login_url, data=login_payload)

            if post_response.status_code == 200 and 'logout' in post_response.text:
                self.stdout.write(self.style.SUCCESS('Successfully logged in to Goodreads'))
            else:
                self.stdout.write(self.style.ERROR('Failed to log in to Goodreads'))

            data_url = 'https://www.goodreads.com/review/list'
            data_response = session.get(data_url)

            if data_response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('Successfully fetched Goodreads data'))
            else:
                self.stdout.write(self.style.ERROR('Failed to fetch Goodreads data'))

        except Exception as e:
            raise CommandError(f'Error occurred: {str(e)}')
