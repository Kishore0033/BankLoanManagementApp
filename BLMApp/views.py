from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from BLMApp.models import *
from BLMApp.forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.

def homePage(request):
    loan_type_data = LoanTypes.objects.all()
    return render(request, 'BLMApp/home.html', {'loan_type_data': loan_type_data})

def loanForm(request):
    loan_plans = LoanPlans.objects.all()
    # loan_plan_choices = {loan_plan.id: f"{loan_plan.loan_type} with {loan_plan.loan_interest_rate}% interest for {loan_plan.loan_plan_duration_months} ({loan_plan.loan_plan_duration_years} years)" for loan_plan in loan_plans}
    if request.method == 'POST':   
        loan_plan_data = LoanPlans.objects.filter(loan_type = request.POST['loan_type']).first()
        loanApplicationForm = applyLoanForm(request.POST)    
        if loanApplicationForm.is_valid():
            apply_loan = loanApplicationForm.save(commit=False)

            # apply_loan.loan_plan = request.POST['loan_plan']
            apply_loan.user = request.user
            interestAmount = float(request.POST['loan_amount']) * float(loan_plan_data.loan_plan_duration_years) * float(loan_plan_data.loan_interest_rate / 100)
            totalPayableAmount = interestAmount + float(request.POST['loan_amount'])
            monthlyPayableAmount = totalPayableAmount / 12

            apply_loan.interest_amount = interestAmount
            apply_loan.total_payable_amount = totalPayableAmount
            apply_loan.monthly_payable_amount = monthlyPayableAmount
            apply_loan.emi_paid = 0
            apply_loan.emi_pending = int(loan_plan_data.loan_plan_duration_months)

            apply_loan.save()
            # return redirect('/loanConfirmation')
    else:
        loanApplicationForm = applyLoanForm()
    return render(request, 'BLMApp/loanApplicationForm.html', {
        'form':loanApplicationForm, 
        # 'plan_choices': loan_plan_choices
        })

def availLoans(request):
    availableLoans = LoanTypes.objects.all()
    availableLoanPlans = LoanPlans.objects.all()
    return render(request, 'BLMApp/availableLoans.html', {'availableLoans': availableLoans, 'availableLoanPlans': availableLoanPlans})


def kycDatas(request):
    if request.method == "POST":
        profileImage = request.FILES['profileImage']
        firstName = request.POST['fname']
        lastName = request.POST['lname']
        fatherName = request.POST['fatherName']
        gender = request.POST['gender']
        martialStatus = request.POST['martialStatus']
        dateOfBirth = request.POST['dob']
        nationality = request.POST['nationality']
        idProofType = request.POST['idProofType']
        idProofNo = request.POST['idProofNo']
        idProofFile = request.FILES['idProofFile']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        pincode = request.POST['pincode']
        email = request.POST['email']
        phone = request.POST['phoneno']

        obj = KYCRegistration()
        obj.add_profile_image = profileImage
        obj.first_name = firstName
        obj.last_name = lastName
        obj.father_name = fatherName
        obj.gender = gender
        obj.martial_status = martialStatus
        obj.date_of_birth = dateOfBirth
        obj.nationality = nationality
        obj.id_proof_type = idProofType
        obj.id_proof_number = idProofNo
        obj.id_proof_file = idProofFile
        obj.residental_address = address
        obj.city_or_town = city
        obj.state = state
        obj.country = country
        obj.pin_code = pincode   
        obj.email = email
        obj.phone_number = phone
        obj.save()
    return render(request, 'BLMApp/kycRegistrationForm.html')


# def kycRegistration(request):
#     if request.method == 'POST':
#         kycRegistrationFormContext = kycRegistrationForm(request.POST, request.FILES)
#         if kycRegistrationFormContext.is_valid():
#             kycRegistrationFormContext.save()
#             return redirect('/form')
#     else:
#         kycRegistrationFormContext = kycRegistrationForm()
#     return render(request, 'BLMApp/kycRegistrationForm.html', {'form': kycRegistrationFormContext})


@login_required
def yourLoans(request):
    your_loans = ApplyLoan.objects.filter(user=request.user)
    return render(request, 'BLMApp/yourLoans.html', {'loans': your_loans})

# def login(request):
#     return render(request, 'BLMApp/login.html')

def signup(request):
    if request.method == "POST":
        form = signUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = signUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile(request):
    return render(request, 'BLMApp/profile.html')

# def loanConfirmation(request):
#     kycID = request.POST.get('kyc_id')
#     loanTypeID = request.POST.get('loan_type')
#     loanPlanID = request.POST.get('loan_plan')
#     loanAmount = int(request.POST.get('loan_amount'))

#     fetch_loan_type = LoanTypes.objects.filter(pk = loanTypeID).first()
#     fetch_loan_plan = LoanPlans.objects.filter(pk = loanPlanID).first()
    
#     loanType = fetch_loan_type.loan_type
#     # loanType = LoanTypes.objects.get(loan_type = loanTypeRef)
#     interestRate = int(fetch_loan_plan.loan_interest_rate)
#     planDurationMons = int(fetch_loan_plan.loan_plan_duration_months)
#     planDurationYrs = int(fetch_loan_plan.loan_plan_duration_years)
#     loanPlan = f"{loanType} with {interestRate}% interest for {planDurationYrs} Years"

#     interestAmount = loanAmount * planDurationYrs * interestRate / 100
#     totalPayableAmount = loanAmount + interestAmount
#     monthlyPayableAmount = round(totalPayableAmount / 12, 2)

