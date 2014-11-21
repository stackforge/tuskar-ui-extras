# -*- coding: utf8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import horizon.messages
import json
import logging
import requests
import urllib

from collections import namedtuple
from django.conf import settings
from horizon import tabs
from requests_oauthlib import OAuth1
from six import string_types
from tuskar_ui import api
from tuskar_ui.infrastructure.nodes import tabs as nodes_tabs

from .tables import ErrataTable

SAT_CONF_KEYS = ['compute-1::ExtraConfig', 'Satellite']
SAT_HOST_PARAM = 'SatelliteHost'
SAT_AUTH_PARAM = 'SatelliteAuth'
SAT_ORG_PARAM = 'SatelliteOrg'

LOG = logging.getLogger('tuskar_sat_ui')
ErrataItem = namedtuple('ErrataItem', ['title', 'type', 'id', 'issued'])


class DetailOverviewTab(nodes_tabs.DetailOverviewTab):
    template_name = 'infrastructure/nodes/_detail_overview_sat.html'

    def get_context_data(self, request):
        result = super(DetailOverviewTab, self).get_context_data(request)
        if result['node'].uuid is None:
            return result

        # Find the stack
        try:
            plan = api.tuskar.Plan.get_the_plan(request)
            stack = api.heat.Stack.get_by_plan(self.request, plan)
        except Exception as e:
            LOG.exception(e)
            horizon.messages.error(request,
                                   _("Could not retrieve errata."))
            return result

        if stack is None:
            return result

        config = stack.parameters

        # Find the Satellite configuration data.
        # The configuration data is store in Heat as parameters.
        # They may be stored directly as Heat parameters,
        # or in a the JSON structure stored in ExtraConfig.
        for key in SAT_CONF_KEYS:
            if key in config:
                config = config[key]
            if key.endswith('ExtraConfig'):
                # It's stored in ExtraConfig. ExtraConfig is a JSON structure.
                # Un-JSON it.
                config = json.loads(config)

        for param in [SAT_HOST_PARAM, SAT_AUTH_PARAM, SAT_ORG_PARAM]:
            if param not in config:
                horizon.messages.error(request,
                                       _("No Satellite configuration found."))
                return result

        host = config[SAT_HOST_PARAM]
        auth = config[SAT_AUTH_PARAM].split(':')
        organization = config[SAT_ORG_PARAM]

        if auth[0] == 'oauth':
            auth = OAuth1(auth[1], auth[2])
        elif auth[0] == 'basic':
            auth = auth[1], auth[2]
        else:
            horizon.messages.error(
                request,
                _(('Satellite configuration error, '
                  'unknown authentication "%s".') % auth[0]))

        addresses = result['node'].addresses
        #addresses = ['"52:54:00:4F:D8:65"']  # Use for debugging

        # Get the errata here
        host = host.strip('/')  # Get rid of any trailing slash in the host url
        verify = not getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)

        # Pick up the UUID from the MAC address This makes no sense, as we
        # need both MAC address and the interface, and we don't have the
        # interface, so we need to make multiple slow searches. If the
        # Satellite UUID isn't the same as this one, and it probably isn't we
        # need to store a mapping somewhere.
        url = '{host}/katello/api/v2/systems'.format(host=host)
        uuid = None
        for mac in addresses:
            for interface in ['eth0', 'eth1', 'en0', 'en1']:

                q = 'facts.net.interface.{iface}.mac_address:{mac}'.format(
                    iface=interface, mac=mac)
                params = {'search': q, 'organization_id': organization}
                r = requests.get(url, params=params, auth=auth, verify=verify)
                r.raise_for_status()  # Raise an error if the request failed
                results = r.json()['results']
                if results:
                    uuid = results[0]['uuid']
                    break

        if uuid is None:
            # No node found
            result['errata'] = None
            return result

        errata_url = '{host}/katello/api/v2/systems/{id}/errata'
        r = requests.get(errata_url.format(host=host, id=uuid),
                         auth=auth,
                         verify=verify)
        r.raise_for_status()  # Raise an error if the request failed
        errata = r.json()['results']
        if not errata:
            result['errata'] = None
        else:
            data = [ErrataItem(x['title'], x['type'], x['id'], x['issued'])
                    for x in errata]
            result['errata'] = ErrataTable(request, data=data)
        return result


class NodeDetailTabs(tabs.TabGroup):
    slug = "node_details"
    tabs = (DetailOverviewTab,)
