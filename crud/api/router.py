from django.urls import path
from rest_framework.routers import DefaultRouter
from crud.api.views import UserApiViewSet

router_crud = DefaultRouter()
router_crud.register(prefix='crud', basename='crud', viewset=UserApiViewSet)
