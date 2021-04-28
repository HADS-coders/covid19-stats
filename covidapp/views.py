from django.shortcuts import render
import requests
import json
url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "d9cbda2f6dmshc2bba4bd0e71c1ap1ab42fjsnc01c43dd2e87",

    }

response = requests.request("GET", url, headers=headers).json()


# Create your views here.

## Function to get Data from response and return the dictionary
def getData(index,countryList):
    selectedCountry=response['response'][index]['country']
    new=response['response'][index]['cases']['new']
    active=response['response'][index]['cases']['active']
    critical=response['response'][index]['cases']['critical']
    recovered=response['response'][index]['cases']['recovered']
    total=response['response'][index]['cases']['total']
    deaths= int(total) - int(active)-int(recovered)
    return {'selectedcountry':selectedCountry ,'mylist':countryList,'new':new,'active':active,'critical':critical,'recovered':recovered,'deaths':deaths,'total':total}


def index(request):

    countryList = []
    context={}
    noofresults = int(response['results'])
    for x in range(0, noofresults):
        countryList.append(response['response'][x]['country'])

    if request.method=="POST":
        selectedcountry = request.POST['selectedcountry']
        print(selectedcountry)
        noofresults = int(response['results'])
        for x in range(0,noofresults):
            if selectedcountry==response['response'][x]['country']:
                context=getData(x,countryList)
        return render(request, 'index.html', context)

    elif noofresults>1:
        context=getData(0,countryList)
        return render(request,'index.html',context)

    context={'mylist': countryList}
    return render(request,'index.html',context)

    