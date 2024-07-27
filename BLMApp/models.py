from django.db import models
import datetime
import os
import random
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your models here.

def getFileName(request, fileName):
    currentTime = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    newFileName = "%s-%s"%(currentTime, fileName)
    return os.path.join('static/uploads/', newFileName)

def getProfileImageKYC(instance, fileName):
    currentTime = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
    newFileName = f"{instance.first_name}_{instance.last_name}-{currentTime}_{fileName}"
    return os.path.join('static/uploads/IDProof/Profiles', newFileName)

def getIdProofFile(instance, fileName):
    currentTime = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
    newFileName =  f"{instance.first_name}_{instance.last_name}-{currentTime}_{instance.id_proof_type}"
    return os.path.join('static/uploads/IDProof/Documents', newFileName)


class LoanTypes(models.Model):
    loan_type = models.CharField(max_length=50, null=False, blank=False)
    loan_description = models.CharField(max_length=150, null=False, blank=False)
    loan_image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    max_loan_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return self.loan_type

class LoanPlans(models.Model):
    loan_type = models.ForeignKey(LoanTypes, on_delete=models.CASCADE, null=False, blank=False)
    loan_plan_duration_months = models.IntegerField(null=False, blank=False)
    # Converting months to years
    loan_plan_duration_years = models.DecimalField(max_digits=4, decimal_places=1, null=False, blank=False, editable=False)
    loan_interest_rate = models.DecimalField(max_digits=3, decimal_places=2, null=False, blank=False)

    def save(self, *args, **kwargs):
        self.loan_plan_duration_years = round(self.loan_plan_duration_months / 12, 1)
        super(LoanPlans, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.loan_type} with {self.loan_interest_rate}% interest for {self.loan_plan_duration_months} months ({self.loan_plan_duration_years} years)"

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('others', 'Others'),
)

MARTIAL_STATUS_CHOICES = (
    ('single', 'Single'),
    ('married', 'Married'),
)

ID_PROOF_CHOICES = (
    ('passport', 'Passport'),
    ('driving_license', 'Driving License'),
    ('aadhaar_card', 'Aadhaar Card'),
    ('pan_card', 'PAN Card'),
    ('voter_id', 'Voter ID'),
)

REQUEST_CHOICES = (
    # ('Pending', 'Pending'),
    ('Approved', 'Approve'), 
    ('Rejected', 'Reject'),
)
    

def generate_unique_id():
    return random.randint(100000000000, 999999999999)

class KYCRegistration(models.Model):
    kyc_id = models.IntegerField(default=generate_unique_id, unique=True, editable=False)

    # Identity Details
    add_profile_image = models.ImageField(upload_to=getProfileImageKYC, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    father_name = models.CharField(max_length=30, null=False, blank=False)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=False, blank=False)
    martial_status = models.CharField(max_length=20, choices=MARTIAL_STATUS_CHOICES, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    nationality = models.CharField(max_length=50, null=False, blank=False)
    id_proof_type = models.CharField(max_length=30, choices=ID_PROOF_CHOICES, null=False, blank=False)
    id_proof_number = models.CharField(max_length=30, null=False, blank=False)
    id_proof_file = models.FileField(upload_to=getIdProofFile)

    # Address Details
    residental_address = models.CharField(max_length=255, null=False, blank=False)
    city_or_town =  models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=30, null=False, blank=False)
    country = models.CharField(max_length=30, null=False, blank=False)
    pin_code = models.CharField(max_length=10)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    
    # For Verification
    created_at = models.DateField(auto_now_add=True)
    kyc_status = models.CharField(max_length=20, choices=REQUEST_CHOICES, default='Pending')


    def __str__(self):
        return f"{self.kyc_id} - {self.first_name} {self.last_name} - {self.kyc_status}"

class ApplyLoan(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

    kyc_id = models.IntegerField()
    user_name_kyc = models.CharField(max_length=30, editable=False, default=" ")

    currentTime = datetime.datetime.now().strftime("%Y%m%H%M")
    generate_loanID = "%s%s"%("YB", currentTime)

    # Loan ID
    loan_id = models.CharField(max_length=40, default=generate_loanID, editable=False)

    # Loan Application
    loan_type = models.ForeignKey(LoanTypes, on_delete=models.SET_NULL, null=True, default=None)
    loan_plan = models.ForeignKey(LoanPlans, on_delete=models.SET_NULL, null=True, default=None)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    applied_on = models.DateField(auto_now_add=True, null=True)
    approval_status = models.CharField(max_length=20, choices=REQUEST_CHOICES, default='Pending')

    # Loan calculations
    interest_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable = False)
    total_payable_amount = models.DecimalField(max_digits=10, decimal_places=2, default = 0, editable = False)
    monthly_payable_amount = models.DecimalField(max_digits=10, decimal_places=2, default = 0, editable = False)
    emi_paid = models.IntegerField(null=False, blank=False)
    emi_pending = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.approval_status} {self.loan_id} - {self.loan_type} applied by {self.user}"

