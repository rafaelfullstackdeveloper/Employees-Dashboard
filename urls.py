#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Define as rotas da API para o aplicativo job_tracker e configura as URLs do projeto.
#
# Author:      rafaelfullstackdeveloper
#
# Created:     31/05/2025
# Copyright:   (c) rafaelfullstackdeveloper 2025
# Licence:     GNU
#-------------------------------------------------------------------------------

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobSiteViewSet, JobApplicationViewSet, ApplicationTimelineViewSet

# Inicializa o roteador padrão do Django REST Framework para registrar viewsets automaticamente.
router = DefaultRouter()

# Registra o ViewSet JobSiteViewSet na rota 'job-sites', gerando endpoints para operações CRUD.
router.register(r'job-sites', JobSiteViewSet)

# Registra o ViewSet JobApplicationViewSet na rota 'applications', gerando endpoints para operações CRUD.
router.register(r'applications', JobApplicationViewSet)

# Registra o ViewSet ApplicationTimelineViewSet na rota 'timeline', gerando endpoints para operações CRUD.
router.register(r'timeline', ApplicationTimelineViewSet)

# Define as URLs do aplicativo job_tracker, incluindo todas as rotas geradas pelo roteador sob o prefixo 'api/'.
urlpatterns = [
    path('api/', include(router.urls)),  # Inclui as rotas da API geradas pelo roteador.
]

from django.contrib import admin
from django.urls import path, include

# Define as URLs principais do projeto, incluindo o painel administrativo e as rotas do aplicativo job_tracker.
urlpatterns = [
    path('admin/', admin.site.urls),  # Rota para o painel administrativo do Django.
    path('', include('job_tracker.urls')),  # Inclui as URLs do aplicativo job_tracker na raiz do projeto.
]