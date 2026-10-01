from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        error_messages={"required": "Name is required."},
    )
    email = forms.EmailField(
        help_text="(We'll never share your email)",
        error_messages={"required": "Email is required."},
    )
    message = forms.CharField(
        error_messages={"required": "A message is required."},
    )
    message.widget = forms.Textarea(attrs={"rows": "10"})
    website = forms.CharField(required=False)
    website.widget = forms.TextInput(
        attrs={"tabindex": "-1", "autocomplete": "off", "data-pooh": "true"}
    )

    def clean_website(self):
        if self.cleaned_data["website"]:
            raise forms.ValidationError("Spam detected")
        return ""


class NewsletterForm(forms.Form):
    subscriber_email = forms.EmailField()
