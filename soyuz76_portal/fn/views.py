from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView

from .models import FnReplacement
from .forms import ExcelUploadForm
from parameters.models import Objects
import openpyxl
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


fn_post = FnReplacement.objects.all()

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class ExcelUploadFormView(SuperuserRequiredMixin, View):
    template_name = 'fn/loading_excel.html'

    def get(self, request):
        form = ExcelUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES.get('excel_file')
            if excel_file:
                try:
                    # Получить все записи в таблице FnReplacement
                    fn_replacements = FnReplacement.objects.all()

                    # Удалить каждую запись в цикле
                    for fn_replacement in fn_replacements:
                        fn_replacement.delete()
                    # Погнали перенос данных
                    wb = openpyxl.load_workbook(excel_file, data_only=True)
                    sheet = wb.active
                    records_processed = 0

                    for row in sheet.iter_rows(min_row=2, values_only=True):
                        if len(row) < 9:
                            row += (None,) * (9 - len(row))

                        name_object, sap, legal_entity, addres_object, nomer_pos, model_fr, sn_fr, sn_fn, date_fp, replacement_date = row

                        if date_fp is not None:
                            if isinstance(date_fp, datetime):
                                date_fp = date_fp.date()
                            else:
                                try:
                                    date_fp = datetime.strptime(date_fp, "%Y-%m-%d").date()
                                except ValueError:
                                    date_fp = None  # Устанавливаем значение как None при неверном формате даты

                        if replacement_date is not None:
                            if isinstance(replacement_date, datetime):
                                replacement_date = replacement_date.date()
                            else:
                                try:
                                    replacement_date = datetime.strptime(replacement_date, "%Y-%m-%d").date()
                                except ValueError:
                                    replacement_date = None  # Устанавливаем значение как None при неверном формате даты

                        # Поиск объектов с совпадающим SAP значением
                        matching_objects = Objects.objects.filter(sap=sap)

                        for object_instance in matching_objects:
                            region_instance = object_instance.regions  # Получение связанного региона
                            # Создание объекта FnReplacement с установленным значением regions
                            fn_replacement = FnReplacement(
                                name_object=name_object,
                                sap=sap,
                                legal_entity=legal_entity,
                                addres_object=addres_object,
                                nomer_pos=nomer_pos,
                                model_fr=model_fr,
                                sn_fr=sn_fr,
                                sn_fn=sn_fn,
                                date_fp=date_fp,
                                replacement_date=replacement_date,
                                regions=region_instance  # Устанавливаем регион
                            )
                            fn_replacement.save()
                            records_processed += 1

                        # Если SAP не совпадает, создаем FnReplacement с regions=None
                        if not matching_objects.exists():
                            fn_replacement = FnReplacement(
                                name_object=name_object,
                                sap=sap,
                                legal_entity=legal_entity,
                                addres_object=addres_object,
                                nomer_pos=nomer_pos,
                                model_fr=model_fr,
                                sn_fr=sn_fr,
                                sn_fn=sn_fn,
                                date_fp=date_fp,
                                replacement_date=replacement_date,
                                regions=None  # Устанавливаем regions в None
                            )
                            fn_replacement.save()
                            records_processed += 1

                    return JsonResponse({'message': 'Загрузка данных завершена успешно.'})
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=500)
            else:
                return JsonResponse({'error': 'Файл не был выбран.'}, status=400)
        else:
            return JsonResponse({'error': 'Неверный формат файла.'}, status=400)



# Общий Mixin для отображения ФН
class CommonViewMixin:
    # Общие методы и атрибуты здесь
    model = FnReplacement
    def get_queryset(self):
        current_date = datetime.now()
        two_months_ago = current_date - timedelta(days=25)

        queryset = self.model.objects.filter(
            replacement_date__isnull=False,
            replacement_date__gte=two_months_ago,
        ).order_by('replacement_date')
        return queryset

        filter_column_name = self.request.GET.get('filter_column_name')
        filter_legal_entity = self.request.GET.get('filter_legal_entity')
        if filter_column_name:
            queryset = queryset.filter(name_object__icontains=filter_column_name)
        if filter_legal_entity:
            queryset = queryset.filter(legal_entity__icontains=filter_legal_entity)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_column_name'] = self.request.GET.get('filter_column_name', '')
        context['filter_legal_entity'] = self.request.GET.get('filter_legal_entity', '')
        context['fn_replacements_page'] = context['page_obj']

        return context


