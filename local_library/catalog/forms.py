import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as lazy
from colorama import Fore, Back

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    
    # Cleans data removing unwanted or unsafe input using default validators
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(lazy('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(lazy('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

"""
from django.forms import ModelForm

from catalog.models import BookInstance

class RenewBookModelForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']
Note: You can also include all fields in the form using fields = '__all__', or you can use exclude (instead of fields) to specify the fields not to include from the model).

Neither approach is recommended because new fields added to the model are then automatically included in the form (without the developer necessarily considering possible security implications).


If these aren't quite right, then we can override 
them in our class Meta, specifying a dictionary 
containing the field to change and its new value. 
For example, in this form, we might want a label 
for our field of "Renewal date" 
(rather than the default based on the 
field name: Due Back), and we also want our help 
text to be specific to this use case.
class Meta:
    model = BookInstance
    fields = ['due_back']
    labels = {'due_back': lazy('New renewal date')}
    help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}


class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
       data = self.cleaned_data['due_back']

       # Check if a date is not in the past.
       if data < datetime.date.today():
           raise ValidationError(_('Invalid date - renewal in past'))

       # Check if a date is in the allowed range (+4 weeks from today).
       if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

       # Remember to always return the cleaned data.
       return data
update the corresponding form variable name from 
renewal_date to due_back as in the second form 
declaration: RenewBookModelForm(initial={'due_back': proposed_renewal_date}.
"""
