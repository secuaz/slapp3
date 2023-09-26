from django.urls import path
from . import views

urlpatterns = [
    path('machine/', views.MachineListView.as_view(), name='machine-list'),
    path('machine/new', views.MachineCreateView.as_view(), name='new-machine'),
    path('machine/<pk>/edit', views.MachineUpdateView.as_view(), name='edit-machine'),
    path('machine/<pk>/delete', views.MachineDeleteView.as_view(), name='delete-machine'),
    path('machine/<name>', views.MachineView.as_view(), name='machine'),

    path('production/', views.ProductionView.as_view(), name='production-list'), 
    path('production/new', views.SelectMachineView.as_view(), name='select-machine'), 
    path('production/new/<pk>', views.ProductionCreateView.as_view(), name='new-production'),    
    path('production/<pk>/delete', views.ProductionDeleteView.as_view(), name='delete-production'),
    
    path('dispatch/', views.DispatchView.as_view(), name='dispatch-list'),
    path('dispatch/new', views.DispatchCreateView.as_view(), name='new-dispatch'),
    path('dispatch/<pk>/delete', views.DispatchDeleteView.as_view(), name='delete-dispatch'),

    path("production/<orderno>", views.ProductionOrderView.as_view(), name="production-order"),
    path("dispatch/<orderno>", views.DispatchOrderView.as_view(), name="dispatch-order"),
]