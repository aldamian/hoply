from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import datetime
from datetime import timedelta
import requests


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        endpoint = "https://caracal.imada.sdu.dk/app2022/users"
        bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYXBwMjAyMiJ9.iEPYaqBPWoAxc7iyi507U3sexbkLHRKABQgYNDG4Awk"
        headers = {
            "Authorization": "Bearer " + bearer_token,
            "Content-Type": "application/json",
        }
        

        # get users that have been created in the last 24 hours
        users = User.objects.filter(last_login__gte=datetime.datetime.now() - timedelta(hours=24))

        for user in users:
            # post user to upstream database
            data = {
                "id": user.username,
                "user_id": user.first_name,
                "stamp": user.last_login,
            }
            response = requests.post(endpoint, headers=headers, json=data)
            print(response.status_code)



