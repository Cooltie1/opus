from django.shortcuts import render

# Create your views here.
def indexPageView(request) :
    return render(request, 'opusapp/index.html')

def searchPageView(request) :
    return render(request, 'opusapp/search.html')

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