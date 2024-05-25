from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "essay/<int:essay_id>/full_submission/",
        views.full_submission,
        name="full_submission",
    ),
    path(
        "essay/<int:essay_id>/full_feedback/", views.full_feedback, name="full_feedback"
    ),
    path("submit/", views.submit_essay, name="submit_essay"),
    path("essays/", views.essay_list, name="essay_list"),
]
 