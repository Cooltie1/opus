from django.contrib import admin
from django.db import models
from .models import State, Drug, Prescriber, PrescriberDrug

# Register your models here.
admin.site.register(State)
admin.site.register(Drug)
admin.site.register(Prescriber)
admin.site.register(PrescriberDrug)

