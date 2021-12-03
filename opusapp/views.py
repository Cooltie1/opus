from django.shortcuts import render

from opusapp.models import State, Prescriber, Drug
from django.db.models.functions import Concat
from django.db.models import Value, F

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
    ).filter(fname__icontains=fname, lname__icontains=lname, credential__icontains=credentials, gender__icontains=gender, state__state_name__icontains=state, specialty__icontains=specialty )
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
    
    
    context = {
        'data' : data,
        'type' : 'drug'
    }


    return render(request, 'opusapp/search-results.html', context)

def prescriberView(request, npi) :

    prescriber = Prescriber.objects.get(npi=npi)

    context = {
        'prescriber' : prescriber,
    }

    return render(request, 'opusapp/prescriber.html', context)

def drugView(request, drug_id) :
    return render(request, 'opusapp/drug.html')

def learnView(request) :
    return render(request, 'opusapp/learn.html')

def dashboardView(request) :
    return render(request, 'opusapp/dashboard.html')

def adminView(request) :
    return render(request, 'opusapp/admin.html')

def adminNewView(request) :
    return render(request, 'opusapp/admin-new.html')