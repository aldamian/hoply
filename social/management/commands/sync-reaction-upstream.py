from django.core.management.base import BaseCommand
import datetime
from datetime import timedelta
import requests
from social.models import Reaction


class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):

        endpoint = "https://caracal.imada.sdu.dk/app2022/reactions"
        bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYXBwMjAyMiJ9.iEPYaqBPWoAxc7iyi507U3sexbkLHRKABQgYNDG4Awk"
        headers = {
            "Authorization": "Bearer " + bearer_token,
            "Content-Type": "application/json",
        }
        response = requests.get(endpoint, headers=headers)
        print(response.status_code)

        # get reactions from the last 24 hours
        reactions = Reaction.objects.filter(stamp__gte=datetime.datetime.now() - timedelta(hours=24))
        
        for reaction in reactions:
            # post reaction to upstream database
            data = {
                "user_id": reaction.author,
                "post_id": reaction.post,
                "type": reaction.choice,
                "stamp": reaction.stamp,
            }
            response = requests.post(endpoint, headers=headers, json=data)
            print(response.status_code)