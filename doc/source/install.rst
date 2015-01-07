Installation instructions
=========================

Go into your Horizon directory::

    cd horizon/

Install Tuskar UI Extras with all dependencies in your virtual environment::

    tools/with_venv.sh pip install -r ../tuskar-ui-extras/requirements.txt
    tools/with_venv.sh pip install -e ../tuskar-ui-extras/


Enabling Tuskar-UI Boxes
------------------------

To enable the Tuskar-UI Boxes plugin in Horizon, copy the config file:.

    cp ../tuskar-ui-extras/_60_tuskar_boxes.py.example openstack_dashboard/local/enabled/_60_tuskar_boxes.py


Enabling Tuskar Satellite Integration
-------------------------------------

To enable the Tuskar-SAT6 UI plugin in Horizon, copy the config file:.

    cp ../tuskar-ui-extras/_60_tuskar_sat_ui.py.example openstack_dashboard/local/enabled/_60_tuskar_sat_ui.py


Setting up the Satellite integration
------------------------------------

You need to configure the connection to Satellite for the Satellite integration
to work. This can be done in two ways. Either by adding parameters to the Heat
Template, or by adding the parameters in the "ExtraConfig" configuration field.

There parameter is called `Satellite`, and contains the following subkeys:

 * SatelliteHost: The URL to the Satellite server, f.ex 'http://example.com/'
 * SatelliteOrg: The name of the organistion you want to use, f ex 'ACME'
 * SatelliteAuth: A string containing authentication information.

When adding the configuration information to the ExtraConfig field it should be
stored in JSON format. For example:

    {
        'Satellite': {
            'SatelliteHost': 'http://example.com/',
            'SatelliteAuth': 'oauth:client:7TgjxHen20ghdfo739bhGDlncHN7Ft5E',
            'SatelliteOrg': 'ACME',
    }

Authentication information
..........................

The Satellite authentication information should be in the format
'protocol:authstring'. Currently two protocols are supported, ``basic`` and
``oauth``.

For basic authentication the authstring should be the username and password,
separated by a colon. This means you can't have a colon in the username. Ex::

    basic:username:password

For OAuth the authstring should be a client key and a client secret. These are
obtained from your OAuth system. Ex::

    oauth:client:7TgjxHen20ghdfo739bhGDlncHN7Ft5E

