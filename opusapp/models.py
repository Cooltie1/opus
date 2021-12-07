from django.db import models

class State(models.Model) :
    state_abbrev = models.CharField(max_length=2, primary_key=True)
    state_name = models.CharField(max_length=15)
    # Make population a big int field
    population = models.IntegerField()
    deaths = models.IntegerField()

    class Meta() :
        db_table = 'state'

    def __str__(self) :
        return self.state_name

class Drug(models.Model) :
    drug_id = models.IntegerField(primary_key=True)
    drug_name = models.CharField(max_length=50)
    is_opioid = models.BooleanField()

    class Meta() :
        db_table = 'drug'

    def __str__(self) :
        return self.drug_name

class Prescriber(models.Model) :
    npi = models.BigIntegerField(primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING, db_column='state')
    credential = models.CharField(max_length=25, blank=True)
    specialty = models.CharField(max_length=50)
    is_opioid_prescriber = models.BooleanField()
    total_prescriptions = models.IntegerField()

    prescriber_drugs = models.ManyToManyField(Drug, through='PrescriberDrug')

    class Meta() :
        db_table = 'prescriber'

    def getName(self) :
        return self.lname + ', ' + self.fname

    def __str__(self) :
        return self.getName()

class PrescriberDrug(models.Model) :
    # id = models.IntegerField(primary_key=True)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, db_column='drug_id')
    prescriber = models.ForeignKey(Prescriber, on_delete=models.CASCADE, db_column='npi')
    count = models.IntegerField()

    class Meta() :
        db_table = 'prescriber_drug'

    def __str__(self) :
        return self.prescriber.getName() + ' ' + self.drug.drug_name + ': ' + str(self.count)
