from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PatientViewSet, AppointmentViewSet, TreatmentRecordViewSet, MessageViewSet

router = SimpleRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'treatments', TreatmentRecordViewSet, basename='treatment')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