#     # Create a new ApplyLoan object and set its attributes
#     loanAppForm = ApplyLoan(
#         kyc_id=kycID,
#         loan_type=loan_type,
#         loan_plan=loan_plan,
#         loan_amount=loanAmount,
#         interest_amount=interestAmount,
#         total_payable_amount=totalPayableAmount,
#         monthly_payable_amount=monthlyPayableAmount,
#         emi_paid=0,
#         emi_pending=planDurationMons,
#     )

#     loanAppForm.save()

#     return render(request, 'BLMApp/loanConfirmationPage.html', {
#         'loanType': loanType,
#         'loanPlan': loanPlan,
#         'loanAmount': loanAmount,
#         'loanInterestAmount': interestAmount,
#         'loanTotalPayableAmount': totalPayableAmount,
#         'loanMonthlyPayableAmount': monthlyPayableAmount,
#     })



def loanConfirmation(request):
    kycID = int(request.POST.get('kyc_id'))
    loanTypeID = request.POST.get('loan_type')
    loanPlanID = request.POST.get('loan_plan')
    loanAmount = int(request.POST.get('loan_amount'))

    # Fetch the related LoanTypes and LoanPlans objects
    loan_type = LoanTypes.objects.get(pk=loanTypeID)
    loan_plan = LoanPlans.objects.get(pk=loanPlanID)
    fetch_kyc_registration = KYCRegistration.objects.all()
    user_name_kyc = " "
    for users in fetch_kyc_registration:
        # user_name_kyc = type(kycID)
        if users.kyc_id == kycID:
            user_name_kyc = f"{users.first_name} {users.last_name}"

            interestRate = int(loan_plan.loan_interest_rate)
            planDurationMons = int(loan_plan.loan_plan_duration_months)
            planDurationYrs = int(loan_plan.loan_plan_duration_years)

            loanPlan = f"{loan_type.loan_type} with {interestRate}% interest for {planDurationYrs} Years"

            interestAmount = loanAmount * planDurationYrs * interestRate / 100
            totalPayableAmount = loanAmount + interestAmount
            monthlyPayableAmount = round(totalPayableAmount / 12, 2)

            # Create a new ApplyLoan object and set its attributes
            loanAppForm = ApplyLoan(
                user=request.user,
                kyc_id=kycID,
                user_name_kyc=user_name_kyc,
                loan_type=loan_type,
                loan_plan=loan_plan,
                loan_amount=loanAmount,
                interest_amount=interestAmount,
                total_payable_amount=totalPayableAmount,
                monthly_payable_amount=monthlyPayableAmount,
                emi_paid=0,
                emi_pending=planDurationMons,
            )

            # Save the ApplyLoan object to the database
            loanAppForm.save()

            return render(request, 'BLMApp/loanConfirmationPage.html', {
                'kycID': kycID,
                'userName': user_name_kyc,
                'loanType': loan_type,
                'loanPlan': loanPlan,
                'loanAmount': loanAmount,
                'loanInterestAmount': interestAmount,
                'loanTotalPayableAmount': totalPayableAmount,
                'loanMonthlyPayableAmount': monthlyPayableAmount,
            })
            break
        else:
            return render(request, 'BLMApp/userNotFound.html')



def payEmi(request):
    return render(request, 'BLMApp/payemi.html')

def paymentPage(request):
    loan_id = request.POST.get('loan_id')
    fetch_loans = ApplyLoan.objects.filter(loan_id=loan_id).first()
    if loan_id == fetch_loans.loan_id:
        if fetch_loans.approval_status == "Approved":
            user_name = fetch_loans.user
            loan_type = fetch_loans.loan_amount
            emi_amount = fetch_loans.monthly_payable_amount
            loan_plan = fetch_loans.loan_plan
            loan_amount = fetch_loans.loan_amount
            interest_amount = fetch_loans.interest_amount
            total_payable_amount = fetch_loans.total_payable_amount
            status = fetch_loans.approval_status

            if request.method == 'POST':
                # Reduce emi_pending and increase emi_paid fields
                fetch_loans.emi_pending -= 1
                fetch_loans.emi_paid += 1
                fetch_loans.save()

            return render(request, 'BLMApp/paymentPage.html', {
                'loanID': loan_id,
                'userName': user_name,
                'emiAmount': emi_amount,
                'loanType': loan_type,
                'loanPlan': loan_plan,
                'loanAmount': loan_amount,
                'interestAmount': interest_amount,
                'totalPayableAmount': total_payable_amount,
                'status': status,
            })
        elif fetch_loans.approval_status == "Pending":
            return render(request, 'BLMApp/loanPending.html')
        elif fetch_loans.approval_status == "Rejected":
            return render(request, 'BLMApp/loanRejected.html')
    else:
        return render(request, 'BLMApp/loanNotFound.html')

def loanSuccess(request):
    return render(request, 'BLMApp/loanSuccessPage.html')

def paymentSuccess(request):
    return render(request, 'BLMApp/paymentSuccess.html')

def paymentSuccess(request):
    return render(request, 'BLMApp/paymentSuccess.html')

def loanSuccess(request):
    return render(request, 'BLMApp/paymentSuccess.html')

def paymentPage(request):
    return render(request, 'BLMProject/loanSuccess.html', {
        'emi_pending': emiAmount,
        'loan_id': loanID,
        'loan_type': loanType,
        'loan_amount': loanAmount,
        'interest_amount': interestAmount,
        'total_payable_amount': totalPayableAmount,
        'approval_status': approvalStatus,
    })