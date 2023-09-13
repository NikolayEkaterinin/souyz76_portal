from django.urls import path, reverse_lazy, include
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .views import (
    IndexListView,
    AboutRegistrationView,
    InstructionDetailView,
    InstructionCreateView,
    InstructionDeleteView,
    InstructionUpdateView,
    ProfileDetailView,
    ProfileUpdateView,
    CategoryListView,
    CategoryCreateView,
    InstructionCategoryListView,
    ProfileAdminDetailView,
    PostDetailView
)
from django.views.generic.edit import CreateView
from user.forms import RegistrationForm

app_name = 'pages'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    # urls страниц инструкций
    path('instructions/<int:pk>', InstructionDetailView.as_view(), name='detail'),
    path('instructions/create', InstructionCreateView.as_view(), name='create'),
    path('instructions/<int:pk>/delete', InstructionDeleteView.as_view(), name='delete'),
    path('instructions/<int:pk>/update', InstructionUpdateView.as_view(), name='update'),
    # urls профиля
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile'),
    path('profile/<str:username>/admin', ProfileAdminDetailView.as_view(), name='profile_admin'),
    path('profile/<str:username>/edit', ProfileUpdateView.as_view(), name='profile_edit'),

    # Post urls
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),

    # ursl категории
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/create/', CategoryCreateView.as_view(), name='create_category'),

    path('instructions/category/<slug:category_slug>/', InstructionCategoryListView.as_view(), name='instructions_category_list'),

    # Логин.
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),

    path('about_registration/', AboutRegistrationView.as_view(template_name='registration/about_registration.html'), name='about_registration'),

    # Логаут.
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),

    # Изменение пароля.
    path('password_change/', PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    # Сообщение об успешном изменении пароля.
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Восстановление пароля.
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    # Сообщение об отправке ссылки для восстановления пароля.
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # Вход по ссылке для восстановления пароля.
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # Сообщение об успешном восстановлении пароля.
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=RegistrationForm,
            success_url=reverse_lazy('pages:about_registration'),
        ),
        name='registration',
    ),
]
