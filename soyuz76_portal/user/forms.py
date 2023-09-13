import os
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser
from parameters.models import Regions, EmployeePosition

# Создаем кастомный виджет для текстовых полей с фиксированной высотой
class CustomTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['style'] = 'height: 30px;'  # Задаем желаемую высоту здесь


# Форма регистрации пользователей, основанная на UserCreationForm
class RegistrationForm(UserCreationForm):
    # Поле для выбора регионов (множественный выбор)
    regions = forms.ModelMultipleChoiceField(
        queryset=Regions.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Регионы'  # Метка для поля
    )

    # Поле для выбора должности (одиночный выбор)
    employee_position = forms.ModelChoiceField(
        queryset=EmployeePosition.objects.all(),
        widget=forms.Select,
        required=True,
        label='Должность'  # Метка для поля
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

    # Поле для имени пользователя
    username = forms.CharField(widget=CustomTextInput, label='Имя пользователя')

    # Поле для имени пользователя
    first_name = forms.CharField(widget=CustomTextInput, label='Имя')

    # Поле для фамилии пользователя
    last_name = forms.CharField(widget=CustomTextInput, label='Фамилия')

    # Поле для адреса электронной почты
    email = forms.EmailField(widget=CustomTextInput, label='Email')

    # Поле для даты рождения с кастомным виджетом
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'style': 'height: 30px;'}),
        required=True,
        label='Дата рождения'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'birthday', 'regions', 'employee_position')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        regions = self.cleaned_data.get("regions")
        if regions:
            user.regions.set(regions)

        user.regions.set(self.cleaned_data["regions"])

        # Получаем выбранную должность
        selected_employee_position = self.cleaned_data["employee_position"]

        # Устанавливаем выбранную должность пользователю
        user.employee_position = selected_employee_position

        # Если выбранная должность - "Инженер"
        if selected_employee_position.name == "Инженер":
            base_folder = "PPR"  # Базовая папка
            region_names = [region.name for region in self.cleaned_data["regions"]]
            engineer_folder = os.path.join(base_folder, *region_names, f"{user.first_name}_{user.last_name}")

            if not os.path.exists(engineer_folder):
                os.makedirs(engineer_folder)

            # Сохраняем путь к папке инженера в базе данных
            user.engineer_folder_path = engineer_folder
            user.save()

        return user


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'last_name', 'first_name', 'birthday', 'email']
