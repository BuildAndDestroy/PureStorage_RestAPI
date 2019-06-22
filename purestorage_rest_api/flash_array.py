#!/usr/bin/env python
"""
flash_array.py holds all attributes needed
to run the REST API client from rest_session.py file.
"""
import datetime
import random
import prettytable
import purestorage


class FlashArray(object):
    """
    Class to compile array attributes to query requests through REST API.
    """

    def __init__(self, working_array, api_token, secure, volumes=None, drives=None, alert_distro=None, initiators=None, initiator_connections=None, hgroup_connect=None, connect=None, host=None, hgroup=None, snapshot=None, pgroup=None, api_tokens=None):
        self.working_array = working_array
        self.api_token = api_token
        self.https = secure
        self.array = purestorage.FlashArray(
            self.working_array, api_token=self.api_token, verify_https=self.https)
        self.volumes = volumes or None
        self.drives = drives or None
        self.alert_distro = alert_distro or None
        self.initiators = initiators or None
        self.initiator_connections = initiator_connections or None
        self.hgroup_connect = hgroup_connect or None
        self.connect = connect or None
        self.host = host or None
        self.hgroup = hgroup or None
        self.snapshot = snapshot or None
        self.pgroup = pgroup or None
        self.api_tokens = api_tokens or None

    def disconnect_from_flasharray(self):
        """Disconnect from the array, ending REST session."""
        print '\n[*] Disconnecting from {}'.format(self.working_array)
        self.array.invalidate_cookie()


class ListFlashArray(FlashArray):
    """
    Class inheritance to list FlashArray attributes.
    """
    """
    list_hardware()
    list_hgroups()
    list_messages()
    list_network_interfaces()
    list_pgroups()
    list_ports()
    list_publickeys()
    list_snmp_managers()
    list_subnets()
    list_volume_block_differences()
    list_volume_private_connections()
    list_volume_shared_connections()
    """

    def list_alert_distro(self):
        """List all recipients for alerting."""
        print '\n[*] Recipients of alerts.'
        user_distros = self.array.list_alert_recipients()
        return user_distros

    def list_array_drives(self):
        """List all drives on the array."""
        print '\n[*] Drives on the array.'
        list_drives = self.array.list_drives()
        return list_drives

    def user_api_tokens(self):
        """Obtain users and their API tokens."""
        print '\n[*] User\'s API Tokens.'
        user_tokens = self.array.list_api_tokens()
        return user_tokens

    def list_volumes(self):
        """List volumes that are on array."""
        print '\n[*] Volumes on array.'
        volumes = self.array.list_volumes()
        return volumes

    def list_initiators(self):
        """List of initiators."""
        print '\n[*] Initiators connected to array.'
        initiators = self.array.list_hosts()
        return initiators

    def list_connected_arrays(self):
        """List of connected arrays."""
        print '\n[*] Arrays connected to {}'.format(self.working_array)
        connected_arrays = self.array.list_array_connections()
        return connected_arrays

    def list_initiator_connections(self):
        """List of attributes connected to a host."""
        print '\n[*] Host Group attribute details.'
        returned_initiator_details = []
        for host in self.initiator_connections:
            returned_initiator_details.append(
                self.array.list_host_connections(host))
        return returned_initiator_details

    def list_hgroup_connect(self):
        """List hosts with their host group."""
        print '\n[*] Hosts within host groups.'
        hgroups = self.array.list_hgroups()
        return hgroups


class CreateFlashArray(FlashArray):
    """Class inheritance to create FlashArray attributes."""

    def create_volume(self):
        """Create a volume on the array.

        Syntax: <volume name> <1TB>
        """
        print '\n[*] Creating Volume {}'.format(self.volumes[0])
        volume = self.volumes[0]
        volume_size = self.volumes[1]
        self.array.create_volume(volume, volume_size)
        print '\n[*] Volume {} at size {} is now created!'.format(
            volume, volume_size)

    def create_snapshot(self):
        """"""
        print '\n[*] Creating snapshot for {}'.format(self.volumes[0])
        date_time_now =  datetime.datetime.now()
        todays_data_time = date_time_now.strftime("%d-%m-%Y-%H-%M-%S")
        suffix = '{}-{}'.format(todays_data_time, str(random.random()).replace('.','-'))
        self.array.create_snapshot(self.volumes[0], suffix=suffix)
        print '\n[*] Snapshot {}.{} created!'.format(self.volumes[0], suffix)

