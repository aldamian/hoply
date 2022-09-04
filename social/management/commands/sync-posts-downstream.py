from django.core.management.base import BaseCommand
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
        response = requests.get(endpoint, headers=headers)
        print(response.status_code)

        if response.status_code == 200:
                
                posts = response.json()
    
                for post in posts:
                    if Post.objects.filter(uuid=post['id']).exists():
                        # update post
                        post_obj = Post.objects.get(uuid=post['id'])
                        post_obj.user_id = post['user_id']
                        post_obj.body = post['content']
                        post_obj.edited_stamp = post['stamp']
                        post_obj.save()

                    else:
                        # create post
                        post_obj = Post.objects.create(uuid=post['id'], 
                                                       user_id=post['user_id'], 
                                                       body=post['content'], 
                                                       stamp=post['stamp'])
                        post_obj.save()