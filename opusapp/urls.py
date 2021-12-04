from django.urls import path
from .views import indexPageView, searchPageView, resultsPrescriberView, resultsDrugView, prescriberView, drugView, learnView, dashboardView, adminView, adminNewView
urlpatterns = [
    path("", indexPageView, name="index"),
    path("search/", searchPageView, name="search"),
    path("results/prescriber/", resultsPrescriberView, name="results-prescriber"),
    path("results/drug/", resultsDrugView, name="results-drug"),
    path("prescriber/<int:npi>/", prescriberView, name="prescriber"),
    path("prescriber-new/", prescriberView, name="prescriber-new"),
    path("drug/<int:drug_id>/", drugView, name="drug"),
    path("learn/", learnView, name="learn"),
    path("dashboard/", dashboardView, name="dashboard"),
    path("admin/<int:npi>/", adminView, name="admin"),
    path("admin/new/", adminNewView, name="admin-new"),
    path("admin/", adminView, name="admin"),
]
