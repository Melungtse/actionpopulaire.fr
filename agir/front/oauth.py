import logging
import sys

from django.views.generic import RedirectView
from django.conf import settings
from django.utils.http import is_safe_url
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login, logout, BACKEND_SESSION_KEY, SESSION_KEY
from django.core.urlresolvers import reverse, reverse_lazy

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, MissingTokenError


logger = logging.getLogger(__name__)


def oauth_error_page(request, *, error_code=None):
    exc_type, exc, traceback = sys.exc_info()

    if error_code is None and exc_type is not None:
        error_code = exc_type.__name__

    if exc is not None:
        logger.warning('OAuth error', exc_info=True)

    return TemplateResponse(
        request=request,
        template='oauth_error.html',
        context={'error_code': error_code},
        content_type='text/html',
        status=400,
    )


class OauthRedirectView(RedirectView):
    http_method_names = ['get']

    def get_redirect_url(self, *args, **kwargs):
        client = OAuth2Session(
            client_id=settings.OAUTH['client_id'],
            redirect_uri=settings.OAUTH['redirect_domain'] + reverse('oauth_return_view'),
            scope=['view_profile'],
        )

        # extract next url
        next_url = self.request.GET.get('next', None)

        # save it to the session
        if next_url and is_safe_url(next_url):
            self.request.session['login_next_url'] = next_url

        # the user is then redirected to the auth provider with the right parameters
        url, state = client.authorization_url(settings.OAUTH['authorization_url'])

        # the nonce is saved inside the session
        self.request.session['oauth2_nonce'] = state
        return url


class OauthReturnView(RedirectView):
    http_method_names = ['get']
    default_url = reverse_lazy('change_profile')

    def get(self, request, *args, **kwargs):
        state_nonce = request.session.get('oauth2_nonce', None)

        if state_nonce is None:
            return oauth_error_page(request, error_code='NoStateError')

        client = OAuth2Session(
            client_id=settings.OAUTH['client_id'],
            redirect_uri=settings.OAUTH['redirect_domain'] + reverse('oauth_return_view'),
            scope=['view_profile'],
            state=state_nonce,
        )

        try:
            token = client.fetch_token(
                token_url=settings.OAUTH['token_exchange_url'],
                authorization_response=self.request.build_absolute_uri(),
                client_id=settings.OAUTH['client_id'], client_secret=settings.OAUTH['client_secret']
            )
        except (MismatchingStateError, MissingTokenError):
            return oauth_error_page(request)

        if 'profile' not in token:
            return HttpResponseBadRequest('No `profile` key returned by Oauth server')

        profile_url = token['profile']

        user = authenticate(profile_url=profile_url)

        if user:
            login(request, user)
        else:
            return HttpResponseForbidden('No corresponding user')

        request.session['oauth2_nonce'] = None

        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        next_url = self.request.session.get('login_next_url', None)

        if next_url and is_safe_url(next_url):
            return next_url

        return self.default_url


class LogOffView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return f"{settings.OAUTH['logoff_url']}?next=/"

    def get(self, request, *args, **kwargs):
        logger.debug(
            'User logging off: Backend: %s, session: %s',
            request.session.get(BACKEND_SESSION_KEY, None),
            request.session.get(SESSION_KEY, None)
        )

        logout(request)
        return super().get(request, *args, **kwargs)