from django.shortcuts import render
import requests
import json
from datetime import datetime,timedelta

url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "f7de9c9031mshc6181de5aca69b3p1f88a8jsn8140b4cacc69",
    }

response = requests.request("GET", url, headers=headers).json()

def precentgeChange(latest,previous):
    try:
        percentage = (int(latest)-int(previous))/int(latest)*100
    except ZeroDivisionError:
        return 0
    return '+'+str(round(percentage,2)) if percentage>0 else round(percentage,2)

def getDayBeforePercentage(selectedCountry,countryList,latestData):

    url = "https://covid-193.p.rapidapi.com/history"
    country  = "All"
    day = datetime.now().date()-timedelta(days=1)
    queryString = {"country":selectedCountry,"day":day}

    dayBeforeResponse = requests.request("GET", url, headers=headers,params=queryString).json()
    dayBeforeData = getData(dayBeforeResponse,0,countryList)
    new = precentgeChange(latestData['new'],dayBeforeData['new'])
    active = precentgeChange(latestData['active'],dayBeforeData['active'])
    critical = precentgeChange(latestData['critical'],dayBeforeData['critical'])
    recovered = precentgeChange(latestData['recovered'],dayBeforeData['recovered'])
    total = precentgeChange(latestData['total'],dayBeforeData['total'])
    deaths = precentgeChange(latestData['deaths'],dayBeforeData['deaths'])

    return {'selectedcountry':selectedCountry ,'mylist':countryList,'new':new,'active':active,'critical':critical,'recovered':recovered,'deaths':deaths,'total':total}


def getData(response,index,countryList):

    ''' Function to get Data of particular country from response and return the dictionary '''

    try:
        new = response['response'][index]['cases']['new'] if response['response'][index]['cases']['new'] else 0
        active = response['response'][index]['cases']['active'] if response['response'][index]['cases']['active'] else 0
        critical = response['response'][index]['cases']['critical'] if response['response'][index]['cases']['critical'] else 0
        recovered = response['response'][index]['cases']['recovered'] if response['response'][index]['cases']['recovered'] else 0
        total = response['response'][index]['cases']['total'] if response['response'][index]['cases']['total'] else 0
        deaths = int(total) - int(active)-int(recovered)
        return {'new':new,'active':active,'critical':critical,'recovered':recovered,'deaths':deaths,'total':total}
    except:
        return  {'new':0,'active':0,'critical':0,'recovered':0,'deaths':0,'total':0}

def index(request):

    countryList = []
    noOfResults = int(response['results'])
    allStatIndex = 0
    
    for x in range(0, noOfResults):
        countryList.append(response['response'][x]['country'])
        if response['response'][x]['country']=='All':
            allStatIndex = x

    countryList.sort()

    if request.method=="POST":
        selectedCountry = request.POST['selectedcountry']
        for x in range(0,noOfResults):
            if selectedCountry == response['response'][x]['country']:
                latestData = getData(response,x,countryList)
                dayBeforeData = getDayBeforePercentage(selectedCountry,countryList,latestData)
                context = {'selectedcountry':selectedCountry ,'mylist':countryList,'latestData':latestData,'dayBeforeData':dayBeforeData}
        return render(request, 'index.html', context)

    # get total data of all worldwide and render at start 
    latestData = getData(response,allStatIndex,countryList) 
    dayBeforeData = getDayBeforePercentage('All',countryList,latestData)
    context = {'selectedcountry':'All' ,'mylist':countryList,'latestData':latestData,'dayBeforeData':dayBeforeData}
    return render(request,'index.html',context)

    