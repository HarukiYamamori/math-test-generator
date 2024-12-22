from django.urls import path

from myapp.views import MathTestGeneratorAPIView

urlpatterns = [
    path('generate/', MathTestGeneratorAPIView.as_view(), name='generate-math-tests'),
]