from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import logging
from .models import Application
from .forms import UserRegistrationForm, CitizenshipApplicationForm, PANApplicationForm, ContactForm

# Set up logger
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def citizenship(request):
    if request.method == 'POST':
        form = CitizenshipApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                application.user = request.user
                application.type = 'citizenship'
                application.country = 'Nepal'  # Default value
                application.status = 'pending'  # Default status
                application.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Citizenship application submitted successfully!'
                    })
                
                messages.success(request, 'Citizenship application submitted successfully!')
                return redirect('dashboard')
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': str(e)
                    }, status=400)
                messages.error(request, f'Error submitting application: {str(e)}')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid form data',
                    'errors': form.errors
                }, status=400)
    else:
        form = CitizenshipApplicationForm()
    return render(request, 'core/citizenship.html', {'form': form})

@login_required
def pan(request):
    if request.method == 'POST':
        form = PANApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                application.user = request.user
                application.type = 'pan'
                application.country = 'Nepal'  # Default value
                application.status = 'pending'  # Default status
                application.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'PAN application submitted successfully!'
                    })
                
                messages.success(request, 'PAN application submitted successfully!')
                return redirect('dashboard')
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': str(e)
                    }, status=400)
                messages.error(request, f'Error submitting application: {str(e)}')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid form data',
                    'errors': form.errors
                }, status=400)
    else:
        form = PANApplicationForm()
    return render(request, 'core/pan.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                application.user = request.user if request.user.is_authenticated else None
                application.type = 'contact'
                application.status = 'pending'  # Default status
                application.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Message sent successfully!'
                    })
                
                messages.success(request, 'Message sent successfully!')
                return redirect('home')
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': str(e)
                    }, status=400)
                messages.error(request, f'Error sending message: {str(e)}')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid form data',
                    'errors': form.errors
                }, status=400)
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})

@login_required
def dashboard(request):
    # Get application counts
    total_applications = Application.objects.filter(user=request.user).count()
    pending_applications = Application.objects.filter(user=request.user, status='pending').count()
    approved_applications = Application.objects.filter(user=request.user, status='approved').count()
    rejected_applications = Application.objects.filter(user=request.user, status='rejected').count()
    
    # Get recent applications
    applications = Application.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    # Get applications by type for chart
    applications_by_type = Application.objects.filter(user=request.user).values('type').annotate(count=Count('id'))
    
    context = {
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
        'applications': applications,
        'applications_by_type': list(applications_by_type)
    }
    
    return render(request, 'core/dashboard.html', context)

@login_required
@require_http_methods(["POST"])
def update_application_status(request, application_id):
    logger.info(f"Attempting to update application {application_id} status")
    try:
        # Parse the JSON data
        try:
            data = json.loads(request.body)
            status = data.get('status')
            
            logger.info(f"Received data: {data}")  # Debug log
            
            if not status:
                logger.warning(f"Status not provided in request for application {application_id}")
                return JsonResponse({
                    'success': False,
                    'message': 'Status is required'
                }, status=400)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON data for application {application_id}: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            }, status=400)
        
        # Validate status
        if status not in ['approved', 'rejected']:
            logger.warning(f"Invalid status '{status}' for application {application_id}")
            return JsonResponse({
                'success': False,
                'message': f'Invalid status: {status}. Must be either "approved" or "rejected"'
            }, status=400)
        
        # Get and update the application
        try:
            application = get_object_or_404(Application, pk=application_id)
            
            # Log the current state
            logger.info(f"Found application {application_id}: type={application.type}, current_status={application.status}")
            
            # Ensure the user has permission to update this application
            if application.user != request.user:
                logger.warning(f"User {request.user.pk} attempted to update application {application_id} belonging to user {application.user.pk}")
                return JsonResponse({
                    'success': False,
                    'message': 'You do not have permission to update this application'
                }, status=403)
            
            # Check if the application is already approved/rejected
            if application.status != 'pending':
                logger.warning(f"Attempted to update non-pending application {application_id} (current status: {application.status})")
                return JsonResponse({
                    'success': False,
                    'message': f'Application is already {application.status}'
                }, status=400)
            
            # Update the status
            application.status = status
            application.save()
            
            logger.info(f"Successfully updated application {application_id} status to {status}")
            return JsonResponse({
                'success': True,
                'message': f'Application successfully {status}'
            })
            
        except Application.DoesNotExist:
            logger.error(f"Application {application_id} not found")
            return JsonResponse({
                'success': False,
                'message': 'Application not found'
            }, status=404)
            
    except Exception as e:
        logger.error(f"Unexpected error updating application {application_id}: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'An unexpected error occurred'
        }, status=500)
