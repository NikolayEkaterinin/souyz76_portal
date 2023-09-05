from django.urls import path
from .views import RulesPagesView, AboutPageView, IndexPagesView

app_name = 'pages'

urlpatterns = [
   path('about/', AboutPageView.as_view(), name='about'),
   path('rules/', RulesPagesView.as_view(), name='rules'),
    path('', IndexPagesView.as_view(), name='index')
]