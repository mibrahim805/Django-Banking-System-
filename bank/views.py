from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from bank.forms import RegistrationForm, BankCreationForm, BranchCreationForm
from bank.models import Bank, Branch


def user_register_view(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'registration/register.html', {'form': form})




@login_required
def profile_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({}, status=401)

    user = request.user
    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    })

@login_required
def profile_page(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    return render(request, "profile/profile.html", {"user": request.user})



def profile_edit(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    user = request.user
    errors = {}

    if request.method == "GET":
        return render(request, "profile/profile_edit.html", {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        })

    elif request.method == "POST":
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email", "")
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if email:
            try:
                validate_email(email)
            except ValidationError:
                errors["email"] = "Enter a valid email address"

        if password1:
            if password1 != password2:
                errors["password2"] = "The two password fields didn't match"
            elif len(password1) < 8:
                errors["password1"] = "This password is too short. It must contain at least 8 characters"

        if errors:
            return render(request, "profile/profile_edit.html", {
                "errors": errors,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
            })

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        if password1:
            user.set_password(password1)

        user.save()

        if password1:
            from django.contrib.auth import login
            login(request, user)

        return redirect('/profile/view/')


@login_required
def add_bank(request):
    if request.method == 'POST':
        form = BankCreationForm(request.POST)
        if form.is_valid():
            owner = request.user
            bank = form.save(commit=False)
            bank.owner = owner
            form.save()
            return redirect('profile_view')
    else:
        form = BankCreationForm()
        return render(request, 'bank/add_bank.html', {'form': form})


@login_required
def bank_list_view(request):
    if request.method == 'GET':
        banks = Bank.objects.filter(owner=request.user)
        return render(request, 'bank/bank_list.html', {'banks': banks})


@login_required
def bank_detail_view(request, bank_id):
    if request.method == 'GET':
        try:
            bank = Bank.objects.get(id=bank_id, owner=request.user)
            branches = Branch.objects.filter(bank=bank)
            return render(request, 'bank/bank_detail.html', {'bank': bank, 'branches': branches})
        except Bank.DoesNotExist:
            return HttpResponse(status=404)


@login_required
def delete_bank(request, bank_id):
    if request.method == 'POST':
        try:
            bank = Bank.objects.get(id=bank_id, owner=request.user)
            bank.delete()
            return redirect('bank_list')
        except Bank.DoesNotExist:
            return HttpResponse(status=404)



@login_required
def create_branch_view(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id)
    if bank.owner != request.user:
        return HttpResponse(status=403)
    if request.method == 'POST':
        form = BranchCreationForm(request.POST)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.bank = bank
            branch.save()
            return redirect(f"/banks/branch/{branch.id}/details/")
    else:
        form = BranchCreationForm()
    return render(request, 'branch/add_branch.html', {'form': form, 'bank': bank})


@login_required
def branch_detail_view(request, branch_id):
    if request.method == 'GET':
        branch = get_object_or_404(Branch, id=branch_id)
        if branch.bank.owner != request.user:
            return HttpResponse(status=403)
        return render(request, 'branch/branch_detail.html', {'branch': branch})


@login_required
def delete_branch(request, branch_id):
    if request.method == 'POST':
        branch = get_object_or_404(Branch, id=branch_id)
        if branch.bank.owner != request.user:
            return HttpResponse(status=403)
        bank_id = branch.bank.id
        branch.delete()
        return redirect(f"/banks/{bank_id}/details/")


@login_required
def update_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    if branch.bank.owner != request.user:
        return HttpResponse(status=403)
    if request.method == 'POST':
        form = BranchCreationForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect(f"/banks/{branch.bank.id}/details/")
    else:
        form = BranchCreationForm(instance=branch)
    return render(request, 'branch/update_branch.html', {'form': form, 'branch': branch})
