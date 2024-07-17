
from .models import Email

def email_counts(request):
    if request.user.is_authenticated:
        inbox_count = Email.objects.filter(user=request.user, folder='inbox').count()
        starred_count = Email.objects.filter(user=request.user, folder='starred').count()
        sent_count = Email.objects.filter(user=request.user, folder='sent').count()
        drafts_count = Email.objects.filter(user=request.user, folder='drafts').count()
        outbox_count = Email.objects.filter(user=request.user, folder='outbox').count()
        important_count = Email.objects.filter(user=request.user, folder='important').count()
        bin_count = Email.objects.filter(user=request.user, folder='bin').count()

        return {
            'inbox_count': inbox_count,
            'starred_count': starred_count,
            'sent_count': sent_count,
            'drafts_count': drafts_count,
            'outbox_count': outbox_count,
            'important_count': important_count,
            'bin_count': bin_count,
        }
    else:
        return {}
