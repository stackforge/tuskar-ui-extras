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

import json

from tuskar_ui.test import helpers

from tuskar_sat_ui.nodes import tabs


class SatTests(helpers.BaseAdminViewTests):
    def test_satellite_config_direct(self):
        config = json.dumps({
            'Satellite': {
                'SatelliteHost': 'http://example.com/',
                'SatelliteAuth': 'basic:user:pass',
                'SatelliteOrg': 'ACME',
            },
        })
        host, auth, org = tabs._get_satellite_config(config)
        self.assertEqual(host, 'http://example.com')
        self.assertEqual(auth, ('user', 'pass'))
        self.assertEqual(org, 'ACME')

    def test_satellite_config_extra1(self):
        config = json.dumps({
            'compute-1::ExtraConfig': {
                'Satellite': json.dumps({
                    'SatelliteHost': 'http://example.com/',
                    'SatelliteAuth': 'basic:user:pass',
                    'SatelliteOrg': 'ACME',
                }),
            },
        })
        host, auth, org = tabs._get_satellite_config(config)
        self.assertEqual(host, 'http://example.com')
        self.assertEqual(auth, ('user', 'pass'))
        self.assertEqual(org, 'ACME')

    def test_satellite_config_extra2(self):
        config = json.dumps({
            'compute-1::ExtraConfig': json.dumps({
                'Satellite': {
                    'SatelliteHost': 'http://example.com/',
                    'SatelliteAuth': 'basic:user:pass',
                    'SatelliteOrg': 'ACME',
                },
            }),
        })
        host, auth, org = tabs._get_satellite_config(config)
        self.assertEqual(host, 'http://example.com')
        self.assertEqual(auth, ('user', 'pass'))
        self.assertEqual(org, 'ACME')
