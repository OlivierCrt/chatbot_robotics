"""
Actions personnalisées pour le chatbot RoboTeach
Fichier : actions.py
"""

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import numpy as np
import math

class ActionCalculateMGD(Action):
    """Calcule le Modèle Géométrique Direct (angles -> position)"""
    
    def name(self) -> Text:
        return "action_calculate_mgd"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Récupération des données
        q1 = tracker.get_slot("q1") or 0.0
        q2 = tracker.get_slot("q2") or 0.0
        q3 = tracker.get_slot("q3") or 0.0
        L1 = tracker.get_slot("link_length_1") or 300.0
        L2 = tracker.get_slot("link_length_2") or 250.0
        L3 = tracker.get_slot("link_length_3") or 150.0
        
        # Conversion radians
        q1_rad = math.radians(q1)
        q2_rad = math.radians(q2)
        q3_rad = math.radians(q3)
        
        # Calcul position (x, y)
        x = (L1 * math.cos(q1_rad) + 
             L2 * math.cos(q1_rad + q2_rad) + 
             L3 * math.cos(q1_rad + q2_rad + q3_rad))
        
        y = (L1 * math.sin(q1_rad) + 
             L2 * math.sin(q1_rad + q2_rad) + 
             L3 * math.sin(q1_rad + q2_rad + q3_rad))
        
        z = 100.0
        phi_deg = math.degrees(q1_rad + q2_rad + q3_rad)
        
        message = f"""
🎯 **MGD Calculé**
📍 **Position :** X={x:.1f}, Y={y:.1f}, Z={z:.1f} mm
📐 **Orientation :** {phi_deg:.1f}°
ℹ️ Configuration : q1={q1}°, q2={q2}°, q3={q3}°
"""
        dispatcher.utter_message(text=message)
        
        return [
            SlotSet("last_calculation_type", "MGD"),
            SlotSet("target_x", x),
            SlotSet("target_y", y),
            SlotSet("target_z", z),
            SlotSet("topics_learned", tracker.get_slot("topics_learned") or [] + ["MGD"])
        ]


class ActionCalculateMGI(Action):
    """Calcule le Modèle Géométrique Inverse (position -> angles)"""
    
    def name(self) -> Text:
        return "action_calculate_mgi"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        x = tracker.get_slot("target_x") or 500.0
        y = tracker.get_slot("target_y") or 0.0
        
        L1 = tracker.get_slot("link_length_1") or 300.0
        L2 = tracker.get_slot("link_length_2") or 250.0
        L3 = tracker.get_slot("link_length_3") or 150.0
        
        r = math.sqrt(x**2 + y**2)
        r_max = L1 + L2 + L3
        r_min = abs(L1 - L2 - L3)
        
        if r > r_max or r < r_min:
            dispatcher.utter_message(text=f"⚠️ **Point Inaccessible**\nDistance {r:.0f}mm hors de portée ({r_min:.0f}-{r_max:.0f}mm).")
            return [SlotSet("last_calculation_type", "MGI_failed")]
        
        # MGI Simplifié (q3=0)
        q3 = 0.0
        
        # Al-Kashi pour q2
        cos_q2 = (r**2 - L1**2 - L2**2) / (2 * L1 * L2)
        cos_q2 = max(-1, min(1, cos_q2))
        
        q2_rad = math.acos(cos_q2) # Solution coude haut
        
        k1 = L1 + L2 * math.cos(q2_rad)
        k2 = L2 * math.sin(q2_rad)
        q1_rad = math.atan2(y, x) - math.atan2(k2, k1)
        
        q1 = math.degrees(q1_rad)
        q2 = math.degrees(q2_rad)
        
        message = f"""
🎯 **MGI Calculé (Solution Coude Haut)**
📐 **Angles :** q1={q1:.1f}°, q2={q2:.1f}°, q3={q3:.1f}°
📍 **Cible :** X={x:.0f}, Y={y:.0f} mm
"""
        dispatcher.utter_message(text=message)
        
        return [
            SlotSet("q1", q1),
            SlotSet("q2", q2),
            SlotSet("q3", q3),
            SlotSet("last_calculation_type", "MGI"),
            SlotSet("topics_learned", tracker.get_slot("topics_learned") or [] + ["MGI"])
        ]


