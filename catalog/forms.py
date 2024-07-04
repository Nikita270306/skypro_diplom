from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from crispy_forms.helper import FormHelper
from django.urls import reverse_lazy

from catalog.models import Product, Category, Version


class FormStyleMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.Select):  # Пример для поля типа Select
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductCreateForm(FormStyleMixin, ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price_per_unit')

    def clean_name(self):
        name = self.cleaned_data['name']
        banned_words = ['casino', 'cryptocurrency', 'crypto', 'exchange', 'cheap',
                        'free', 'scam', 'police', 'radar']

        for word in banned_words:
            if word.lower() in name.lower():
                raise ValidationError(f"Слово '{word}' запрещено использовать в названии продукта. ")

        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        banned_words = ['casino', 'cryptocurrency', 'crypto', 'exchange', 'cheap',
                        'free', 'scam', 'police', 'radar']

        for word in banned_words:
            if word.lower() in description.lower():
                raise ValidationError(f"Слово '{word}' запрещено использовать в описании продукта.")

        return description

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        return super().form_valid(form)

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

        self.helper.attrs = {'class': 'form-control'}
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter name'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Enter description'})
        self.fields['category'].widget.attrs.update({'placeholder': 'Choose category'})
        self.fields['image'].widget.attrs.update({'placeholder': 'Upload photo'})
        self.fields['price_per_unit'].widget.attrs.update({'placeholder': 'Enter price'})


class ProductUpdateForm(FormStyleMixin, ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price_per_unit')

    def __init__(self, *args, **kwargs):
        super(ProductUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

        self.helper.attrs = {'class': 'form-control'}
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter name'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Enter description'})
        self.fields['category'].widget.attrs.update({'placeholder': 'Choose category'})
        self.fields['image'].widget.attrs.update({'placeholder': 'Upload photo'})
        self.fields['price_per_unit'].widget.attrs.update({'placeholder': 'Enter price'})


class VersionCreateForm(FormStyleMixin, ModelForm):
    class Meta:
        model = Version
        fields = ('version_name', 'version_number', 'current_version')

    def __init__(self, *args, **kwargs):
        super(VersionCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

        self.helper.attrs = {'class': 'form-control'}
        self.fields['version_name'].widget.attrs.update({'placeholder': 'Enter name'})
        self.fields['version_number'].widget.attrs.update({'placeholder': 'Enter number'})
        self.fields['current_version'].widget.attrs.update({'placeholder': 'Choose version'})


class VersionUpdateForm(FormStyleMixin, ModelForm):
    class Meta:
        model = Version
        fields = ('version_name', 'version_number', 'current_version')

    def __init__(self, *args, **kwargs):
        super(VersionUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

        self.helper.attrs = {'class': 'form-control'}
        self.fields['version_name'].widget.attrs.update({'placeholder': 'Enter name'})
        self.fields['version_number'].widget.attrs.update({'placeholder': 'Enter number'})
        self.fields['current_version'].widget.attrs.update({'placeholder': 'Choose version'})


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price_per_unit', 'is_published')
        success_url = reverse_lazy('products:detail_list')

    def clean_name(self):
        name = self.cleaned_data['name']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word in name.lower():
                raise forms.ValidationError(f'Название не должно содержать запрещенное слово: {word}')
        return name

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

        self.fields['name'].widget.attrs.update({'placeholder': 'Enter name'})
        self.fields['price_per_unit'].widget.attrs.update({'placeholder': 'Enter price'})


ProductForm.base_fields['is_published'].widget.attrs['class'] = 'form-check-input'
