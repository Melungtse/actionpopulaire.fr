from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.views.generic import View

from events.models import Event
from groups.models import SupportGroup


class NBUrlsView(View):
    nb_paths = {
        '/users/event_pages/new?parent_id=103': reverse_lazy('create_event'),
        '/users/event_pages/new?parent_id=73': reverse_lazy('create_group'),
        '/users/event_pages/new?parent_id=38840': reverse_lazy('create_event'),
        '/agir': reverse_lazy('volunteer'),
        '/inscription_detail': reverse_lazy('change_profile'),
        '/projet': 'https://avenirencommun.fr/avenir-en-commun/',
        '/le_projet': 'https://avenirencommun.fr/avenir-en-commun/',
        '/livrets_thematiques': 'https://avenirencommun.fr/livrets-thematiques/',
        '/convention': 'https://convention.jlm2017.fr/',
        '/commander_du_materiel': 'https://materiel.lafranceinsoumise.fr/',
        '/materiel': 'https://materiel.lafranceinsoumise.fr/',
        '/actualites': 'https://lafranceinsoumise.fr/actualites/',
        '/le_blog': 'http://melenchon.fr/',
        '/donner': 'https://lafranceinsoumise.fr/',
        '/groupes_appui': 'https://lafranceinsoumise.fr/carte',
        '/groupes_d_appui': 'https://lafranceinsoumise.fr/carte',
        '/groupes_proches': 'https://lafranceinsoumise.fr/carte',
        '/groupes_appui_redirige': 'https://lafranceinsoumise.fr/carte',
        '/evenements_locaux_redirige': 'https://lafranceinsoumise.fr/carte',
        '/evenements_locaux': 'https://lafranceinsoumise.fr/carte',
        '/les_groupes_d_appui': 'https://lafranceinsoumise.fr/carte',
        '/groupes_proches': 'https://lafranceinsoumise.fr/groupes-appui/carte-groupes-dappui/',
        '/evenements_proches': 'https://lafranceinsoumise.fr/groupes-appui/carte-groupes-dappui/',
        '/caravanes_liste': 'https://lafranceinsoumise.fr/groupes-appui/les-casserolades/',
        '/carte': 'https://lafranceinsoumise.fr/carte',
        '/merci': 'https://lafranceinsoumise.fr/merci',
        '/18_mrs': 'https://18mars2017.fr/',
        '/universites_populaires': 'https://avenirencommun.fr/univpop_programme/',
    }

    def get(self, request, nb_path):
        try:
            event = Event.objects.get(nb_path=nb_path)
            return HttpResponsePermanentRedirect(reverse('view_event', args=[event.id]))
        except Event.DoesNotExist:
            pass

        try:
            group = SupportGroup.objects.get(nb_path=nb_path)
            return HttpResponsePermanentRedirect(reverse('view_group', args=[group.id]))
        except SupportGroup.DoesNotExist:
            pass

        try:
            nb_url = nb_path
            if request.META['QUERY_STRING']:
                nb_url = nb_url + '?' + request.META['QUERY_STRING']
            url = self.nb_paths[nb_url]
            return HttpResponsePermanentRedirect(url)
        except KeyError:
            pass

        return HttpResponse(status=503)
