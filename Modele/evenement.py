import json
import codecs

class Event: #class permettant d'entrer dans le json les informations des spectacles

    def __init__(self, genre, name, author, place, date, image, interpret, duration, language, subtitle, preview, low_price,
                 medium_price, premium_price, option_price,k):

        self.genre = genre
        self.name = name
        self.author = author
        self.place = place
        self.date = date
        self.image = image
        self.interpret = interpret
        self.duration = duration
        self.language = language
        self.subtitle = subtitle
        self.preview = preview
        self.low_price = low_price
        self.medium_price = medium_price
        self.premium_price = premium_price
        self.option_price = option_price
        self.k = k

    def write_json(self):
        file = open('./Modele/Evenement.json', 'rb+')  # on passe en binaire par souci de généralisation des données
        tache = json.load(file)
        x = {"Event" + str(self.k): [
            self.genre,
            self.name,
            self.author,
            self.place,
            self.date,
            self.image,
            self.interpret,
            self.duration,
            self.language,
            self.subtitle,
            self.preview,
            self.low_price,
            self.medium_price,
            self.premium_price,
            self.option_price
        ]}
        tache["Event" + str(self.k) ]=x["Event" + str(self.k)]
        file.seek(0)
        json.dump(tache, codecs.getwriter('utf-8')(file), sort_keys=True, indent=4, ensure_ascii=False)
        file.truncate()
        file.close()