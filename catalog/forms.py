from django import forms

from catalog.models import Product, Version

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта',
                   'биржа', 'дешево', 'бесплатно', 'обман',
                   'полиция', 'радар'
                   ]


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_current_version":
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('owner', 'status',)

    def clean(self):

        cleaned_data = super().clean()
        name = cleaned_data.get('title')
        description = cleaned_data.get('text')

        if name and any(word in name.lower() for word in FORBIDDEN_WORDS):
            self.add_error('title', 'Недопустимое слово в названии продукта!')

        if description and any(word in description.lower() for word in FORBIDDEN_WORDS):
            self.add_error('text', 'Недопустимое слово в описании продукта!')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = "__all__"


class ProductModerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('text', 'category', 'status',)
