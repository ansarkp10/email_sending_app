from django import forms

class EmailForm(forms.Form):
    from_email = forms.EmailField(label='From', widget=forms.EmailInput(attrs={'readonly': 'readonly'}))
    receiver_email = forms.EmailField(label='To')
    subject = forms.CharField(max_length=255, label='Subject')
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'message-textarea'}), label='Message')
    attachments = forms.FileField(required=False, label='Attachments')
