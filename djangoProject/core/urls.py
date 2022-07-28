from django.urls import path
from .views import home, staff, criteria, report, big_report, view_big_report, integral_indicator

urlpatterns = [
    path('', home, name='home'),
    path('staff', staff, name='staff'),
    path('report', report, name='report'),
    path('criteria', criteria, name='criteria'),

    path('big_report', big_report, name='big_report'),
    path('view_big_report/<int:report_id>', view_big_report, name='view_big_report'),

    path('integral_indicator', integral_indicator, name='integral_indicator')
]
