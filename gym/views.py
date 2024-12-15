import datetime
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum
from .models import User, Membership, Transaction, Equipment, Trainer, Classes, Promotional, TransactionDetail, Maintenance
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from . import models
from datetime import date
from .models import Banners, User
from django.contrib.auth import logout
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.http import HttpResponse, HttpResponseForbidden
from uuid import uuid4

def home(request):
	banners= models.Banners.objects.all()
	return render(request, 'main.html',{'banners':banners})


def membership_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            # Validate user based on email
            user = User.objects.get(email=email)
            login(request, user)  # Log in the user

            # Fetch user's membership data
            try:
                transaction = Transaction.objects.get(user=user)
                return render(request, 'membership/dashboard.html', {'transaction': transaction})
            except Transaction.DoesNotExist:
                messages.error(request, 'No membership data found.')
                return redirect('membership_login')

        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('membership_login')

    return render(request, 'membership/login.html')

def membership_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        membership_data = request.POST.get('membership')

        try:
            # Split the selected membership data
            membership_id, duration = membership_data.split('_')

            # Create a new user
            user = User.objects.create_user(username=username, email=email)
            user.save()

            # Fetch membership details
            membership = Membership.objects.get(membership_id=membership_id)
            duration_months = int(duration)
            membership_start_date = timezone.now()
            membership_end_date = membership_start_date + relativedelta(months=duration_months)

            # Generate a unique transaction ID
            transaction_id = str(uuid4())

            # Create the transaction
            transaction = Transaction.objects.create(
                transaction_id=transaction_id,  # Set the unique ID
                user=user,
                membership=membership,
                membership_start_date=membership_start_date,
                membership_end_date=membership_end_date,
            )
            transaction.save()

            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('membership_login')

        except Membership.DoesNotExist:
            messages.error(request, 'Selected membership plan does not exist.')
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return redirect('membership_signup')

    # Prepare memberships with calculated fees
    memberships = Membership.objects.all()
    membership_data = []
    for membership in memberships:
        membership_data.append({
            'membership_id': membership.membership_id,
            'membership_name': membership.membership_name,
            'monthly_fee': membership.monthly_fee,
            'three_month_fee': membership.monthly_fee * 3,
            'six_month_fee': membership.monthly_fee * 6,
            'twelve_month_fee': membership.monthly_fee * 12,
        })
        
    # Fetch all memberships to display in the signup form
    memberships = Membership.objects.all()
    return render(request, 'membership/signup.html', {'memberships': membership_data})

@login_required
def membership_dashboard(request):
    try:
        # Fetch the transaction linked to the logged-in user
        transaction = Transaction.objects.get(user=request.user)
    except Transaction.DoesNotExist:
        transaction = None  # Handle the case where no transaction exists

    # Pass transaction data to the template
    return render(request, 'membership/dashboard.html', {'transaction': transaction})

@login_required
def membership_dashboard_membership(request):
    # Fetch the current user's membership details
    transactions = Transaction.objects.filter(user=request.user).select_related('membership')

    # Fetch all promotions
    promotions = Promotional.objects.filter(
        promotional_start_date__lte=timezone.now(),
        promotional_end_date__gte=timezone.now()
    )

    context = {
        'transactions': transactions,  
        'promotions': promotions,      
    }
    return render(request, 'membership/dashboard_membership.html', context)

@login_required
def membership_dashboard_classes(request):
    # Fetch all classes
    upcoming_classes = Classes.objects.filter(class_schedule__gte=timezone.now())

    # Fetch classes the user is enrolled in
    enrolled_classes = TransactionDetail.objects.filter(
        transaction__user=request.user, 
        class_info__isnull=False
    ).select_related('class_info')

    context = {
        'upcoming_classes': upcoming_classes,  # Available classes
        'enrolled_classes': enrolled_classes,  # User's enrolled classes
    }
    return render(request, 'membership/dashboard_classes.html', context)

def membership_logout(request):
    logout(request)
    return render(request, 'membership/logout.html')


def trainer_login(request):
    if request.method == 'POST':
        trainer_name = request.POST.get('trainer_name')
        trainer_id = request.POST.get('trainer_id')

        # Validate input
        if not trainer_name or not trainer_id:
            messages.error(request, 'Both Trainer Name and Trainer ID are required.')
            return redirect('trainer_login')

        try:
            # Fetch trainer based on trainer_name and trainer_id
            trainer = Trainer.objects.get(trainer_name=trainer_name, trainer_id=trainer_id)

            # Store trainer information in the session
            request.session['trainer_id'] = trainer.trainer_id
            request.session['trainer_name'] = trainer.trainer_name

            # Success message and redirection
            messages.success(request, f"Welcome {trainer.trainer_name}!")
            return redirect('trainer_dashboard')

        except Trainer.DoesNotExist:
            # Handle invalid credentials
            messages.error(request, 'Invalid Trainer Name or Trainer ID. Please try again.')
            return redirect('trainer_login')

    return render(request, 'trainer/login.html')

