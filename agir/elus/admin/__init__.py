from datetime import datetime

import reversion
from data_france.models import (
    Commune,
    CollectiviteDepartementale,
    CollectiviteRegionale,
)
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from psycopg2._range import DateRange

from agir.elus.models import (
    MandatMunicipal,
    MandatDepartemental,
    MandatRegional,
    MUNICIPAL_DEFAULT_DATE_RANGE,
    DEPARTEMENTAL_DEFAULT_DATE_RANGE,
    REGIONAL_DEFAULT_DATE_RANGE,
)
from agir.lib.search import PrefixSearchQuery
from agir.people.models import Person
from .filters import (
    CommuneFilter,
    DepartementFilter,
    DepartementRegionFilter,
    RegionFilter,
)
from .forms import (
    PERSON_FIELDS,
    CreerMandatForm,
    CreerMandatMunicipalForm,
)


class BaseMandatAdmin(admin.ModelAdmin):
    form = CreerMandatForm
    add_form_template = "admin/change_form.html"
    change_form_template = "elus/admin/history_change_form.html"
    search_fields = ("person",)
    default_date_range = None

    def get_conseil_queryset(self, request):
        raise NotImplementedError("Implémenter cette méthode est obligatoire")

    def get_form(self, request, obj=None, change=False, **kwargs):
        form_class = super(BaseMandatAdmin, self).get_form(
            request, obj, change, **kwargs
        )
        if "conseil" in form_class.base_fields:
            form_class.base_fields["conseil"].queryset = self.get_conseil_queryset(
                request
            )

        return form_class

    def get_fieldsets(self, request, obj=None):
        """Permet de ne pas afficher les mêmes champs à l'ajout et à la modification

        S'il y a ajout, on ne veux pas montrer le champ de choix de l'email officiel.
        S'il y a modification, on veut montrer le lien vers la personne plutôt que la personne.
        """
        can_view_person = request.user.has_perm("people.view_person")

        # cas de la création d'un nouveau mandat
        if obj is None:
            return tuple(
                (
                    title,
                    {
                        **params,
                        "fields": tuple(
                            f for f in params["fields"] if f != "email_officiel"
                        ),
                    },
                )
                for title, params in self.fieldsets
            )

        additional_fieldsets = ()
        if obj.person is not None:
            person = obj.person
            models = [MandatMunicipal, MandatDepartemental, MandatRegional]
            fields = [
                "mandats_municipaux",
                "mandats_departementaux",
                "mandats_regionaux",
            ]
            current_model = self.model
            querysets = [
                model.objects.exclude(id=obj.id)
                if model == current_model
                else model.objects.all()
                for model in models
            ]
            autres_mandats = [qs.filter(person=person).exists() for qs in querysets]

            if any(autres_mandats):
                additional_fieldsets += (
                    (
                        "Autres mandats",
                        {
                            "fields": tuple(
                                f for f, ex in zip(fields, autres_mandats) if ex
                            )
                        },
                    ),
                )

        if can_view_person:
            return (
                tuple(
                    (
                        (
                            title,
                            {
                                **params,
                                "fields": tuple(
                                    f if f != "person" else "person_link"
                                    for f in params["fields"]
                                ),
                            },
                        )
                        for title, params in self.fieldsets
                    )
                )
                + additional_fieldsets
            )
        return self.fieldsets + additional_fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj) + (
            "actif",
            "person_link",
            "mandats_municipaux",
            "mandats_departementaux",
            "mandats_regionaux",
        )

        if obj is not None:
            return readonly_fields + ("person", "conseil")
        return readonly_fields

    def get_autocomplete_fields(self, request):
        return super().get_autocomplete_fields(request) + ("person",)

    def get_search_results(self, request, queryset, search_term):
        use_distinct = False
        if search_term:
            return (
                queryset.filter(
                    person__search=PrefixSearchQuery(
                        search_term, config="simple_unaccented"
                    )
                ),
                use_distinct,
            )
        return queryset, use_distinct

    def actif(self, obj):
        return "Oui" if (timezone.now().date() in obj.dates) else "Non"

    actif.short_description = "Mandat en cours"

    def person_link(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            reverse("admin:people_person_change", args=[obj.person_id]),
            str(obj.person),
        )

    person_link.short_description = "Profil de l'élu"

    def is_insoumise(self, obj):
        if obj.person:
            return "Oui" if obj.person.is_insoumise else "Non"
        return "-"

    is_insoumise.short_description = "Insoumis⋅e"

    def get_changeform_initial_data(self, request):
        """Permet de préremplir le champs `dates' en fonction de la dernière élection"""
        initial = super().get_changeform_initial_data(request)
        initial.setdefault("dates", self.default_date_range)

        if "person" in request.GET:
            try:
                initial["person"] = Person.objects.get(pk=request.GET["person"])
            except Person.DoesNotExist:
                pass

        if "conseil" in request.GET:
            try:
                initial["conseil"] = self.get_conseil_queryset(request).get(
                    code=request.GET["conseil"]
                )
            except ObjectDoesNotExist:
                pass

        if "debut" in request.GET and "fin" in request.GET:
            try:
                initial["dates"] = DateRange(
                    datetime.strptime(request.GET["debut"], "%Y-%m-%d").date(),
                    datetime.strptime(request.GET["fin"], "%Y-%m-%d").date(),
                )
            except ValueError:
                pass

        return initial

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        with reversion.create_revision():
            reversion.set_comment("Depuis l'interface d'aministration")
            reversion.set_user(request.user)
            return super().changeform_view(request, object_id, form_url, extra_context)

    def mandats_municipaux(self, obj=None):
        person = obj.person

        mandats = MandatMunicipal.objects.filter(person=person)

        return format_html_join(
            mark_safe("<br>"),
            '<a href="{}">{}</a>',
            (
                (
                    reverse("admin:elus_mandatmunicipal_change", args=(m.id,)),
                    f"{m.conseil.nom_complet}, {m.get_mandat_display()}",
                )
                for m in mandats
                if m != obj
            ),
        )

    mandats_municipaux.short_description = "Mandats municipaux"

    def mandats_departementaux(self, obj=None):
        person = obj.person

        mandats = MandatDepartemental.objects.filter(person=person)
        return format_html_join(
            mark_safe("<br>"),
            '<a href="{}">{}</a>',
            (
                (
                    reverse("admin:elus_mandatdepartemental_change", args=(m.id,)),
                    f"{m.conseil.nom}, {m.get_mandat_display()}",
                )
                for m in mandats
                if m != obj
            ),
        )

    mandats_departementaux.short_description = "Mandats départementaux"

    def mandats_regionaux(self, obj=None):
        person = obj.person

        mandats = MandatRegional.objects.filter(person=person)
        return format_html_join(
            mark_safe("<br>"),
            '<a href="{}">{}</a>',
            (
                (
                    reverse("admin:elus_mandatregional_change", args=(m.id,)),
                    f"{m.conseil.nom}, {m.get_mandat_display()}",
                )
                for m in mandats
                if m != obj
            ),
        )

    mandats_regionaux.short_description = "Mandats régionaux"

    def membre_reseau_elus(self, object):
        return object.person.get_membre_reseau_elus_display()

    membre_reseau_elus.short_description = "Membre du réseau ?"
    membre_reseau_elus.admin_order_field = "person__membre_reseau_elus"


