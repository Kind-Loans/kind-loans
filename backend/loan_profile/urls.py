"""
URLs for the loan_profile app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from loan_profile import views


router = DefaultRouter()
router.register("loanprofile", views.LoanProfileViewSet)

app_name = "loan_profile"

urlpatterns = [
    path("", include(router.urls)),
]
