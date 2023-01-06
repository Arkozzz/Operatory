#sauvegarde chargement edition

from Modele.payment import *

articles=[]

def controller_articles(): #retourne la valeur des articles
    return articles

def controller_get_article(num): #retourne la valeur d'un article précis parmis les articles (sous liste de liste)
    return articles[num]

def controller_payment_manage(card_number, date, cryptogram, mail, price, title, concert_date): #récupère les informations bancaires, les crypte et les sauvegarde.
    payment_object = Payment(card_number, date, cryptogram, mail)
    payment_object.encryption_data()
    payment_object.write_json()
    payment_object.send_mail(mail, price, title, concert_date)

def controller_load_json(): #charger le json
    global articles
    with open('./Modele/Evenement.json', "r", encoding='utf-8') as file:
        data = json.load(file)

    articles = list(data.values())

def controller_save_json(): #enregistrer le json
    data = {}
    for i in range(len(articles)):
        data['Event%i'%i]  = articles[i]

    with open('./Modele/Evenement.json', "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def controller_empty_article(): #crée un article totalement vide afin d'y ajouter des éléments

    article = [""]*15
    articles.append(article)
    return article

def uml():
    pass

uml()
    
