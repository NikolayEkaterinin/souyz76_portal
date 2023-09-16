from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages  # Импорт фреймворка для сообщений
from .models import FnReplacement
from .forms import ExcelUploadForm
import openpyxl
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class ExcelUploadFormView(SuperuserRequiredMixin, View):
    template_name = 'objects_loading_excel.html'

    def get(self, request):
        form = ExcelUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES.get('excel_file')
            if excel_file:
                try:
                    # Удалить все существующие записи перед загрузкой новых данных
                    FnReplacement.objects.all().delete()

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
                            replacement_date=replacement_date
                        )
                        fn_replacement.save()
                        records_processed += 1

                    # Добавьте сообщение об успешной загрузке с количеством обработанных строк
                    messages.success(request, f'Загрузка данных завершена успешно. Внесено {records_processed} строк.')

                    # Редирект на страницу с графиком
                    return redirect('название-URL-страницы-с-графиком')  # Замените на реальное название URL для страницы с графиком
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=500)
            else:
                return JsonResponse({'error': 'Файл не был выбран.'}, status=400)
        else:
            return JsonResponse({'error': 'Неверный формат файла.'}, status=400)
