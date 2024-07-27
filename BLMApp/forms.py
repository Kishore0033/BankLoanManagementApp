from django import forms
from BLMApp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class applyLoanForm(forms.ModelForm):
    class Meta:
        model = ApplyLoan
        fields = [
            'kyc_id',
            'loan_type',
            'loan_plan',
            'loan_amount',
            'approval_status',
        ]
        widgets = {
            'approval_status': forms.RadioSelect()
        }

    
# class kycRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = KYCRegistration
#         fields = '__all__'
        
class addLoanPlanForm(forms.ModelForm):
    class Meta:
        model = LoanPlans
        fields = '__all__'

class signUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = {
            'username',
            'email',
        }

        def save(self, commit = True):
            user = super(signUpForm, self).save(commit = False)
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user