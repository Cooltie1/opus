from django.shortcuts import render

from opusapp.models import State, Prescriber

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
    return render(request, 'opusapp/search-results.html')

def resultsDrugView(request) :
    return render(request, 'opusapp/search-results.html')

def prescriberView(request, npi) :
    return render(request, 'opusapp/prescriber.html')

def drugView(request, drugid) :
    return render(request, 'opusapp/drug.html')

def learnView(request) :
    return render(request, 'opusapp/learn.html')

def dashboardView(request) :
    return render(request, 'opusapp/dashboard.html')

def adminView(request) :
    return render(request, 'opusapp/admin.html')

def adminNewView(request) :
    return render(request, 'opusapp/admin-new.html')