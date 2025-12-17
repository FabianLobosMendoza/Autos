"""URL patterns for clients app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('crear/', views.client_create, name='client_create'),
    path('<int:client_id>/', views.client_detail, name='client_detail'),
    path('<int:client_id>/editar/', views.client_edit, name='client_edit'),
    path('<int:client_id>/imprimir/', views.client_contract, name='client_contract'),
    path('<int:client_id>/pdf/', views.client_pdf, name='client_pdf'),
    path('calendario/', views.client_calendar, name='client_calendar'),
    path('calendario/<int:event_id>/editar/', views.client_event_edit, name='client_event_edit'),
    path('calendario/<int:event_id>/eliminar/', views.client_event_delete, name='client_event_delete'),
    path('leads/<int:lead_id>/nota/', views.client_lead_note_add, name='client_lead_note_add'),
    path('leads/<int:lead_id>/entrevista/', views.lead_interview_create, name='lead_interview_create'),
    path('leads/<int:lead_id>/eliminar/', views.client_lead_delete, name='client_lead_delete'),
]
