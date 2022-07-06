from django.forms import ModelForm

from .models import PricingCategory


class PricingForm(ModelForm):
    class Meta:
        model = PricingCategory
        fields = ['title',
                  'description',
                  'price',
                  'made_by',
                  'made_at'
                  ]

    def __int__(self, *args, **kwargs):
        super(PricingForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'input'
        self.fields['description'].widget.attrs['class'] = 'description'

