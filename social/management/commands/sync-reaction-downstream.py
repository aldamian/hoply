from django.core.management.base import BaseCommand
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

        if response.status_code == 200:

            reactions = response.json()

            for reaction in reactions:
                # filter reaction by user_id and post_id
                if Reaction.objects.filter(user_id=reaction['user_id'], post_id=reaction['post_id']).exists():
                    # update reaction
                    reaction_obj = Reaction.objects.get(user_id=reaction['user_id'], post_id=reaction['post_id'])
                    reaction_obj.author = reaction['user_id']
                    reaction_obj.post = reaction['post_id']
                    reaction_obj.choice = reaction['type']
                    reaction_obj.status = reaction['status']
                    reaction_obj.save()

                else:
                    # create reaction
                    reaction_obj = Reaction.objects.create(user_id=reaction['user_id'], 
                                                           post_id=reaction['post_id'], 
                                                           author=reaction['user_id'], 
                                                            post=reaction['post_id'], 
                                                            choice=reaction['type'], 
                                                            status=reaction['status'])
                    reaction_obj.save()