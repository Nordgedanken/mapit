# Create boundaries in MapIt for GErmany.  You need the complete shapefile from
#
#   https://osm.wno-edv-service.de/boundaries/
#
# Example usage:
#
#   ./manage.py mapit_de_import_osm mapit_de/data/Germany.shp
#

import os
import re
import sys

from collections import namedtuple

from django.core.management import call_command
from django.core.management.base import BaseCommand

from mapit.models import Generation, NameType, Country


class Command(BaseCommand):
    """Import South African boundaries"""

    help = 'Import shapefile German boundary data'

    def add_arguments(self, parser):
        parser.add_argument('--import', '-i', help="The shapefile")
    #    parser.add_argument('--districts', '-d', help="The district municipalities shapefile")
    #    parser.add_argument('--provinces', '-p', help="The provinces shapefile")
    #    parser.add_argument('--locals', '-l', help="The local municipalities shapefile")
    #    parser.add_argument('--commit', action='store_true', dest='commit', help='Actually update the database')

    def handle(self, **options):

        stop = False
        for k in ('import'):
            if options[k]:
                if not os.path.exists(options[k]):
                    print >> sys.stderr, "The file %s didn't exist" % (options[k],)
                    stop = True
            else:
                print >> sys.stderr, "You must specify --" + re.sub(r'_', '-', k)
                stop = True
        if stop:
            sys.exit(1)

        new_generation = Generation.objects.new()
        if not new_generation:
            raise Exception("There's no inactive generation for the import")

        country = Country.objects.get(code='DE')

        name_type = NameType.objects.get(code='binfo')

        BoundaryType = namedtuple('BoundaryType',
                                  ['shapefile',
                                   'area_type_code',
                                   'code_field',
                                   'code_type_code',
                                   'name_field',
                                   'name_suffix_field'])

        boundary_types = [BoundaryType(shapefile=options['binfo'],
                                       area_type_code='O01',
                                       code_field='ADMIN_LEVE',
                                       code_type_code='osm_rel',
                                       name_field='NAME',
                                       name_suffix_field='')

        for b in boundary_types:
            all_options = standard_options.copy()
            all_options.update({'generation_id': new_generation.id,
                                'area_type_code': b.area_type_code,
                                'name_type_code': name_type.code,
                                'country_code': country.code,
                                'code_field': b.code_field,
                                'code_type': b.code_type_code,
                                'name_field': b.name_field,
                                'name_suffix_field': b.name_suffix_field,
                                'new': False,
                                'use_code_as_id': False,
                                'encoding': 'UTF-8'})
            call_command('mapit_import',
                         b.shapefile,
                         **all_options)