class DestroyFlashArray(FlashArray):
    """
    Class inheritance to destroy FlashArray attributes.
    """

    def destroy_volume(self):
        """Destroy a requested volume."""
        for volume in self.volumes:
            print '\n[*] Destroying Volume {}'.format(volume)
            self.array.destroy_volume(volume)
            print '\n[*] Volume {} has been destroyed!'.format(volume)


class DecorateData(object):
    """
    Format the list subparser to a table format.
    """

    def __init__(self, import_list):
        self.import_list = import_list

    def decorate_alert_recipients(self):
        """Format list_alert_recipients into a table."""
        table = prettytable.PrettyTable(['Enabled', 'Name'])
        for dictionary in self.import_list:
            table.add_row([dictionary['enabled'], dictionary['name']])
        print table

    def decorate_user_api_tokens(self):
        """Format user api tokens into a table."""
        table = prettytable.PrettyTable(['API Token', 'Name', 'Created'])
        for dictionary in self.import_list:
            table.add_row([dictionary['api_token'],
                           dictionary['name'], dictionary['created']])
        print table

    def decorate_list_drives(self):
        """Format drives into a table."""
        table = prettytable.PrettyTable(['Capacity',
                                         'Details',
                                         'Last_evac_completed',
                                         'Last_failure',
                                         'Name',
                                         'Status',
                                         'Type'])
        for dictionary in self.import_list:
            table.add_row([dictionary['capacity'],
                           dictionary['details'],
                           dictionary['last_evac_completed'],
                           dictionary['last_failure'],
                           dictionary['name'],
                           dictionary['status'],
                           dictionary['type']])
        print table

    def decorate_volumes(self):
        """Format volumes into table format."""
        header = prettytable.PrettyTable(
            ['Source', 'Serial', 'Size', 'Name', 'Created'])
        for dictionary in self.import_list:
            header.add_row(
                [dictionary['source'],
                 dictionary['serial'],
                 dictionary['size'],
                 dictionary['name'],
                 dictionary['created']])
        print header

    def decorated_initiators(self):
        """Format initiators into table format."""
        header = prettytable.PrettyTable(['IQN', 'WWN', 'Name', 'HGroup'])
        for dictionary in self.import_list:
            header.add_row(
                [dictionary['iqn'],
                 dictionary['wwn'],
                 dictionary['name'],
                 dictionary['hgroup']])
        print header

    def decorate_initiator_connections(self):
        """Format initiator_connections into table format."""
        header = prettytable.PrettyTable(
            ['Host Group', 'LUN', 'Name', 'Volume'])
        for entry in self.import_list:
            for dictionary in entry:
                header.add_row([
                    dictionary['hgroup'],
                    dictionary['lun'],
                    dictionary['name'],
                    dictionary['vol']
                ])
        print header

    def decorated_connected_arrays(self):
        """Format connected_arrays into table format."""
        header = prettytable.PrettyTable(
            ['Array Name',
             'Connected',
             'ID',
             'Management Address',
             'Replication Address',
             'Throttled',
             'Type',
             'Version'])
        for dictionary in self.import_list:
            header.add_row([
                dictionary['array_name'],
                dictionary['connected'],
                dictionary['id'],
                dictionary['management_address'],
                dictionary['replication_address'],
                dictionary['throttled'],
                dictionary['type'],
                dictionary['version']
            ])
        print header

    def decorated_hgroups(self):
        """Format hgroups into table format."""
        header = prettytable.PrettyTable(['Name', 'Hosts'])
        for dictionary in self.import_list:
            header.add_row([
                dictionary['name'],
                dictionary['hosts']
            ])
        print header
