import os
import signal
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import Restarted

class ActionEndConversation(Action):
    def name(self) -> str:
        return "action_end_conversation"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Au revoir ! N'hésitez pas à revenir pour en apprendre plus sur la robotique. À bientôt !")
        return [Restarted()]

class ActionIlustrer(Action):
    def name(self) -> str:
        return "action_illustrer"

    def run(self, dispatcher, tracker, domain):
        # On récupère le dernier intent pour savoir quoi illustrer
        intent = tracker.latest_message['intent'].get('name')
        
        images = {
            "ask_robot_types": "https://www.robotpark.com/image/data/BLOG_EN/51000/All-Types-Of-Robots-By-Robotpark.png",
            "ask_kinematics": "https://www.mdpi.com/electronics/electronics-13-03304/article_deploy/html/images/electronics-13-03304-g001.png",
            "ask_articulation": "https://www.memoireonline.com/09/09/2723/Elaboration-dune-strategie-de-coordination-de-mouvements-pour-un-manipulateur-mobile-redondant148.png",
            "ask_dof": "https://miro.medium.com/v2/resize:fit:1280/format:webp/1*bRZ2SkufbL5QnXCnf9kYSA.jpeg"
        }

        image_url = images.get(intent)

        if image_url:
            dispatcher.utter_message(text="Voici une illustration pour vous aider :", image=image_url)
        else:
            pass 

        return []