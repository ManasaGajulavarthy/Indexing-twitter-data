'''
@author: Souvik Das
Institute: University at Buffalo
'''

import json
import datetime
import pandas as pd
from twitter import Twitter
from tweet_preprocessor import TWPreprocessor
from indexer import Indexer
from os.path import exists
import pickle

reply_collection_knob = True


def read_config():
    with open("config.json") as json_file:
        data = json.load(json_file)

    return data


def write_config(data):
    with open("config.json", 'w') as json_file:
        json.dump(data, json_file)


def save_file(data, filename):
    df = pd.DataFrame(data)
    df.to_pickle("data/" + filename)


def read_file(type, id):
    return pd.read_pickle(f"data/{type}_{id}.pkl")


def main():
    config = read_config()
    indexer = Indexer()
    twitter = Twitter()

    pois = config["pois"]
    keywords = config["keywords"]
    tweet_ids_poi = {}
    tweet_ids_keyword = {}

    for i in range(len(pois)):
        if pois[i]["finished"] == 0:
            print(f"---------- collecting tweets for poi: {pois[i]['screen_name']}")

            raw_tweets = twitter.get_tweets_by_poi_screen_name(pois[i]["screen_name"], pois[i]["count"])  # pass args as needed

            processed_tweets = []
            for tw in raw_tweets:
                #tweet_ids_poi[tw.id_str] = [tw.id_str, pois[i]["screen_name"]]
                processed_tweets.append(TWPreprocessor.preprocess(tw, 'poi', pois[i]["country"]))

            indexer.create_documents(processed_tweets)

            pois[i]["finished"] = 1
            pois[i]["collected"] = len(processed_tweets)

            write_config({
                "pois": pois, "keywords": keywords
            })

            save_file(processed_tweets, f"poi_{pois[i]['id']}.pkl")
            print("------------ process complete -----------------------------------")

    for i in range(len(keywords)):
        if keywords[i]["finished"] == 0:
            print(f"---------- collecting tweets for keyword: {keywords[i]['name']}")

            raw_tweets = twitter.get_tweets_by_lang_and_keyword(keywords[i]['name'], keywords[i]['count'], keywords[i]['lang'])  # pass args as needed

            processed_tweets = []
            for tw in raw_tweets:
                #tweet_ids_keyword[tw.id_str] = [tw.id_str, tw.user.name]
                processed_tweets.append(TWPreprocessor.preprocess(tw, 'keyword', keywords[i]['country']))

            indexer.create_documents(processed_tweets)

            keywords[i]["finished"] = 1
            keywords[i]["collected"] = len(processed_tweets)

            write_config({
                "pois": pois, "keywords": keywords
            })

            save_file(processed_tweets, f"keywords_{keywords[i]['id']}.pkl")

            print("------------ process complete -----------------------------------")

    if reply_collection_knob:
        # Write a driver logic for reply collection, use the tweets from the data files for which the replies are to collected.
        processed_tweets = []
        i = 15
        filename = "data/"+"poi_"+str(i)+".pkl"
        if exists(filename):
            infile = open(filename, 'rb')
            new_dict = pickle.load(infile)
            ids = []
            covid_keywords = ["covid19", "corona", "coronavirus","hospital","covidresources","oxygen","stayhomestaysafe","वैश्विकमहामारी","सुरक्षित रहें","संगरोध","मास्क","कोविड मृत्यु","covid19","स्वयं चुना एकांत","डेल्टा संस्करण","covid-19","एंटीबॉडी","दूसरी लहर","distancia social","rt-pcr","sarscov2","sintomas","desinfectante","susanadistancia","cuarentena","asintomático","quedateencasa","covid19","covid","quarentena","staysafe","cdc","virus","pandemia","variante delta","lockdown","positive","stayathome","कोविड","कोविड 19","कोविड-19","workfromhome","autoaislamiento","casos","deltavariant","wearamask","coronawarriors","quedate en casa"]
            vaccine_keywords=  ["टीका", "फाइजर", "epavacúnate", "vaccine mandate","टीकाकरण",
                                "vaccine side effect","vacunación","anticuerpos","eficacia de la vacuna","vacuna covid","vaccination","second dose","first dose","fullyvaccinated","sinovac","एस्ट्राजेनेका","johnson & johnson’s janssen","remdesivir","कोवैक्सीन","moderna","eficacia de la vacuna","vacuna covid","covidvaccine","zycov-d","vaccines","#largestvaccinedrive","vaccination","dosis de vacuna","campaña de vacunación","vaccineshortage","vacunar","covaxine","antibodies","वैक्सीन", "प्रभाव","लसीकरण","completamente vacunado", "novaccinepassports","dosis","mrna vaccine","mandato de vacuna","टीके","campaña de vacunación"]
            # for text, id in zip(new_dict['tweet_text'],new_dict['id']):
            #     for word, word1 in zip(covid_keywords,vaccine_keywords):
            #         if word in text or word1 in text:
            #             if id not in ids:
            #                 ids.append(id)
            raw_tweets = (twitter.get_replies(new_dict['id'], new_dict['poi_name'][0]))
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw, 'reply'))
            indexer.create_documents(processed_tweets)
            infile.close()

if __name__ == "__main__":
    main()
