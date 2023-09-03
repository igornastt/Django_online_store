from django import forms

from catalog.models import Product, Version

# Список запрещенных слов, проверяемых при заполнении формы
FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта',
                   'биржа', 'дешево', 'бесплатно', 'обман',
                   'полиция', 'радар'
                   ]


class StyleFormMixin:
    """Класс-миксин для стилизации форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_current_version":
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    """Класс для генерации формы создания продукта"""

    class Meta:
        model = Product
        fields = "__all__"

    def clean(self):
        """Метод для валидации полей названия и описания продукта"""

        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        if name and any(word in name.lower() for word in FORBIDDEN_WORDS):
            self.add_error('name', 'Недопустимое слово в названии продукта!')

        if description and any(word in description.lower() for word in FORBIDDEN_WORDS):
            self.add_error('description', 'Недопустимое слово в описании продукта!')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    """Класс для генерации формы версии продукта"""

    class Meta:
        model = Version
        fields = "__all__"
