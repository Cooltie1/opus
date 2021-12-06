from django.shortcuts import render

from opusapp.models import State, Prescriber, Drug
from django.db.models.functions import Concat
from django.db.models import Value, F

import requests
import json

# Create your views here.
def indexPageView(request) :
    return render(request, 'opusapp/index.html')

def searchPageView(request) :
    credentialsSQL = 'select distinct 1 NPI, credential from prescriber order by credential'
    specialtySQL = 'select distinct 1 NPI, specialty from prescriber order by specialty'
    context = {
        "state" : State.objects.all(),
        "credentials" : Prescriber.objects.raw(credentialsSQL),
        "specialty" : Prescriber.objects.raw(specialtySQL)
    }

    
    return render(request, 'opusapp/search.html', context)

def resultsPrescriberView(request) :
    fname = request.GET['inputFname']
    lname = request.GET['inputLname']
    credentials = request.GET['inputCredentials']
    gender = request.GET['inputGender']
    state = request.GET['inputState']
    specialty = request.GET['inputSpecialty']
    data = Prescriber.objects.values('npi', 'fname', 'lname'
    ).annotate(id=F('npi'), name=Concat('lname', Value(', '), 'fname')
    ).filter(fname__icontains=fname, lname__icontains=lname, credential__icontains=credentials, gender__icontains=gender, state__state_name__icontains=state, specialty__icontains=specialty
    ).order_by('name')
    context = {
        'data' : data,
        'type' : 'prescriber'

    }

    return render(request, 'opusapp/search-results.html', context)

def resultsDrugView(request) :
    drugname = request.GET['inputDrugName']
    data = Drug.objects.values('drug_id', 'drug_name').annotate(id=F('drug_id'), name=F('drug_name'))
    if 'isOpiate' not in request.GET :
        data = data.filter(drug_name__icontains=drugname)
    else :
        data = data.filter(drug_name__icontains=drugname, is_opioid=True)
    
    data = data.order_by('name')
    
    context = {
        'data' : data,
        'type' : 'drug'
    }


    return render(request, 'opusapp/search-results.html', context)

def prescriberView(request, npi) :

    prescriber = Prescriber.objects.get(npi=npi)

    # Recommender endpoint

    prescriber_drugs = prescriber.prescriberdrug_set.all()

    pd_array = list()

    for drug in prescriber_drugs:
        pd_array.append({"npi": prescriber.npi, "drugname": drug.drug.drug_name, "count": drug.count})

    url = "http://f10c5a45-9edc-4888-8523-31dc6679a174.eastus2.azurecontainer.io/score"

    payload = json.dumps({
    "Inputs": {
        "Triple": pd_array,
        "Prescriber": [
        {
            "npi": prescriber.npi,
            "gender": prescriber.gender,
            "state": prescriber.state.state_abbrev,
            "credentials": prescriber.credential,
            "specialty": prescriber.specialty,
            "isopioidprescriber": prescriber.is_opioid_prescriber
        }
        ],
        "Drug": [
        {
            "drugid": 2,
            "drugname": "ABILIFY",
            "isopioid": "False"
        }
        ]
    },
    "GlobalParameters": {}
    })

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 22E1USKfKxTpWKxgcO0y7e8TmaNzfWAQ'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    json_response = response.json()
    results = json_response['Results']['WebServiceOutput0'][0]
    recommended_drugs = list()

    for v in results.values():
        recommended_drugs.append(v)


    # Classification Endpoint

    url2 = "http://5945a9a0-d5e3-48dd-aabe-14062600c948.eastus2.azurecontainer.io/score"

    payload2 = json.dumps({
    "Inputs": {
        "Prescriber": [
        {
            "gender": prescriber.gender,
            "state": prescriber.state.state_abbrev,
            "credentials": prescriber.credential,
            "specialty": prescriber.specialty
        }
        ]
    },
    "GlobalParameters": {}
    })
    headers2 = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer hPSeYAfReUAocTuFBhOAceV3pIsaeT9w'
    }

    response2 = requests.request("POST", url2, headers=headers2, data=payload2)
    json_response2 = response2.json()
    predicted_prescriber = json_response2['Results']['WebServiceOutput0'][0]['Scored Labels']


    # Regression endpoint

    url3 = "http://5ac3a83a-6af1-4054-8047-e88567f6e85b.eastus2.azurecontainer.io/score"

    payload3 = json.dumps({
    "Inputs": {
        "Prescriber": [
        {
            "gender": prescriber.gender,
            "state": prescriber.state.state_abbrev,
            "credentials": prescriber.credential,
            "specialty": prescriber.specialty
        }
        ]
    },
    "GlobalParameters": {}
    })
    headers3 = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eHUpjMW1d4K6SIK4bg189mvrLhKaK7Hl'
    }

    response3 = requests.request("POST", url3, headers=headers3, data=payload3)
    json_response3 = response3.json()
    predicted_prescriptions = json_response3['Results']['WebServiceOutput0'][0]['Scored Labels']
    predicted_prescriptions = round(predicted_prescriptions, 0)

    context = {
        'prescriber' : prescriber,
        'recommended_drugs': recommended_drugs,
        'predicted_prescriber': predicted_prescriber,
        'predicted_prescriptions': predicted_prescriptions,
    }

    return render(request, 'opusapp/prescriber.html', context)

