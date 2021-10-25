import pickle
dict = {
"ip": "3.21.245.240",
"port": "8983",
"covid_keywords": ["covid19", "corona", "coronavirus","hospital","covidresources","oxygen","stayhomestaysafe","वैश्विकमहामारी","सुरक्षित रहें","संगरोध","मास्क","कोविड मृत्यु","covid19","स्वयं चुना एकांत","डेल्टा संस्करण","covid-19","एंटीबॉडी","दूसरी लहर","distancia social","rt-pcr","sarscov2","sintomas","desinfectante","susanadistancia","cuarentena","asintomático","quedateencasa","covid19","covid","quarentena","staysafe","cdc","virus","pandemia","variante delta","lockdown","positive","stayathome","कोविड","कोविड 19","कोविड-19","workfromhome","autoaislamiento","casos","deltavariant","wearamask","coronawarriors","quedate en casa"],
"vaccine_keywords": ["टीका", "फाइजर", "epavacúnate", "vaccine mandate","टीकाकरण",
"vaccine side effect","vacunación","anticuerpos","eficacia de la vacuna","vacuna covid","vaccination","second dose","first dose","fullyvaccinated","sinovac","एस्ट्राजेनेका","johnson & johnson’s janssen","remdesivir","कोवैक्सीन","moderna","eficacia de la vacuna","vacuna covid","covidvaccine","zycov-d","vaccines","#largestvaccinedrive","vaccination","dosis de vacuna","campaña de vacunación","vaccineshortage","vacunar","covaxine","antibodies","वैक्सीन", "प्रभाव","लसीकरण","completamente vacunado", "novaccinepassports","dosis","mrna vaccine","mandato de vacuna","टीके","campaña de vacunación"],
"core": "IRF21P1"
}
filename = 'project1_index_details.pickle'
with open(filename, 'wb') as f:
    pickle.dump(dict, f, protocol=pickle.HIGHEST_PROTOCOL)

with open(filename, 'rb') as f:
    b = pickle.load(f)

print(dict == b)