# Передача данных на страницу замены ФН
class FnReplacementListView(CommonViewMixin, ListView):

    template_name = 'base/fn.html'
    context_object_name = 'fn_replacements'
    paginate_by = 10

    def get_queryset(self):
        user_regions = self.request.user.regions.all()  # Получаем все регионы текущего пользователя
        common_queryset = CommonViewMixin().get_queryset()

        if self.request.user.employee_position.name == 'Администратор':
            queryset = common_queryset
        # Фильтруем queryset на основе совпадения регионов пользователя и данных из CommonViewMixin
        else:
            queryset = common_queryset.filter(regions__in=user_regions)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_column_name'] = self.request.GET.get('filter_column_name', '')
        context['filter_legal_entity'] = self.request.GET.get('filter_legal_entity', '')
        context['fn_replacements_page'] = context['page_obj']

        # Добавляем текущего пользователя в контекст
        context['user'] = self.request.user

        return context



def search_fn_replacements(request):
    # Получить параметры поиска из GET-параметров запроса
    search_query = request.GET.get('search_query', '')

    # Выполнить поиск записей в модели FnReplacement на основе поискового запроса
    fn_replacements = FnReplacement.objects.filter(
        Q(name_object__icontains=search_query) |
        Q(legal_entity__icontains=search_query)  # Добавьте другие поля, по которым нужно искать
    ).order_by('replacement_date')

    # Создать объект Paginator с количеством записей на странице равным 100
    paginator = Paginator(fn_replacements, 100)

    # Получить номер текущей страницы из GET-параметра
    page = request.GET.get('page')

    try:
        # Получить объект страницы с номером page
        fn_replacements_page = paginator.page(page)
    except PageNotAnInteger:
        # Если page не является целым числом, отобразить первую страницу
        fn_replacements_page = paginator.page(1)
    except EmptyPage:
        # Если page больше, чем доступное количество страниц, отобразить последнюю страницу
        fn_replacements_page = paginator.page(paginator.num_pages)

    # Определить контекст данных для передачи в шаблон
    context = {
        'fn_replacements_page': fn_replacements_page,
        'search_query': search_query,  # Передача поискового запроса в шаблон
    }

    # Отрендерить HTML шаблон с данными таблицы и результатами поиска
    return render(request, 'base/fn.html', context)


def filter_data(request):
    # Получите параметры фильтрации из POST-запроса
    filter_column_name = request.POST.get('filter_column_name', '')
    filter_legal_entity = request.POST.get('filter_legal_entity', '')
    filter_sap = request.POST.get('filter_sap', '')
    filter_sn_fr = request.POST.get('filter_sn_fr', '')
    filter_sn_fn = request.POST.get('filter_sn_fn', '')

    # Выполните фильтрацию данных на основе полученных параметров
    fn_replacements = FnReplacement.objects.filter(
        name_object__icontains=filter_column_name,
        legal_entity__icontains=filter_legal_entity,
        sap__icontains=filter_sap,  # Фильтрация по SAP
        sn_fr__icontains=filter_sn_fr,  # Фильтрация по серийному номеру ФР
        sn_fn__icontains=filter_sn_fn  # Фильтрация по серийному номеру ФН
        # Добавьте другие фильтры по необходимости
    ).order_by('replacement_date')

    # Определите контекст данных для передачи в шаблон
    context = {
        'fn_replacements': fn_replacements
    }

    # Отрендерите часть HTML с отфильтрованными данными и отправьте ее обратно на клиент
    html_response = render(request, 'base/partial_filtered_data.html', context)

    # Преобразуйте HTML-ответ в текст и верните его
    return JsonResponse({'filtered_data': html_response.content.decode()})



