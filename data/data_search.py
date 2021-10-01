import json
import pandas as pd
import os
import time
from whoosh.fields import Schema, TEXT, ID
from whoosh import index
from whoosh.qparser import QueryParser
import os.path
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

start_time=time.time()
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
cuisine = "thai"
outdoor = "outdoor"
preferences = ["outdoor", "delivery", "Restaurant"]


print(cuisine, outdoor, preferences)
print("data loaded at: ",time.time()-start_time)


if cuisine is not None:
    cuisine =cuisine.title()

cuisine_match = cuisine == None
outdoor_match = (not outdoor)
preference_match = 0
print(cuisine_match, outdoor_match, preference_match)

data_file = open("../yelp_data/yelp_academic_dataset_business.json", encoding='utf-8')

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))

ix = index.open_dir("indexdir")

"""writer = ix.writer()
counter=0
for line in data_file:
    parsed_line=json.loads(line)
    if parsed_line["categories"] is not None and "Restaurants" in parsed_line["categories"]:
        writer.add_document(title=parsed_line["name"]+"-"+parsed_line["business_id"], content=line,
                    path=parsed_line["business_id"])
        counter+=1
print("writer added at: ",time.time()-start_time, "total", counter)
writer.commit()

print("writer finished at: ",time.time()-start_time)"""

results=[]
search_result = {}
with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse(cuisine)
    results += searcher.search(query, terms=True, limit=None)

    for preference in preferences:
        query = QueryParser("content", ix.schema).parse(preference+": True")
        results += searcher.search(query, terms=True, limit=None)

    for r in results:
        content=json.loads(r["content"])
        business_id=content["business_id"]
        if(business_id not in search_result.keys()):
            search_result[business_id]={"name": content["name"], "score": r.score, "matched_terms": 1}
        else:
            search_result[business_id]["score"] += r.score
            search_result[business_id]["matched_terms"] += 1

search_results=sorted(search_result.values(), key=lambda result: result["score"], reverse=True)
search_results=sorted(search_results, key=lambda result: result["matched_terms"], reverse=True)
print(search_results)