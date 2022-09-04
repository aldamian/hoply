from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import requests


class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):

        endpoint = "https://caracal.imada.sdu.dk/app2022/users"
        bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYXBwMjAyMiJ9.iEPYaqBPWoAxc7iyi507U3sexbkLHRKABQgYNDG4Awk"
        headers = {
            "Authorization": "Bearer " + bearer_token,
            "Content-Type": "application/json",
        }
        response = requests.get(endpoint, headers=headers)
        print(response.status_code)

        if response.status_code == 200:

            users = response.json()

            for user in users:
                if User.objects.filter(username=user['id']).exists():
                    # update user
                    user_obj = User.objects.get(username=user['id'])
                    user_obj.first_name = user['name']
                    # update user's time stamp
                    user_obj.last_login = user['stamp']
                    user_obj.save()

                else:
                    # create user
                    user_obj = User.objects.create_user(username=user['id'], password='password1234')
                    user_obj.first_name = user['name']
                    user_obj.last_login = user['stamp']
                    user_obj.save()




        
        
