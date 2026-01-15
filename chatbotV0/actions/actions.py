import os
import signal
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import Restarted
from rasa_sdk.events import SlotSet

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

class ActionCalculateMGD(Action):
    def name(self) -> str:
        return "action_calculate_mgd"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="J'ai calculé le Modèle Géométrique Direct.")
        
        return [SlotSet("calculus", "MGD")]

class ActionCalculateMGI(Action):
    def name(self) -> str:
        return "action_calculate_mgi"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Calcul du Modèle Géométrique Inverse terminé.")
        
        return [SlotSet("calculus", "MGI")]

class ActionCalculateJacobian(Action):
    def name(self) -> str:
        return "action_calculate_jacobian"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        dispatcher.utter_message(text="La matrice Jacobienne a été calculée. Elle relie les vitesses articulaires aux vitesses de l'effecteur.")
        
        return [SlotSet("calculus", "Jacobienne")]

class ActionGetSpecificHelp(Action):
    def name(self) -> str:
        return "action_get_specific_help"

    def run(self, dispatcher, tracker, domain):
        # On récupère la valeur du slot 'calculus'
        last_calc = tracker.get_slot("calculus")

        if last_calc == "MGD":
            msg = """Nous venons de voir le MGD (Position via Angles).

Voulez-vous maintenant :
• Inverser le problème avec le MGI ?
• Voir comment calculer les vitesses avec la Jacobienne ?
• Obtenir le code Python pour ce calcul ?"""

        elif last_calc == "MGI":
            msg = """Le calcul du MGI est terminé.

Souhaitez-vous :
• Vérifier si ce point est dans l'espace de travail (Workspace) ?
• Générer une trajectoire vers cette position ?
• Faire un quiz pour vérifier vos connaissances ?"""

        elif last_calc == "Jacobienne":
            msg = """La Matrice Jacobienne permet de lier les vitesses.

Prochaines étapes suggérées :
• Étudier le contrôle et l'asservissement ?
• Voir les singularités du robot ?
• Revenir au menu principal ?"""

        else:
            # Aide générique si aucun calcul n'a été fait
            msg = """Je peux vous aider à comprendre les bases de la robotique ou effectuer des calculs.
            
Souhaitez-vous calculer un MGD, un MGI ou une Jacobienne ? """

        dispatcher.utter_message(text=msg)
        return []