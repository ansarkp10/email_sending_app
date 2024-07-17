from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse
from .forms import EmailForm
from .models import Email
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as authlogin, logout as authlogout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, BadHeaderError
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from .models import Email, Attachment

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                authlogin(request, user)
                return redirect('index')
            else:
                error_message = "Invalid email or password."
                return render(request, 'login.html', {'error_message': error_message})
        except User.DoesNotExist:
            error_message = "Invalid email or password."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def logout(request):
    authlogout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            error_message = 'Passwords do not match.'
            return render(request, 'signup.html', {'error_message': error_message})
        if User.objects.filter(email=email).exists():
            error_message = 'Email already exists. Please choose a different one.'
            return render(request, 'signup.html', {'error_message': error_message})
        else:
            username = email.split('@')[0]  # Generate a username from the email
            user = User.objects.create_user(username=username, email=email, password=password1)
            return redirect('login')
    return render(request, 'signup.html')

@login_required(login_url='login')
def create(request):
    email_sent = False
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            from_email = request.user.email
            receiver_email = form.cleaned_data['receiver_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            attachments = request.FILES.getlist('attachments')

            try:
                email = EmailMessage(
                    subject,
                    message,
                    from_email,
                    [receiver_email],
                    reply_to=[from_email]
                )

                for attachment in attachments:
                    email.attach(attachment.name, attachment.read(), attachment.content_type)

                email.send(fail_silently=False)

                email_instance = Email.objects.create(
                    user=request.user,
                    from_email=from_email,
                    receiver_email=receiver_email,
                    subject=subject,
                    message=message,
                    folder='sent'
                )

                for attachment in attachments:
                    Attachment.objects.create(
                        email=email_instance,
                        file=attachment
                    )

                email_sent = True
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            except Exception as e:
                return HttpResponse(f'Error: {e}')

            return redirect('index')
    else:
        form = EmailForm(initial={'from_email': request.user.email})

    return render(request, 'create.html', {'form': form, 'email_sent': email_sent})


@login_required(login_url='login')
def index(request):
    query = request.GET.get('q', '')
    emails = Email.objects.filter(user=request.user).exclude(folder='bin').order_by('-sent_at')
    if query:
        emails = emails.filter(subject__icontains=query)
    
    context = get_email_counts(request.user)
    context['emails'] = emails
    context['query'] = query

    return render(request, 'index.html', context)

@login_required(login_url='login')
def email_detail(request, email_id):
    email = get_object_or_404(Email, id=email_id)
    attachments = email.attachments.all()
    return render(request, 'email_detail.html', {'email': email, 'attachments': attachments})


def toggle_star(request, email_id):
    email = get_object_or_404(Email, id=email_id, user=request.user)
    email.is_starred = not email.is_starred
    email.save()
    return redirect('index')

def starred_toggle_star(request, email_id):
    email = get_object_or_404(Email, id=email_id, user=request.user)
    email.is_starred = not email.is_starred
    email.save()
    return redirect('starred_emails')

def starred_emails(request):
    query = request.GET.get('q', '')

    starred_emails = Email.objects.filter(user=request.user, is_starred=True).order_by('-sent_at')
    if query:
        starred_emails = starred_emails.filter(subject__icontains=query)

    context = get_email_counts(request.user)
    context['emails'] = starred_emails
    context['query'] = query
    return render(request, 'starred.html', context)

def starred_to_bin(request, email_id):
    email = get_object_or_404(Email, id=email_id, user=request.user)
    email.folder = 'bin'  # Move the email to the bin
    email.is_starred = False  # Remove the star from the email
    email.save()
    return redirect('starred_emails')


def get_email_counts(user):
    return {
        'inbox_count': Email.objects.filter(user=user, folder='inbox').count(),
        'starred_count': Email.objects.filter(user=user, folder='starred').count(),
        'sent_count': Email.objects.filter(user=user, folder='sent').count(),
        'drafts_count': Email.objects.filter(user=user, folder='drafts').count(),
        'outbox_count': Email.objects.filter(user=user, folder='outbox').count(),
        'important_count': Email.objects.filter(user=user, folder='important').count(),
        'bin_count': Email.objects.filter(user=user, folder='bin').count(),
    }

def drafts_emails(request):
    query = request.GET.get('q', '')

    drafts = Email.objects.filter(user=request.user, folder='drafts').order_by('-sent_at')
    if query:
        drafts = drafts.filter(subject__icontains=query)

    context = get_email_counts(request.user)
    context['drafts'] = drafts
    context['query'] = query
    return render(request, 'drafts.html', context)

def move_from_drafts(request, email_id):
    email = get_object_or_404(Email, id=email_id, user=request.user, folder='drafts')
    email.folder = 'inbox'  # Move the email to the inbox
    email.save()
    return redirect('drafts_emails')

def outbox_emails(request):
    query = request.GET.get('q', '')

    outbox = Email.objects.filter(user=request.user, folder='outbox').order_by('-sent_at')
    if query:
        outbox = outbox.filter(subject__icontains=query)

    context = get_email_counts(request.user)
    context['outbox'] = outbox
    context['query'] = query
    return render(request, 'outbox.html', context)

def important_emails(request):
    query = request.GET.get('q', '')

    important_emails = Email.objects.filter(user=request.user, folder='important').order_by('-sent_at')
    if query:
        important_emails = important_emails.filter(subject__icontains=query)

    context = get_email_counts(request.user)
    context['important_emails'] = important_emails
    context['query'] = query
    return render(request, 'important.html', context)

def remove_important(request, email_id):
    email = get_object_or_404(Email, id=email_id, user=request.user)
    email.folder = 'inbox'  # Move the email back to the inbox
    email.save()
    return redirect('important_emails')

def important_to_bin(request, email_id):
    email = get_object_or_404(Email, id=email_id, user=request.user)
    email.folder = 'bin'  # Move the email to the bin
    email.save()
    return redirect('important_emails')

def bin_emails(request):
    query = request.GET.get('q', '')
    bin_emails = Email.objects.filter(user=request.user, folder='bin').order_by('-sent_at')
    if query:
        bin_emails = bin_emails.filter(subject__icontains=query)

    context = get_email_counts(request.user)
    context['bin_emails'] = bin_emails
    context['query'] = query
    return render(request, 'bin.html', context)

def delete_all_bin_emails(request):
    if request.method == 'POST':
        Email.objects.filter(user=request.user, folder='bin').delete()
    return redirect('bin_emails')

def delete_email(request, email_id):
    email = get_object_or_404(Email, id=email_id, user=request.user, folder='bin')
    email.delete()
    return redirect('bin_emails')

def recover_email(request, email_id):
    email = Email.objects.get(id=email_id, user=request.user, folder='bin')
    email.folder = 'inbox'
    email.save()
    return redirect('bin_emails')

def move_to_bin(request, email_id):
    email = get_object_or_404(Email, id=email_id, user=request.user)
    email.folder = 'bin'  # Move the email to the bin
    email.save()
    return redirect('index')

def remove_draft(request, email_id):
    email = get_object_or_404(Email, id=email_id, user=request.user)
    email.folder = 'inbox'  # Move the email back to the inbox
    email.save()
    return redirect('drafts_emails')

def drafts_to_bin(request, email_id):
    email = get_object_or_404(Email, id=email_id, user=request.user)
    email.folder = 'bin'  # Move the email to the bin
    email.save()
    return redirect('drafts_emails')

@require_POST
def move_email(request, email_id):
    email = get_object_or_404(Email, id=email_id, user=request.user)
    new_folder = request.POST.get('folder')
    if new_folder in dict(Email.FOLDER_CHOICES).keys():
        email.folder = new_folder
        email.save()
    return redirect('email_detail', email_id=email.id)


