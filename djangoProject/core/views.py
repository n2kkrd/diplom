from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.forms import StaffForm, CriteriaForm, IntegralYearForm
from core.models import Staff, Year, Criteria, Month, BigReportStaff, IntegralYear
from django.http import JsonResponse, QueryDict


@login_required(login_url='/register/')
def home(request):
    context = {'title': 'Home page'}
    return redirect('staff')
    # return render(request, 'general/home.html', context)


@login_required(login_url='/register/')
def staff(request):
    if request.method == 'POST':
        staff_form = StaffForm(request.POST)

        if staff_form.is_valid():
            staff_form.save()
    else:
        staff_form = StaffForm()

    context = {
        'title': 'Сотрудники',
        'staff_form': staff_form,
        'staff': Staff.objects.all(),
    }
    return render(request, 'general/staff.html', context)


@login_required(login_url='/register/')
def report(request):
    if request.method == 'POST':
        for id_criteria, value in request.POST.dict().items():
            try:
                c = Criteria.objects.get(id=int(id_criteria))
                c.value = float(value)
                c.save()
            except (Criteria.DoesNotExist, ValueError):
                pass

        return JsonResponse({'result': 'success'}, status=200)

    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    year = request.GET.get('year')
    month = request.GET.get('month')

    try:
        staff_obj = Staff.objects.get(first_name=first_name, last_name=last_name)
    except Month.DoesNotExist:
        return ''

    try:
        year_obj = staff_obj.year.get(title=year)
    except Year.DoesNotExist:
        year_obj = Year(staff=staff_obj, title=year)
        year_obj.save()

    try:
        month_obj = year_obj.month.get(title=month)
    except Month.DoesNotExist:
        month_obj = Month(year=year_obj, title=month)
        month_obj.save()

        for c in Criteria.objects.filter(big_report__isnull=True, month__isnull=True).order_by('title'):
            c.id = None
            c.month = month_obj
            c.save()

    context = {
        'title': f'Отчет {first_name} {last_name}',
        'month_obj': month_obj,
    }
    return render(request, 'general/report.html', context)


@login_required(login_url='/register/')
def criteria(request):
    if request.method == 'POST':
        form = CriteriaForm(request.POST)
        if form.is_valid():
            form.save()
    elif request.method == 'DELETE':
        id_criteria = QueryDict(request.body).get('id')
        obj_criteria = Criteria.objects.get(id=int(id_criteria))
        obj_criteria.delete()
        return JsonResponse({'result': 'success'}, status=200)
    else:
        form = CriteriaForm()

    context = {
        'title': 'Критерии',
        'criteria': Criteria.objects.filter(big_report__isnull=True) & Criteria.objects.filter(month__isnull=True),
        'form': form
    }
    return render(request, 'general/criteria.html', context)


@login_required(login_url='/register/')
def big_report(request):
    if request.method == 'POST':

        start_date_year = request.POST.dict().get('start_date_year')
        start_date_month = request.POST.dict().get('start_date_month')
        end_date_year = request.POST.dict().get('end_date_year')
        end_date_month = request.POST.dict().get('end_date_month')

        date_start_end = [f"{start_date_year}-{start_date_month}-01", f"{end_date_year}-{end_date_month}-01"]

        staff_first_name = request.POST.dict().get('first_name', '')
        staff_last_name = request.POST.dict().get('last_name', '')

        staff_obj = None
        if staff_first_name and staff_last_name:
            try:
                staff_obj = Staff.objects.get(first_name=staff_first_name, last_name=staff_last_name)
            except Month.DoesNotExist:
                return ''

        big_report_obj = BigReportStaff(staff=staff_obj,
                                        first_year=int(start_date_year),
                                        first_month=int(start_date_month),
                                        last_year=int(end_date_year),
                                        last_month=int(end_date_month),
                                        )
        big_report_obj.save()

        for blank_criteria in Criteria.objects.filter(month=None, big_report=None):
            cache_value = 0
            counter = 0

            if staff_obj:
                criterias = Criteria.objects.filter(title=blank_criteria.title, create_date__range=date_start_end, month__year__staff=staff_obj)
            else:
                one = Criteria.objects.filter(title=blank_criteria.title, create_date__range=date_start_end, big_report__isnull=False)
                two = Criteria.objects.filter(title=blank_criteria.title, create_date__range=date_start_end, month__isnull=False)
                criterias = one | two

            for one_criteria in criterias:
                cache_value += one_criteria.value
                counter += 1

            if counter:
                cache_value /= counter

            c = Criteria(title=blank_criteria.title, value=cache_value, big_report=big_report_obj)
            c.save()
        return JsonResponse({'result': 'success'}, status=200)
    elif request.method == 'DELETE':
        id_big_report = QueryDict(request.body).get('id_big_report')
        try:
            obj_big_report = BigReportStaff.objects.get(id=int(id_big_report))
            obj_big_report.delete()
            return JsonResponse({'result': 'success'}, status=200)
        except BigReportStaff.DoesNotExist:
            return JsonResponse({'result': 'error'}, status=500)

    elif request.method == 'GET':
        context = {
            'title': 'Отчеты',
            'staff': Staff.objects.all(),
            'staff_big_reports': BigReportStaff.objects.filter(staff__isnull=False),
            'company_big_reports': BigReportStaff.objects.filter(staff__isnull=True),
        }
        return render(request, 'general/big_report.html', context)


@login_required(login_url='/register/')
def view_big_report(request, report_id):
    report_obj = BigReportStaff.objects.get(id=int(report_id))

    context = {
        'title': 'Отчет',
        'report_obj': report_obj,
    }
    return render(request, 'general/view_big_report.html', context)


@login_required(login_url='/register/')
def integral_indicator(request):
    if request.method == 'POST':
        fields = request.POST.dict()
        try:
            year_obj = IntegralYear.objects.get(title=int(fields.get('title')))
        except IntegralYear.DoesNotExist:
            year_obj = IntegralYear()

        year_obj.title = int(fields.get('title'))
        year_obj.value_product = int(fields.get('value_product'))
        year_obj.fond_zp = int(fields.get('fond_zp'))
        year_obj.average_annual_value_capital = int(fields.get('average_annual_value_capital'))
        year_obj.average_annual_value_fond = int(fields.get('average_annual_value_fond'))
        year_obj.w = int(fields.get('w'))
        year_obj.average_zp = int(fields.get('average_zp'))
        year_obj.profit_before_tax = int(fields.get('profit_before_tax'))

        year_obj.economy_effectiveness = year_obj.value_product / (year_obj.fond_zp + (year_obj.average_annual_value_capital + year_obj.average_annual_value_fond) * 0.12)
        year_obj.soc_effectiveness = year_obj.w / year_obj.average_zp
        year_obj.financial_efficiency = year_obj.profit_before_tax/(year_obj.fond_zp + (year_obj.average_annual_value_capital + year_obj.average_annual_value_fond) * 0.12)
        year_obj.indicators_of_the_use_resources = (year_obj.economy_effectiveness * year_obj.soc_effectiveness * year_obj.financial_efficiency) ** 0.5

        year_obj.save()

    form = IntegralYearForm()
    years_objects = IntegralYear.objects.order_by('title')

    context = {
        'title': 'Интегральный показатель',
        'form': form,
        'years': years_objects,
    }
    return render(request, 'general/integral_indicator.html', context)
