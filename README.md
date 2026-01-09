docker run -v TONCHEMIN/chatbotV0/actions:/app/actions --net rasa-network --name action-server-sri5a rasa/rasa-sdk:2.8.3

docker start action-server-sri5a



docker run -it -v TONCHEMIN/chatbotV0:/app --net rasa-network rasa/rasa:2.8.34-full train



Lancer le dernier modele:


docker run -it -v TONCHEMIN/chatbotV0:/app --net rasa-network rasa/rasa:2.8.34-full shell