def trainer_signup(request):
    if request.method == 'POST':
        trainer_name = request.POST.get('trainer_name')
        trainer_specialty = request.POST.get('trainer_specialty')
        years_of_experience = request.POST.get('years_of_experience')
        trainer_fee = request.POST.get('trainer_fee')
        phone_number = request.POST.get('phone_number')

        # Validate inputs
        if not all([trainer_name, trainer_specialty, years_of_experience, trainer_fee, phone_number]):
            messages.error(request, 'All fields are required. Please fill out every field.')
            return redirect('trainer_signup')

        try:
            years_of_experience = int(years_of_experience)
            trainer_fee = int(trainer_fee)
            if years_of_experience < 0 or trainer_fee < 0:
                raise ValueError
        except ValueError:
            messages.error(request, 'Years of experience and fee must be valid positive numbers.')
            return redirect('trainer_signup')

        # Create a new trainer
        trainer_id = f"TR-{trainer_name[:3].upper()}-{random.randint(1000, 9999)}"
        Trainer.objects.create(
            trainer_id=trainer_id,
            trainer_name=trainer_name,
            trainer_specialty=trainer_specialty,
            years_of_experience=years_of_experience,
            trainer_fee=trainer_fee,
            phone_number=phone_number,
        )

        messages.success(request, 'Trainer account created successfully. Please log in.')
        return redirect('trainer_login')

    return render(request, 'trainer/signup.html')

@login_required
def trainer_dashboard(request):
    # Ensure the trainer is logged in
    trainer_id = request.session.get('trainer_id')
    if not trainer_id:
        return redirect('trainer_login')

    # Fetch the trainer instance
    try:
        trainer = Trainer.objects.get(trainer_id=trainer_id)
    except Trainer.DoesNotExist:
        return render(request, 'trainer/dashboard.html', {
            'error_message': 'Trainer not found. Please ensure your account is properly linked.'
        })

    # Fetch classes associated with this trainer
    classes = Classes.objects.filter(trainer=trainer)
    upcoming_classes = classes.filter(class_schedule__gte=date.today())
    total_classes = classes.count()

    context = {
        'trainer': trainer,
        'upcoming_classes': upcoming_classes,
        'total_classes': total_classes,
    }
    return render(request, 'trainer/dashboard.html', context)


@login_required
def gym_classes_list(request):
    classes = Classes.objects.all()  
    return render(request, 'classes/list.html', {'classes': classes})

# View for adding a new class
@login_required
def add_gym_class(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        class_schedule = request.POST.get('class_schedule')
        trainer_id = request.POST.get('trainer_id')

        try:
            trainer = Trainer.objects.get(trainer_id=trainer_id)
            new_class = Classes.objects.create(
                class_name=class_name,
                class_schedule=class_schedule,
                trainer=trainer
            )
            new_class.save()
            messages.success(request, 'Gym class added successfully.')
            return redirect('gym_classes_list')
        except Trainer.DoesNotExist:
            messages.error(request, 'Trainer not found.')

    trainers = Trainer.objects.all()
    return render(request, 'classes/add_class.html', {'trainers': trainers})

# View for updating an existing class
@login_required
@login_required
def update_gym_class(request, class_id):
    gym_class = get_object_or_404(Classes, class_id=class_id)
    if request.method == 'POST':
        gym_class.class_name = request.POST.get('class_name')
        gym_class.class_schedule = request.POST.get('class_schedule')
        trainer_id = request.POST.get('trainer_id')

        try:
            trainer = Trainer.objects.get(trainer_id=trainer_id)
            gym_class.trainer = trainer
            gym_class.save()
            messages.success(request, 'Class updated successfully.')
            return redirect('gym_classes_list')
        except Trainer.DoesNotExist:
            messages.error(request, 'Trainer not found.')

    trainers = Trainer.objects.all()
    return render(request, 'classes/update_class.html', {
        'gym_class': gym_class,
        'trainers': trainers,
    })

# View for deleting a class
@login_required
def delete_gym_class(request, class_id):
    gym_class = get_object_or_404(Classes, class_id=class_id)
    gym_class.delete()
    messages.success(request, 'Gym class deleted successfully.')
    return redirect('gym_classes_list')

def trainer_logout(request):
    logout(request)
    return render(request, 'trainer/logout.html')

# Equipment views
def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'Equipment/list.html', {'equipments': equipments})

def add_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('equipment_id')
        equipment_name = request.POST.get('equipment_name')
        equipment_type = request.POST.get('type')
        cost = request.POST.get('cost')
        purchase_date = request.POST.get('purchase_date')
        condition = request.POST.get('condition')
        maintenance_id = request.POST.get('maintenance_id')

        try:
            maintenance = Maintenance.objects.get(pk=maintenance_id) if maintenance_id else None
            Equipment.objects.create(
                equipment_id=equipment_id,
                equipment_name=equipment_name,
                type=equipment_type,
                cost=int(cost),
                purchase_date=purchase_date,
                condition=condition,
                maintenance=maintenance,
            )
            messages.success(request, 'Equipment added successfully.')
            return redirect('equipment_list')
        except Maintenance.DoesNotExist:
            messages.error(request, 'Invalid maintenance record selected.')
    
    maintenances = Maintenance.objects.all()
    return render(request, 'equipment/add_equipment.html', {'maintenances': maintenances})

