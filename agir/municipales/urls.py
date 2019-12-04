from django.urls import path

from agir.municipales.views import CommuneView, SearchView

urlpatterns = (
    path("communes/chercher/", SearchView.as_view(), name="search_commune"),
    path(
        "communes/<str:code_departement>/<str:slug>/",
        CommuneView.as_view(),
        name="view_commune",
    ),
)