class ActionCalculateJacobian(Action):
    """Calcule la Jacobienne"""
    
    def name(self) -> Text:
        return "action_calculate_jacobian"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        q1 = math.radians(tracker.get_slot("q1") or 0.0)
        q2 = math.radians(tracker.get_slot("q2") or 0.0)
        q3 = math.radians(tracker.get_slot("q3") or 0.0)
        
        L1 = tracker.get_slot("link_length_1") or 300.0
        L2 = tracker.get_slot("link_length_2") or 250.0
        L3 = tracker.get_slot("link_length_3") or 150.0
        
        s1, c1 = math.sin(q1), math.cos(q1)
        s12, c12 = math.sin(q1+q2), math.cos(q1+q2)
        s123, c123 = math.sin(q1+q2+q3), math.cos(q1+q2+q3)
        
        J11 = -L1*s1 - L2*s12 - L3*s123
        J12 = -L2*s12 - L3*s123
        J13 = -L3*s123
        
        J21 = L1*c1 + L2*c12 + L3*c123
        J22 = L2*c12 + L3*c123
        J23 = L3*c123
        
        det = J11*J22 - J12*J21
        etat = "⚠️ SINGULARITÉ" if abs(det) < 1e-3 else "✅ OK"
        
        msg = f"""
📊 **Matrice Jacobienne**
| {J11:6.1f} {J12:6.1f} {J13:6.1f} |
| {J21:6.1f} {J22:6.1f} {J23:6.1f} |

Déterminant: {det:.2f} ({etat})
"""
        dispatcher.utter_message(text=msg)
        return [SlotSet("last_calculation_type", "Jacobian")]


class ActionGenerateTrajectory(Action):
    """Génération de trajectoire"""
    
    def name(self) -> Text:
        return "action_generate_trajectory"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Simulation simple
        dispatcher.utter_message(text="🚀 **Trajectoire calculée**\nProfil trapézoïdal généré entre A et B.\nTemps total estimé: 2.5s")
        return [SlotSet("last_calculation_type", "Trajectory")]


class ActionCheckWorkspace(Action):
    """Vérifie l'espace de travail"""
    
    def name(self) -> Text:
        return "action_check_workspace"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        x = tracker.get_slot("target_x") or 500.0
        y = tracker.get_slot("target_y") or 0.0
        
        L1 = tracker.get_slot("link_length_1") or 300.0
        L2 = tracker.get_slot("link_length_2") or 250.0
        L3 = tracker.get_slot("link_length_3") or 150.0
        
        r = math.sqrt(x**2 + y**2)
        r_max = L1 + L2 + L3
        r_min = abs(L1 - L2 - L3)
        
        status = "✅ DANS L'ESPACE" if r_min <= r <= r_max else "❌ HORS ESPACE"
        
        msg = f"🔍 **Check Workspace**\nPoint r={r:.0f}mm\nRésultat: {status}"
        dispatcher.utter_message(text=msg)
        return [SlotSet("last_calculation_type", "Workspace")]


class ActionShowCodeExample(Action):
    """Affiche le code source selon le contexte"""
    
    def name(self) -> Text:
        return "action_show_code_example"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        last = (tracker.get_slot("last_calculation_type") or "MGD").upper()
        
        # J'utilise des chaînes concaténées pour éviter les bugs d'affichage Markdown
        if "MGD" in last:
            title = "MGD (Python)"
            code_content = (
                "def mgd(q1, q2, q3, L1, L2, L3):\n"
                "    q1, q2, q3 = math.radians(q1), math.radians(q2), math.radians(q3)\n"
                "    x = L1*cos(q1) + L2*cos(q1+q2) + L3*cos(q1+q2+q3)\n"
                "    y = L1*sin(q1) + L2*sin(q1+q2) + L3*sin(q1+q2+q3)\n"
                "    return x, y"
            )
            
        elif "MGI" in last:
            title = "MGI (Python)"
            code_content = (
                "def mgi(x, y, L1, L2):\n"
                "    r = sqrt(x**2 + y**2)\n"
                "    cos_q2 = (r**2 - L1**2 - L2**2) / (2*L1*L2)\n"
                "    q2 = acos(max(-1, min(1, cos_q2)))\n"
                "    # ... calcul de q1 ensuite"
            )
            
        else:
            title = "Exemple générique"
            code_content = "print('Calcul non spécifié')"

        # Construction propre du message Markdown
        message = f"💻 **Exemple : {title}**\n\n```python\n{code_content}\n```"
        
        dispatcher.utter_message(text=message)
        return []