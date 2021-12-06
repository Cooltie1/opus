from django.urls import path
from .views import indexPageView, searchPageView, resultsPrescriberView, resultsDrugView, prescriberView, drugView, learnView, dashboardView, adminView, adminNewView, editPrescriberView, savePrescriberView, deletePageView
urlpatterns = [
    path("", indexPageView, name="index"),
    path("search/", searchPageView, name="search"),
    path("results/prescriber/", resultsPrescriberView, name="results-prescriber"),
    path("results/drug/", resultsDrugView, name="results-drug"),
    path("prescriber/<int:npi>/", prescriberView, name="prescriber"),
    path("drug/<int:drug_id>/", drugView, name="drug"),
    path("learn/", learnView, name="learn"),
    path("dashboard/", dashboardView, name="dashboard"),
    path("admin/<int:npi>/", adminView, name="admin"),
    path("admin/new/", adminNewView, name="admin-new"),
    path("editprescriber/<int:npi>/", editPrescriberView, name="prescriber-edit"),
    path("updateprescriber/<int:npi>/", savePrescriberView, name="saveprescriber"),
    path("delete/<int:npi>/", deletePageView, name="delete"),
    path("admin/", adminView, name="admin"),
]
