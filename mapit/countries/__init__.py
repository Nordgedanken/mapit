from django.conf import settings

if settings.MAPIT_COUNTRY == 'DE':
    from mapit_de.countries import *  # noqa