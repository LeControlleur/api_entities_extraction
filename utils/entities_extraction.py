from dotenv import load_dotenv
import os
import textrazor
from wikidata.client import Client
import wikidata
import urllib
import re
import datetime
import threading
import sys
sys.path.append(os.path.join(os.getcwd()))
from utils.statistics_analysis import age_calculator, stats_recording


load_dotenv()

API_KEY_TEXT_RAZOR = os.getenv('API_KEY_TEXT_RAZOR')

textrazor.api_key = API_KEY_TEXT_RAZOR


#   Informations qui seront recherchées au sujet des personnes identifiées
infosToFetch = [
    "full name",
    "birth name",
    "given name",
    "surname",
    "country of citizenship",
    "place of birth",
    "place of death",
    "spouse",
    "child",
    "occupation",
    "date of birth",
    "date of death",
    "age",
    "image"
]


def entities_extraction(text: str) -> list:
    """
    Cette fonction a pour objectif d'extraire les entités présnetes dans le texte passé en paramètre.

    Params:
        text : str
            Texte duquel doit être extraites les entités

    Returns:
        list
            Liste des entités identifiées

    """

    wikidataClient = Client()

    try:
        #   Vérification des paramètres
        if text == "":
            raise (Exception("Missing text"))

        if type(text) != str:
            raise (Exception("Please, provide a text for entities extraction"))

        #   Extraction des entités
        textrazorClient = textrazor.TextRazor(extractors=["entities"])
        response = textrazorClient.analyze(text)

        #   Sélection des entitées correspondates à des personnes
        persons = list(
            filter(lambda x: "Person" in x.dbpedia_types, response.entities()))

        results = []

        #   Enrichissement des infos liées aux personnes
        for person in persons:
            data = wikidataClient.get(person.wikidata_id, load=True)
            add_data = {}
            add_data["full name"] = person.id
            localInfosToFetch = len(infosToFetch)
            for ind in iter(data.attributes["claims"].keys()):
                if localInfosToFetch == 0 :
                    break
                #   Recherche d'informations complémentaires
                info_prop = wikidataClient.get(ind)
                info = data[info_prop]
                label = str(info_prop.label)

                #   Traitement des infos complémentaires en fonction de leur type
                if label in infosToFetch[1:] and label != "image":
                    if label != "image":
                        new_val = None
                        if type(info) == wikidata.multilingual.MonolingualText:
                            new_val = str(info)
                        elif type(info) == wikidata.entity.Entity:
                            new_val = str(info.label)
                        elif type(info) == datetime.date:
                            new_val = info.strftime("%m/%d/%Y")

                        if label in add_data.keys():
                            if add_data[label] != list :
                                add_data[label] = [ add_data[label] ]
                            add_data[label].append(new_val)
                        else:
                            add_data[label] = new_val
                            localInfosToFetch -= 1

                    #   Ajout de l'URL d'une image
                    elif label == "image" and "image" not in add_data.keys():
                        image_url = ""
                        try:
                            image_url = info.image_url
                            if is_image(image_url):
                                add_data[label] = image_url
                                localInfosToFetch -= 1
                        except AttributeError:
                            continue

            if "date of birth" not in add_data.keys():
                add_data["age"] = 0
            elif "date of death" not in add_data.keys():
                add_data["age"] = age_calculator(add_data["date of birth"], "")
            else:
                add_data["age"] = age_calculator(add_data["date of birth"], "date of death")
            
            #   Stats recors on another thread
            th = threading.Thread(target=stats_recording, args=[add_data])
            th.start()
            results.append(add_data)

        return results


    #   Gestion des Exceptions
    except textrazor.TextRazorAnalysisException as e:
        return {
            "message": "Error while extracting entities"
        }

    except Exception as e:
        return {
            "message": str(e)
        }



def is_image(url):
    r = None
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'}))
    except:
        return False
    content_type = r.getheader("Content-Type")
    if re.match("image*", content_type):
        return True
    return False


if __name__ == "__main__":
    texte = "Joe Biden is the US president"
    results = entities_extraction(texte)
    print(results)

