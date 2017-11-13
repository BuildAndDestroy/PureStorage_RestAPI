#!/usr/bin/env python
"""
flash_array.py holds all attributes needed
to run the REST API client from rest_session.py file.
"""
import prettytable
import purestorage


class FlashArray(object):
    """
    Class to compile array attributes to query requests through REST API.
    """

    def __init__(self, working_array, api_token, secure, volumes=None, initiators=None, initiator_connections=None, hgroup_connect=None, connect=None, host=None, hgroup=None, snapshot=None, pgroup=None):
        self.working_array = working_array
        self.api_token = api_token
        self.https = secure
        self.array = purestorage.FlashArray(
            self.working_array, api_token=self.api_token, verify_https=self.https)
        self.volumes = volumes or None
        self.initiators = initiators or None
        self.initiator_connections = initiator_connections or None
        self.hgroup_connect = hgroup_connect or None
        self.connect = connect or None
        self.host = host or None
        self.hgroup = hgroup or None
        self.snapshot = snapshot or None
        self.pgroup = pgroup or None

    def disconnect_from_flasharray(self):
        """Disconnect from the array, ending REST session."""
        print '[*] Disconnecting from {}'.format(self.working_array)
        self.array.invalidate_cookie()


class ListFlashArray(FlashArray):
    """
    Class inheritance to list FlashArray attributes.
    """

    def list_volumes(self):
        """List volumes that are on array."""
        print '[*] Volumes on array.'
        volumes = self.array.list_volumes()
        return volumes

    def list_initiators(self):
        """List of initiators."""
        print '[*] initiators connected to array.'
        initiators = self.array.list_hosts()
        return initiators

    def list_connected_arrays(self):
        """List of connected arrays."""
        print '[*] Arrays connected to {}'.format(self.working_array)
        connected_arrays = self.array.list_array_connections()
        return connected_arrays

    def list_initiator_connections(self):
        """List of attributes connected to a host."""
        print '[*] Host Group attribute details.'
        returned_initiator_details = []
        for host in self.initiator_connections:
            returned_initiator_details.append(
                self.array.list_host_connections(host))
        return returned_initiator_details

    def list_hgroup_connect(self):
        """List hosts with their host group."""
        print '[*] Hosts within host groups.'
        hgroups = self.array.list_hgroups()
        return hgroups


class CreateFlashArray(FlashArray):
    """
    Class inheritance to create FlashArray attributes.
    """

    def create_volume(self):
        """
        Create a volume on the array.
        Syntax: <volume name> <1TB>
        """
        print '[*] Creating Volume {}'.format(self.volumes[0])
        volume = self.volumes[0]
        volume_size = self.volumes[1]
        self.array.create_volume(volume, volume_size)
        print '[*] Volume {} at size {} is now created!'.format(volume, volume_size)


class DestroyFlashArray(FlashArray):
    """
    Class inheritance to destroy FlashArray attributes.
    """

    def destroy_volume(self):
        """Destroy a requested volume."""
        for volume in self.volumes:
            print '[*] Destroying Volume {}'.format(volume)
            self.array.destroy_volume(volume)
            print '[*] Volume {} has been destroyed!'.format(volume)


class DecorateData(object):
    """
    Format the list subparser to a table format.
    """

    def __init__(self, import_list):
        self.import_list = import_list

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