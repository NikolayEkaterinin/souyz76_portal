from django.urls import path, reverse_lazy, include
from django.contrib.auth import views
from .views import IndexPagesView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

app_name = 'pages'

urlpatterns = [
    path('', IndexPagesView.as_view(), name='index'),
    # Логин.
    path('login/',
         views.LoginView.as_view(template_name='login.html'),
         name='login',),
    # Логаут.
    path(
        'logout/',
        views.LogoutView.as_view(template_name='logged_out.html'),
        name='logout',
    ),

    # Изменение пароля.
    path('password_change/',
         views.LogoutView.as_view(template_name='password_change_form.html'),
         name='password_change',
         ),
    # Сообщение об успешном изменении пароля.
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Восстановление пароля.
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # Сообщение об отправке ссылки для восстановления пароля.
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # Вход по ссылке для восстановления пароля.
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # Сообщение об успешном восстановлении пароля.
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('pages:homepage'),
        ),
        name='registration',
    ),
]