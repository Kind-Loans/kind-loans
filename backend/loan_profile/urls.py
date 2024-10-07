"""
URLs for the loan_profile app.
"""

from django.urls import path, include
from rest_framework_nested import routers
from loan_profile import views


router = routers.SimpleRouter()
router.register(r"loanprofile", views.LoanProfileViewSet)

app_name = "loan_profile"

loanupdates_router = routers.NestedSimpleRouter(
    router, r"loanprofile", lookup="loan_profile"
)
loanupdates_router.register(
    r"updates", views.LoanUpdateViewSet, basename="loanprofile-updates"
)

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(loanupdates_router.urls)),
]