@admin.register(MandatMunicipal)
class MandatMunicipalAdmin(BaseMandatAdmin):
    form = CreerMandatMunicipalForm
    autocomplete_fields = ("conseil",)
    default_date_range = MUNICIPAL_DEFAULT_DATE_RANGE

    list_filter = (
        "statut",
        "mandat",
        CommuneFilter,
        DepartementFilter,
        DepartementRegionFilter,
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "person",
                    "conseil",
                    "statut",
                    "membre_reseau_elus",
                    "mandat",
                    "communautaire",
                    "commentaires",
                )
            },
        ),
        (
            "Informations sur l'élu⋅e",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email_officiel",
                    "contact_phone",
                    "location_address1",
                    "location_address2",
                    "location_zip",
                    "location_city",
                    "new_email",
                )
            },
        ),
        ("Précisions sur le mandat", {"fields": ("dates", "delegations")},),
    )

    list_display = (
        "person",
        "conseil",
        "mandat",
        "membre_reseau_elus",
        "statut",
        "actif",
        "communautaire",
        "is_insoumise",
    )

    def get_conseil_queryset(self, request):
        return Commune.objects.filter(
            type__in=[Commune.TYPE_COMMUNE, Commune.TYPE_SECTEUR_PLM]
        )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("person")

    class Media:
        pass


@admin.register(MandatDepartemental)
class MandatDepartementAdmin(BaseMandatAdmin):
    autocomplete_fields = ("conseil",)
    list_filter = ("statut", "mandat", DepartementFilter, DepartementRegionFilter)
    default_date_range = DEPARTEMENTAL_DEFAULT_DATE_RANGE

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "person",
                    "conseil",
                    "statut",
                    "membre_reseau_elus",
                    "mandat",
                    "commentaires",
                )
            },
        ),
        (
            "Informations sur l'élu⋅e",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email_officiel",
                    "contact_phone",
                    "location_address1",
                    "location_address2",
                    "location_zip",
                    "location_city",
                    "new_email",
                )
            },
        ),
        ("Précisions sur le mandat", {"fields": ("dates", "delegations")},),
    )

    list_display = (
        "person",
        "conseil",
        "mandat",
        "membre_reseau_elus",
        "statut",
        "actif",
        "is_insoumise",
    )

    def get_conseil_queryset(self, request):
        return CollectiviteDepartementale.objects.all()

    class Media:
        pass


@admin.register(MandatRegional)
class MandatRegionalAdmin(BaseMandatAdmin):
    list_filter = ("statut", "mandat", RegionFilter)
    default_date_range = REGIONAL_DEFAULT_DATE_RANGE

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "person",
                    "conseil",
                    "statut",
                    "membre_reseau_elus",
                    "mandat",
                    "commentaires",
                )
            },
        ),
        (
            "Informations sur l'élu⋅e",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email_officiel",
                    "contact_phone",
                    "location_address1",
                    "location_address2",
                    "location_zip",
                    "location_city",
                    "new_email",
                )
            },
        ),
        ("Précisions sur le mandat", {"fields": ("dates", "delegations")},),
    )

    list_display = (
        "person",
        "conseil",
        "mandat",
        "membre_reseau_elus",
        "statut",
        "actif",
        "is_insoumise",
    )

    readonly_fields = (
        "actif",
        "person_link",
    )

    def get_conseil_queryset(self, request):
        return CollectiviteRegionale.objects.all()

    class Media:
        pass
