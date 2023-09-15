from django.urls import path
from .views import ExcelUploadFormView, FnReplacementListView , search_fn_replacements, filter_data, FnListView

app_name = 'fn'

urlpatterns = [
    path('fill_database/', ExcelUploadFormView.as_view(), name='fill_database'),
    # path('fn_replacement_table/', fn_replacement_table, name='fn_replacement_table'),
    path('fn_list/', FnReplacementListView.as_view(), name='fn_list'),
    path('search/', search_fn_replacements, name='search_fn_replacements'),
    path('filter-data/', filter_data, name='filter_data'),


]