def drugView(request, drug_id) :

    drug = Drug.objects.get(drug_id=drug_id)

    url = "http://6cead41f-fcfb-465d-aa56-37d12337ca2a.eastus2.azurecontainer.io/score"

    payload = json.dumps({
        "Inputs": {
            "Triple": [{
                "drug_id": 2,
                "npi": 1003016270,
                "count": 15
            }],
            "Prescriber": [{
                "npi": 1003008475,
                "gender": "F",
                "state": "GA",
                "credentials": "NP",
                "specialty": "Nurse Practitioner"
            }],
            "Drug": [{
                "drugid": drug.drug_id,
                "drugname": drug.drug_name,
                "isopioid": str(drug.is_opioid)
            }]
        },
        "GlobalParameters": {}
    })

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer V3ut4SLWIpCa9FNd2impNwMnGGKgtaFJ'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    json_response = response.json()
    results = json_response['Results']['WebServiceOutput0'][0]
    recommended_prescribers = list()

    for v in results.values():
        recommended_prescribers.append(Prescriber.objects.get(npi=v))

    context = {
        'drug' : drug,
        'recommended_prescribers' : recommended_prescribers,
    }

    return render(request, 'opusapp/drug.html', context)

def learnView(request) :
    return render(request, 'opusapp/learn.html')

def dashboardView(request) :
    return render(request, 'opusapp/dashboard.html')

def adminView(request, npi=0) :
    if npi == 0 :
        credentialsSQL = 'select distinct 1 NPI, credential from prescriber order by credential'
        specialtySQL = 'select distinct 1 NPI, specialty from prescriber order by specialty'
        context = {
            "state" : State.objects.all(),
            "credentials" : Prescriber.objects.raw(credentialsSQL),
            "specialty" : Prescriber.objects.raw(specialtySQL)
        }
        return render(request, 'opusapp/admin.html', context)
    else :
        return render(request, 'opusapp/admin-edit.html')
   

def adminNewView(request) :
    if request.method == 'GET' :
        credentialsSQL = 'select distinct 1 NPI, credential from prescriber order by credential'
        specialtySQL = 'select distinct 1 NPI, specialty from prescriber order by specialty'
        context = {
            "state" : State.objects.all(),
            "credentials" : Prescriber.objects.raw(credentialsSQL),
            "specialty" : Prescriber.objects.raw(specialtySQL),
            'message' : ''
        }
        return render(request, 'opusapp/admin-new.html', context)

    elif request.method == 'POST':
        new_npi = request.POST['npi']

        try :
            Prescriber.objects.get(npi = new_npi)

            credentialsSQL = 'select distinct 1 NPI, credential from prescriber order by credential'
            specialtySQL = 'select distinct 1 NPI, specialty from prescriber order by specialty'

            context = {
                'message' : 'Already Exists',
                "state" : State.objects.all(),
                "credentials" : Prescriber.objects.raw(credentialsSQL),
                "specialty" : Prescriber.objects.raw(specialtySQL),
                'npi' : new_npi
            }
            return render(request, 'opusapp/admin-new.html', context)
        except :
            prescriber = Prescriber()
            state = State.objects.get(state_name = request.POST['state'])

            prescriber.npi = request.POST['npi']
            prescriber.fname = request.POST['fname']
            prescriber.lname = request.POST['lname']
            prescriber.credential = request.POST['credential']
            prescriber.gender = request.POST['gender']
            prescriber.state = state
            prescriber.specialty = request.POST['specialty']
            prescriber.is_opioid_prescriber = False
            prescriber.total_prescriptions = 0

            prescriber.save()

            credentialsSQL = 'select distinct 1 NPI, credential from prescriber order by credential'
            specialtySQL = 'select distinct 1 NPI, specialty from prescriber order by specialty'

            context = {
                'message' : 'Added Successfully',
                "state" : State.objects.all(),
                "credentials" : Prescriber.objects.raw(credentialsSQL),
                "specialty" : Prescriber.objects.raw(specialtySQL)
            }

            return render(request, 'opusapp/admin-new.html', context)
    else:
        return render(request, 'opusapp/index.html')