def update_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    if request.method == 'POST':
        equipment.equipment_name = request.POST.get('equipment_name')
        equipment.type = request.POST.get('type')
        equipment.cost = request.POST.get('cost')
        equipment.purchase_date = request.POST.get('purchase_date')
        equipment.condition = request.POST.get('condition')
        maintenance_id = request.POST.get('maintenance_id')

        try:
            equipment.maintenance = Maintenance.objects.get(pk=maintenance_id) if maintenance_id else None
            equipment.save()
            messages.success(request, 'Equipment updated successfully.')
            return redirect('equipment_list')
        except Maintenance.DoesNotExist:
            messages.error(request, 'Invalid maintenance record selected.')

    maintenances = Maintenance.objects.all()
    return render(request, 'equipment/update_equipment.html', {'equipment': equipment, 'maintenances': maintenances})

def delete_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    equipment.delete()
    messages.success(request, 'Equipment deleted successfully.')
    return redirect('equipment_list')

# Maintenance views
def maintenance_list(request):
    maintenances = Maintenance.objects.all()
    return render(request, 'maintenance/list.html', {'maintenances': maintenances})

def add_maintenance(request):
    if request.method == 'POST':
        maintenance_id = request.POST.get('maintenance_id')
        maintenance_date = request.POST.get('maintenance_date')
        maintenance_type = request.POST.get('maintenance_type')
        technician_name = request.POST.get('technician_name')

        Maintenance.objects.create(
            maintenance_id=maintenance_id,
            maintenance_date=maintenance_date,
            maintenance_type=maintenance_type,
            technician_name=technician_name,
        )
        messages.success(request, 'Maintenance record added successfully.')
        return redirect('maintenance_list')

    return render(request, 'maintenance/add_maintenance.html')

def update_maintenance(request, maintenance_id):
    maintenance = get_object_or_404(Maintenance, pk=maintenance_id)
    if request.method == 'POST':
        maintenance.maintenance_date = request.POST.get('maintenance_date')
        maintenance.maintenance_type = request.POST.get('maintenance_type')
        maintenance.technician_name = request.POST.get('technician_name')
        maintenance.save()
        messages.success(request, 'Maintenance record updated successfully.')
        return redirect('maintenance_list')

    return render(request, 'maintenance/update_maintenance.html', {'maintenance': maintenance})

def delete_maintenance(request, maintenance_id):
    maintenance = get_object_or_404(Maintenance, pk=maintenance_id)
    maintenance.delete()
    messages.success(request, 'Maintenance record deleted successfully.')
    return redirect('maintenance_list')


# List all promotions
def promotional_list(request):
    promotions = Promotional.objects.all()
    return render(request, 'promotional/list.html', {'promotions': promotions})

# Add a new promotion
def add_promotional(request):
    if request.method == 'POST':
        promotional_id = request.POST.get('promotional_id')
        promotional_name = request.POST.get('promotional_name')
        description = request.POST.get('description')
        promotional_start_date = request.POST.get('promotional_start_date')
        promotional_end_date = request.POST.get('promotional_end_date')
        discount_percentage = request.POST.get('discount_percentage')

        # Save the promotional record
        Promotional.objects.create(
            promotional_id=promotional_id,
            promotional_name=promotional_name,
            description=description,
            promotional_start_date=promotional_start_date,
            promotional_end_date=promotional_end_date,
            discount_percentage=int(discount_percentage),
        )
        messages.success(request, 'Promotional record added successfully.')
        return redirect('promotional_list')

    return render(request, 'promotional/add_promotional.html')

# Update a promotion
def update_promotional(request, promotional_id):
    promotional = get_object_or_404(Promotional, promotional_id=promotional_id)
    if request.method == 'POST':
        promotional.promotional_name = request.POST.get('promotional_name')
        promotional.description = request.POST.get('description')
        promotional.promotional_start_date = request.POST.get('promotional_start_date')
        promotional.promotional_end_date = request.POST.get('promotional_end_date')
        promotional.discount_percentage = request.POST.get('discount_percentage')
        promotional.save()

        messages.success(request, 'Promotional record updated successfully.')
        return redirect('promotional_list')

    return render(request, 'promotional/update_promotional.html', {'promotional': promotional})

# Delete a promotion
def delete_promotional(request, promotional_id):
    promotional = get_object_or_404(Promotional, promotional_id=promotional_id)
    promotional.delete()
    messages.success(request, 'Promotional record deleted successfully.')
    return redirect('promotional_list')