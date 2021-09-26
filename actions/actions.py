from typing import Dict, Text, Any, List, Union
import json
import pandas as pd
from rasa_sdk import Tracker
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset
import os
import json
import pandas as pd
import os
import time
from whoosh.fields import Schema, TEXT, ID
from whoosh import index
from whoosh.qparser import QueryParser
import os.path

CUISINE_TYPE = [
    "qmerican",
    "thai",
    "mediterranean",
    "greek",
    "mexican",
    "indian",
    "chinese",
    "caribbean",
    "puerto rican",
    "taiwanese",
    "vietnamese",
    "korean",
    "japanese",
    "canadian",
    "brazilian",
    "cuban",
    "german",
    "african",
    "southern",
    "asian fusion",
    "french",
    "middle eastern",
    "persian",
    "iranian",
    "latin american",
    "filipino",
    "halal",
    "irish",
    "lebanese",
    "russian",
    "colombian",
    "portuguese",
    "venezuelan",
    "ethiopian",
    "malaysian",
    "italian",
    "hungarian",
    "british",
    "salvadoran",
    "cantonese",
    "spanish",
    "argentine",
    "dominican",
    "cambodian",
    "singaporean",
    "szechuan",
    "mexican",
    "indonesian",
    "laotian",
    "mongolian",
    "moroccan",
    "honduran",
    "arabian",
    "belgian",
    "afghan",
    "south African",
    "polish",
    "egyptian",
    "ukrainian",
    "armenian",
    "shanghainese"
    "scottish",
    "Australian",
    "Scandinavian",
    "Czech/Slovakian",
    "Calabrian",
    "Nicaraguan",
    "Catalan",
    "Sardinian",
    "Iberian",
]


class ActionRecordPreferences(Action):

    def name(self):
        return "action_record_preferences"

    def run(self, dispatcher, tracker, domain):
        values = tracker.get_latest_entity_values("preference")
        existing_preferences = tracker.get_slot("preferences")
        print("existing: ", existing_preferences)
        events = []
        for value in values:
            print("Current value", value)
            if value.lower() in CUISINE_TYPE:
                events += [SlotSet("cuisine", value)]
            else:
                existing_preferences += [value]
                events += [SlotSet("preferences", existing_preferences)]
        return events


class ActionModifyPreferences(Action):

    def name(self):
        return "action_modify_preferences"

    def run(self, dispatcher, tracker, domain):
        values = tracker.get_latest_entity_values("preference")
        existing_preferences = tracker.get_slot("preferences")
        events = []
        for value in values:
            print("Current value", value)
            if value.lower() in CUISINE_TYPE:
                events += [SlotSet("cuisine", value)]
            else:
                existing_preferences += [value]
                events += [SlotSet("preferences", existing_preferences)]
        return events


class ActionGiverecommendation(Action):
    def name(self) -> Text:
        return "action_give_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cuisine = tracker.get_slot("cuisine")
        if cuisine is not None:
            cuisine = cuisine.title()
        preferences = tracker.get_slot("preferences")
        print(cuisine, preferences)

        ix = index.open_dir("C:/Users/huang/Documents/Tianqi Huang/Research/Thesis/Rasa/data/indexdir")
        results = []
        search_result = {}
        with ix.searcher() as searcher:
            query = QueryParser("content", ix.schema).parse(cuisine)
            results += searcher.search(query, terms=True, limit=None)

            for preference in preferences:
                query = QueryParser("content", ix.schema).parse(preference+": True")
                results += searcher.search(query, terms=True, limit=None)

            for r in results:
                content = json.loads(r["content"])
                business_id = content["business_id"]
                if (business_id not in search_result.keys()):
                    search_result[business_id] = {"name": content["name"], "score": r.score, "matched_terms": 1}
                else:
                    search_result[business_id]["score"] += r.score
                    search_result[business_id]["matched_terms"] += 1
            search_results = sorted(search_result.values(), key=lambda result: result["score"], reverse=True)
            search_results = sorted(search_results, key=lambda result: result["matched_terms"], reverse=True)
        print(search_results[:10])
        if(len(search_results)==0):
            dispatcher.utter_message(text="Nothing found")
        else:
            dispatcher.utter_message(text=search_results[0]["name"]+ " matched "+ str(search_results[0]["matched_terms"])+ " of your preferences")
        return [AllSlotsReset()]
