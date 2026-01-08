# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
    
class ActionPicturePet(Action):

    def name(self) -> Text:
        return "action_picture_pet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pet = tracker.get_slot("pet")

        images = {
            "puppy": "https://www.educateurcanin.fr/wp-content/uploads/2018/08/chiot-il-n-y-a-pas-a-dire-rien-de-mieux-qu-un-animal-pour-redonner-le-sourire_a8c59bfb45cc24ddfdd4dab8f7ba9782552d996a.jpg",
            "butterflies": "https://www.science-et-vie.com/wp-content/uploads/scienceetvie/2022/03/3-decouvertes-etonnantes-sur-vol-des-papillons-morphos.jpg",
            "koala": "https://images.unsplash.com/photo-1579972383667-4894c883d674?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "lion": "https://lh5.googleusercontent.com/proxy/_N-HEU2L_78S70Q9NWv0ARLfG-fxCFcN6k2PZv7FZR77TSfKmmNm_DiuMz_Ui9XuXrfnmdMhBUFlu1srBDwwi7QZPzEw3Cl_wIGCmKonQKOq2kg5Nr65knOEbP6gNa6v21cW",
            "cat": "https://images.ctfassets.net/denf86kkcx7r/57uYN7JlyDtQ91KvRldrm9/0a0656983993f5e09c4daa0a4fd8f5e6/comment-punir-son-chat-91",
            "dog": "https://www.espace-sciences.org/sites/default/files/styles/l980h562_1_744_/public/images/sciences-ouest/dossiers/chien_blanc_630x380.jpg?itok=sKxw81ev",
            "hamster": "https://blog.omlet.fr/wp-content/uploads/sites/8/2025/04/Hamster-allonge-sur-le-comptoir.jpg",
            "penguin": "https://cdn.download.ams.birds.cornell.edu/api/v2/asset/612763581/900"
        }

        if pet in images:
            dispatcher.utter_message("Let me see ... I found this", image=images[pet])
        else:
            dispatcher.utter_message("I don't have this animal :(")

        return []
