from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['Name', 'NUMBERS']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'NUMBERS': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
        }

class SearchForm(forms.Form):
    name = forms.CharField(
        label='Enter the name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by name'})
    )
    number = forms.IntegerField(
        label='Enter the Number',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by number'})
    )

class DeleteForm(forms.Form):
    sno = forms.IntegerField(
        label='Enter the SNO',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter SNO'})
    )

class ModifyForm(forms.Form):
    name = forms.CharField(
        label='Enter the Name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'})
    )
    numbers = forms.IntegerField(
        label='Enter the Number',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number'})
    )
