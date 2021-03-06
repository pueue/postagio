from django import forms
from .models import Canape
from .fields import MultiEmailField


class NewCanapeForm(forms.ModelForm):
    title = forms.CharField(
        label="Title",
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'title',
            'class': 'form-control',
        }))
    image = forms.ImageField(
        label="Image",
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
        }))
    description = forms.CharField(
        label="Description",
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'description',
            'class': 'form-control',
        }))
    is_transferable = forms.BooleanField(
        label="is_transferable",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-control',
        }))
    is_limit = forms.BooleanField(
        label="is_limit",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-control',
        }))
    quantity = forms.IntegerField(
        label="quantity",
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
        help_text="Only required if 'is_limit' is selected.")

    class Meta:
        model = Canape
        fields = ("title", "image", "description", "is_transferable", "is_limit", "quantity")

    def clean(self):
        if self.cleaned_data.get('is_limit'):
            self.fields_required(['quantity'])
        else:
            self.cleaned_data['quantity'] = ''
        return self.cleaned_data

    def fields_required(self, fields):
        """Used for conditionally marking fields as required."""
        for field in fields:
            if not self.cleaned_data.get(field, ''):
                msg = forms.ValidationError("This field is required.")
                self.add_error(field, msg)


class EditCanapeForm(forms.ModelForm):
    title = forms.CharField(
        label="Title",
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'title',
            'class': 'form-control',
        }))
    image = forms.ImageField(
        label="Image",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
        }))
    description = forms.CharField(
        label="Description",
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'description',
            'class': 'form-control',
        }))
    is_transferable = forms.BooleanField(
        label="is_transferable",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-control',
        }))

    class Meta:
        model = Canape
        fields = ("title", "image", "description", "is_transferable",)


class VerifyCodeForm(forms.Form):
    code = forms.RegexField(
        max_length=16,
        regex=r'^[0-9a-fA-F]+$',
        help_text="Letters and digits only.",
        widget=forms.TextInput(attrs={
            'required': 'true',
            'class': 'form-control',
        })
    )


class DistributeCodeForm(forms.Form):
    emails = MultiEmailField(
        widget=forms.Textarea(attrs={
            'required': 'true',
            'class': 'form-control',
        })
    )
