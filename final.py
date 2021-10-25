import requests
import pickle

payload = pickle.load(open("project1_index_details.pickle", "rb"))
res = requests.post("http://54.89.143.10:9999/grade_index", json=payload, timeout=600)
res = res.json()
print(res)

