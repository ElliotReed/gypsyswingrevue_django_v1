from django import forms


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 6}))


class NewsletterForm(forms.Form):
    subscriber_email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "jane@example.com"})
    )
