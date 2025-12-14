from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet, BranchViewSet, DepartmentViewSet, PositionViewSet, UserViewSet, GroupViewSet,
    CategoryViewSet, ItemViewSet, StockMovementViewSet, MessageViewSet,
    login_view, logout_view, current_user, get_csrf_token, create_user_account, change_password
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'items', ItemViewSet)
router.register(r'stock-movements', StockMovementViewSet)
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('csrf/', get_csrf_token, name='csrf'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('current-user/', current_user, name='current-user'),
    path('create-user-account/', create_user_account, name='create-user-account'),
    path('change-password/', change_password, name='change-password'),
]
