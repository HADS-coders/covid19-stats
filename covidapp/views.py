from django.shortcuts import render
import requests
import json

url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "d9cbda2f6dmshc2bba4bd0e71c1ap1ab42fjsnc01c43dd2e87",
    }

response = requests.request("GET", url, headers=headers).json()

def getData(index,countryList):

    ''' Function to get Data of particular country from response and return the dictionary '''

    selectedCountry = response['response'][index]['country']
    new = response['response'][index]['cases']['new'] if response['response'][index]['cases']['new'] else 0
    active = response['response'][index]['cases']['active'] if response['response'][index]['cases']['active'] else 0
    critical = response['response'][index]['cases']['critical'] if response['response'][index]['cases']['critical'] else 0
    recovered = response['response'][index]['cases']['recovered'] if response['response'][index]['cases']['recovered'] else 0
    total = response['response'][index]['cases']['total'] if response['response'][index]['cases']['total'] else 0
    deaths = int(total) - int(active)-int(recovered)
    return {'selectedcountry':selectedCountry ,'mylist':countryList,'new':new,'active':active,'critical':critical,'recovered':recovered,'deaths':deaths,'total':total}


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
        selectedcountry = request.POST['selectedcountry']
        for x in range(0,noOfResults):
            if selectedcountry == response['response'][x]['country']:
                context=getData(x,countryList)
        return render(request, 'index.html', context)

    # get total data of all worldwide and render at start 
    context = getData(allStatIndex,countryList) 
    return render(request,'index.html',context)

    