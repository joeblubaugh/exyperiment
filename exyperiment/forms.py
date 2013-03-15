__author__ = 'joe'

from django.forms import ModelForm, RadioSelect, CheckboxSelectMultiple
from models import Demographics


class DemographicsForm(ModelForm):
    class Meta:
        model = Demographics
        widgets = {
            'gender' : RadioSelect,
            'internet_hours_weekly' : RadioSelect,
            'shopped_online' : RadioSelect,
            'furniture_online' : RadioSelect,
            'shop_online_freq' : RadioSelect,
            'shop_online_spend' : RadioSelect,
            'products_purchased' : CheckboxSelectMultiple,
            'online_store' : CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(DemographicsForm, self).__init__(*args, **kwargs)
        self.fields['products_purchased'].help_text = ''
        self.fields['online_store'].help_text = ''


def remove_holddown(form):
    """This removes the unhelpful "Hold down the...." help texts for the
    specified fields for a form."""
    remove_message = unicode(r'Hold down "Control", or "Command" on a Mac, to select more than one.')
    for field in form.fields:
        field.help_text = field.help_text.replace(remove_message, '').strip()
    return form