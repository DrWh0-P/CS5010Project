'''
Created on Aug 9, 2015

@author: akshat
'''

import requests
from xml.etree import ElementTree

indicator_map = {15:"Obesity", 13:"Smoking", 25:"Primary_Care", 34:"College_Degrees", 23:"No_Insurance", 10003:"Median_Household_Income", 51:"Liquor_Stores", 48:"Healthy_Food_Outlets", 200:"Long_Term_Care_Hospital_Admissions",35:"Unemployed_Persons",50011:"Diabetes_Deaths", 486:"Cancer_Deaths", 83:"Heart_Disease_Deaths", 935:"HIV_Deaths" }
county_map = {}
auth = "Key=5346643abe134855907383ecf8bd7db0"

def populate_county_map():
    f = open("FPS_county_mapping.txt","r")
    for line in f.readlines():
        if "\t" in line:
            county_map["51"+line.strip().split("\t")[1]] = line.strip().split("\t")[0]
        
populate_county_map()

f = open("indicators.csv","w")
for ind in indicator_map:
    response = requests.get("http://services.healthindicators.gov/v5/REST.svc/IndicatorDescription/" + str(ind) +"/Indicators/PageCount?" + auth)
    if response.status_code == 200:
        tree = ElementTree.fromstring(response.content)
        page_count = str(tree.find('Data').text)
        for i in range(1,int(page_count)):
            url = "http://services.healthindicators.gov/v5/REST.svc/IndicatorDescription/" + str(ind) +"/Indicators/" +str(i)+ "?" + auth
            response = requests.get(url)
            if response.status_code == 200:
                    tree = ElementTree.fromstring(response.content)
                    data = tree.find('Data')
                    for indicator in data.findall('Indicator'):
                        fips = str(indicator.find('FIPSCode').text).strip()
                        if  fips.startswith('51') and len(fips)==5 and str(indicator.find('DimensionGraphHeader').text).lower() == 'total':
                            #(indicator_map.get(ind)+ "," + county_map.get(str(indicator.find('FIPSCode').text).strip()) + "," + str(indicator.find('FloatValue').text) + "," + timeframe_map.get(str(indicator.find('TimeframeID').text).strip()) + "\n")
                            f.write(indicator_map.get(ind)+ "," + county_map.get(str(indicator.find('FIPSCode').text).strip()) + "," + "0" if str(indicator.find('FloatValue').text) is None else str(indicator.find('FloatValue').text).strip() +"\n")
                            
                            
f.close()
                         
                        
                