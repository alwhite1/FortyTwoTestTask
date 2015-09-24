from django import forms
from person.models import Person

class EditPersonModelForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    name = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'id': 'edit_name'}),
                           label=u'Name: ')
    last_name = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'id': 'edit_last_name'}),
                                label=u'Last Name: ')
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'id': "edit_day_of_birth"}),
                                    label=u'Date of birth:')
    bio = forms.CharField(widget=forms.Textarea(attrs={'id': 'edit_bio'}),
                          label=u'Bio: ')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'edit_email'}),
                             label=u'Email: ')
    jabber = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'edit_jabber'}),
                              label=u'Jabber: ')
    skype = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'id': 'edit_skype'}),
                            label=u'Skype: ')
    other_contacts = forms.CharField(widget=forms.Textarea(attrs={'id': 'edit_other_contacts'}),
                                     label=u'Other contacts:')
    photo = forms.ImageField(widget=forms.FileInput(attrs={'id': 'edit_photo'}), label=u'Photo: ')
