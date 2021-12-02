from django.urls import path
from .views import indexPageView, searchPageView, resultsPrescriberView, resultsPrescriberView, prescriberView, drugView, learnView, dashboardView, adminView
urlpatterns = [
    path("", indexPageView, name="index"),
    path("/search/", searchPageView, name="search"),
    path("/results-prescriber/", resultsPrescriberView, name="results-prescriber"),
    path("/results-drug/", resultsPrescriberView, name="results-drug"),
    path("/prescriber/<int:npi>/", prescriberView, name="prescriber"),
    path("/drug/<int:drugid>/", drugView, name="drug"),
    path("/learn/", learnView, name="learn"),
    path("/dashboard/", dashboardView, name="dashboard"),
    path("/admin/", adminView, name="admin"),
    
]
