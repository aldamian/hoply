from django.core.management.base import BaseCommand
import datetime
from datetime import timedelta
import requests
from social.models import Post


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        endpoint = "https://caracal.imada.sdu.dk/app2022/posts"
        bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYXBwMjAyMiJ9.iEPYaqBPWoAxc7iyi507U3sexbkLHRKABQgYNDG4Awk"
        headers = {
            "Authorization": "Bearer " + bearer_token,
            "Content-Type": "application/json",
        }
        

        # get posts that have been created in the last 24 hours
        posts = Post.objects.filter(stamp__gte=datetime.datetime.now() - timedelta(hours=24))

        for post in posts:
            # post post to upstream database
            data = {
                "id": post.uuid,
                "user_id": post.user_id,
                "content": post.body,
                "stamp": post.stamp,
            }
            response = requests.post(endpoint, headers=headers, json=data)
            print(response.status_code)



