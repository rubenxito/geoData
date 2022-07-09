import json
from collections import OrderedDict
from deep_translator import DeepL
from deep_translator import GoogleTranslator

file = open('/Users/antropoloops/Box Sync/PycharmProjects/geoData/jsons/unstatsGeoAreaContinentTree.json')
albumJson = json.load(file)
file2 = open('/Users/antropoloops/Box Sync/PycharmProjects/geoData/jsons/m49-countriesFao.json')
albumJson2 = json.load(file2)

# json with country as title
m49CountriesDict = {}
for x in albumJson2:
    countryName = x["country_name_en"]
    m49CountriesDict[countryName] = x
# list with country names
m49CountriesList = []
for country in m49CountriesDict:
    m49CountriesList.append(country)
print('m49CountriesList///////', len(m49CountriesList)) #m49CountriesList)
# print(m49Countries['Antarctica'])

worldCountriesDict = {}
# print(json.dumps(albumJson, indent=4, sort_keys=True))
continents = albumJson['children']
for continent in continents:
    print('/ continent', continent['geoAreaName'])
    if continent['children']:
        subregions1 = continent['children']
        for subregion1 in subregions1:
            print('// subregion1', subregion1['geoAreaName'])
            if subregion1['children']:
                subregions2 = subregion1['children']
                for subregion2 in subregions2:
                    if subregion2['type'] == 'Region':
                        print('/// subregion2', subregion2['geoAreaName'])
                        if subregion2['geoAreaName'] == 'Channel Islands':
                            countries = subregion2['children']
                            for item in countries:
                                country = item['geoAreaName']
                                print('------', country)
                                worldCountriesDict[country] = item
                                worldCountriesDict[country]['subregion'] = subregion1['geoAreaName']
                                # worldCountriesDict[country]['subregion2'] = subregion2['geoAreaName']
                                worldCountriesDict[country]['continent'] = continent['geoAreaName']
                                if item['children']:
                                    pass
                        if subregion2['geoAreaName'] == 'Southern Asia (excluding India)':
                            pass
                        else:
                            countries = subregion2['children']
                            for item in countries:
                                country = item['geoAreaName']
                                print('------', country)
                                worldCountriesDict[country] = item
                                worldCountriesDict[country]['subregion'] = subregion2['geoAreaName']
                                # worldCountries[country]['subregion2'] = subregion2['geoAreaName']
                                worldCountriesDict[country]['continent'] = continent['geoAreaName']
                                if item['children']:
                                    pass
                    if subregion2['type'] == 'Country':
                        country = subregion2['geoAreaName']
                        print('------', country)
                        worldCountriesDict[country] = subregion2
                        worldCountriesDict[country]['subregion'] = subregion1['geoAreaName']
                        worldCountriesDict[country]['continent'] = continent['geoAreaName']

                        if subregion2['children']:
                            pass
# print(len(worldCountries), worldCountries)
# print(json.dumps(worldCountries, indent=4, sort_keys=True))

# list with country names
worldCountriesList = []
for dict in worldCountriesDict:
    worldCountriesList.append(dict)
    # print(worldCountries[dict])
    # print(dict.geoAreaCode)
    #### DELETE keys
    del worldCountriesDict[dict]['children']
    del worldCountriesDict[dict]['type']
print()
print('worldCountriesList/////', len(worldCountriesList))#, worldCountriesList)
print()
missingCountries = list(set(worldCountriesList) - set (m49CountriesList))
print('>>>>>>> MISSING countries', len(missingCountries), missingCountries)
print()
# print(GoogleTranslator.get_supported_languages())
missingCountriesDict = {}
for missingcountry in missingCountries:
    missingCountriesDict[missingcountry] = worldCountriesDict[missingcountry]
    missingCountriesDict[missingcountry]['country_name_ar'] = GoogleTranslator(source='auto', target='ar').translate(missingcountry)
    missingCountriesDict[missingcountry]['country_name_en'] = missingcountry
    missingCountriesDict[missingcountry]['country_name_es'] = GoogleTranslator(source='auto', target='es').translate(missingcountry)
    missingCountriesDict[missingcountry]['country_name_fr'] = GoogleTranslator(source='auto', target='fr').translate(missingcountry)
    missingCountriesDict[missingcountry]['country_name_ru'] = GoogleTranslator(source='auto', target='ru').translate(missingcountry)
    missingCountriesDict[missingcountry]['country_name_zh'] = GoogleTranslator(source='auto', target='zh-CN').translate(missingcountry)
    missingCountriesDict[missingcountry]['ISO3'] = ''
for dict in missingCountriesDict.values():
    del dict['geoAreaName']
    dict['geoAreaCodeM49'] = dict.pop('geoAreaCode')

with open('jsons/tmp/missingCountriesDict.json', 'w') as fp:
    json.dump(missingCountriesDict, fp, sort_keys=True, indent=4, ensure_ascii=False)

# # otro omdo de enumerate
# for i in range(len(m49CountriesList)):
#     item = m49CountriesList[i]
#     if i == 0:
#         print('////////', m49CountriesList[0])


mergedDict = {}
countriesProblemsList = []
# worldCountriesAll = {}
for m49country in m49CountriesList:
    try:
        d1 = worldCountriesDict[m49country]
        d2 = m49CountriesDict[m49country]
        # print('>>>>>>>>>>>>>>', d2)
        mergedDict[m49country] = {**d1, **d2}
        # d3 = d1 | d2
    except:
        countriesProblemsList.append(m49country)

print('countriesProblemsList', len(countriesProblemsList),  countriesProblemsList)
print(len(mergedDict), 'items in mergedDict')

countriesProblemsDict = {}
for problemCountry in countriesProblemsList:
    countriesProblemsDict[problemCountry] = m49CountriesDict[problemCountry]
    countriesProblemsDict[problemCountry]['continent'] = ''
    countriesProblemsDict[problemCountry]['subregion '] = ''
for dict in countriesProblemsDict.values():
    dict['geoAreaCodeM49'] = dict.pop('m49')
with open('jsons/tmp/countriesProblemsDict.json', 'w') as fp:
    json.dump(countriesProblemsDict, fp, sort_keys=True, indent=4, ensure_ascii=False)

# change key names in nested dicts
# key_list = ["country_name_en","country_name_es","country_name_ar","country_name_fr", "country_name_ru","country_name_zh","continent","subregion", "geoAreaCodeM49","ISO3"]
for dict in mergedDict.values():
    del dict['m49']
    del dict['geoAreaName']
    dict['geoAreaCodeM49'] = dict.pop('geoAreaCode')
    # new_dict = OrderedDict((k, dict[k]) for k in key_list)
    # print(new_dict)

with open('m49countriesFULL.json', 'w') as fp:
    json.dump(mergedDict, fp, sort_keys=True, indent=4, ensure_ascii=False)


worldCountriesAll = mergedDict | countriesProblemsDict | missingCountriesDict
print(len(worldCountriesAll), 'items in worldCountriesAll')
with open('worldCountriesAll.json', 'w') as fp:
    json.dump(worldCountriesAll, fp, sort_keys=True, indent=4, ensure_ascii=False)
# get allows to detect errors if key doesn't exists
# print(mergedDict.get('Albania', 'noexiste'))

# print(worldCountries)
# print(json.dumps(worldCountries, indent=4, sort_keys=True))



