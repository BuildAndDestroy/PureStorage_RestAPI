#!/usr/bin/env python3.6
"""Library for rest sessions."""

import datetime
import random

import prettytable
import purestorage


class FlashArray(object):
    """QConnect through REST API and disconnect."""

    def __init__(self, working_array, api_token, secure):
        self.working_array = working_array
        self.api_token = api_token
        self.https = secure
        self.array = purestorage.FlashArray(
            self.working_array, api_token=self.api_token, verify_https=self.https)

    def this_flasharray(self):
        """An option to return the FlashArray name and version."""
        flasharray = self.array.get()
        return [flasharray]

    def disconnect_from_flasharray(self):
        """Disconnect from the array, ending REST session."""
        print(f'\n[*] Disconnecting from {self.working_array}')
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

    def __init__(self, working_array, api_token, secure, volumes=None, drives=None, alert_distro=None, initiator_connections=None, connect=None, hosts=None, hgroup_connect=None, snapshots=None, pgroup=None, api_tokens=None):
        super().__init__(working_array, api_token, secure)
        self.volumes = volumes or None
        self.drives = drives or None
        self.alert_distro = alert_distro or None
        self.initiator_connections = initiator_connections or None
        self.connect = connect or None
        self.hosts = hosts or None
        self.hgroup_connect = hgroup_connect or None
        self.snapshots = snapshots or None
        self.pgroup = pgroup or None
        self.api_tokens = api_tokens or None

    def list_flasharray_hosts(self):
        """Return hosts that are registered with the FlashArray."""
        print('\n[*] Hosts registered with this FlashArray.')
        registered_hosts = self.array.list_hosts()
        return registered_hosts

    def list_alert_distro(self):
        """List all email addresses that receive alerts."""
        print('\n[*] Recipients of alerts.')
        user_distros = self.array.list_alert_recipients()
        return user_distros

    def list_array_drives(self):
        """List all drives on the array."""
        print('\n[*] Drives on the array.')
        list_drives = self.array.list_drives()
        return list_drives

    def user_api_tokens(self):
        """Obtain users and their API tokens."""
        print('\n[*] User\'s API Tokens.')
        user_tokens = self.array.list_api_tokens()
        return user_tokens

    def list_pgroups(self):
        """Retreive a list of pgroups on array."""
        print('\n[*] Pgroups on array.')
        pgroups = self.array.list_pgroups()
        return pgroups

    def list_volumes(self):
        """List volumes that are on array."""
        print('\n[*] Volumes on array.')
        volumes = self.array.list_volumes()
        return volumes

    def list_hgroup_connect(self):
        """List of hosts within an hgroup."""
        print('\n[*] Hosts connected to host groups.')
        initiators = self.array.list_hgroup_connections()
        return initiators

    def list_connected_arrays(self):
        """List of arrays connected to this array."""
        print(f'\n[*] Arrays connected to {self.working_array}')
        connected_arrays = self.array.list_array_connections()
        return connected_arrays

    def list_initiator_connections(self):
        """List of host and volume connections."""
        print('\n[*] Host and volume connection details.')
        returned_initiator_details = []
        for host in self.initiator_connections:
            returned_initiator_details.append(
                self.array.list_host_connections(host))
        return returned_initiator_details

    def list_hgroup_connect(self):
        """List hosts with their host group."""
        print('\n[*] Hosts within host groups.')
        hgroups = self.array.list_hgroups()
        return hgroups

    def list_snapshots(self):
        """We are restricting to just snapshots. Other options availabe in the module.

        Example array.get_volume('mitch-test', snap=True)
        """
        list_of_volume_snapshots = []
        print(f'\n[*] Snapshots for {self.snapshots}')
        for volume_snapshot in self.snapshots:
            list_of_volume_snapshots.append(
                self.array.get_volume(volume_snapshot, snap=True))

        return list_of_volume_snapshots


class CreateFlashArray(FlashArray):
    """Create objects on the FlashArray."""
    def __init__(self, working_array, api_token, secure, volume=None, snapshots=None, host=None, hgroup=None):
        super().__init__(working_array, api_token, secure)
        self.volume = volume or None
        self.snapshots = snapshots or None
        self.host = host or None
        self.hgroup = hgroup or None

    def create_volume(self):
        """Create a volume on the array.

        Syntax: <volume name> <1TB>
        """
        print(f'\n[*] Creating Volume {self.volume[0]}')
        volume = self.volume[0]
        volume_size = self.volume[1]
        self.array.create_volume(volume, volume_size)
        print(f'\n[*] Volume {volume} at size {volume_size} is now created!')

    def create_snapshots(self):
        """Create a snapshot for given volumes, snapshot names will be unique."""
        for volume_name in self.snapshots:
            print(f'\n[*] Creating snapshot for {volume_name}')
            date_time_now = datetime.datetime.now()
            todays_data_time = date_time_now.strftime("%d-%m-%Y-%H-%M-%S")
            suffix = '{}-{}'.format(todays_data_time,
                                    str(random.random()).replace('.', '-'))
            self.array.create_snapshot(volume_name, suffix=suffix)
            print(f'\n[*] Snapshot {volume_name}.{suffix} created!')

    def create_host(self):
        """Coming Soon."""
        print('Coming Soon!')

    def create_hgroup(self):
        """Coming Soon."""
        print('Coming Soon!')

class DestroyFlashArray(FlashArray):
    """docstring for ClassName"""
    def __init__(self, working_array, api_token, secure, volumes=None, pgroups=None):
        super().__init__(working_array, api_token, secure)
        self.volumes = volumes or None
        self.pgroups = pgroups or None

    def destroy_volumes(self):
        """Return a list of destroyed volumes from dictionary output."""
        destroyed_volumes_list = []
        for volume in self.volumes:
            print(f'\n[*] Destroying Volume {volume}.')
            destroyed_volume = self.array.destroy_volume(volume)
            destroyed_volumes_list.append(destroyed_volume)
        return destroyed_volumes_list


    def destroy_pgroups(self):
        """"""
        print('\nComing Soon!')


def decorate_single_list(import_list):
    """Import a single list of dictionaries and decorate."""
    unique_list = []

    for dictionaries in import_list:
        for key, value in dictionaries.items():
            if key not in unique_list:
                unique_list.append(key)

    header = prettytable.PrettyTable(unique_list)
    for dictionary in import_list:
        header.add_row(dictionary.values())

    print(header)


def decorate_multiple_lists(import_lists):
    """Import a list of lists, that are dictionaries, and decorate."""
    unique_list = []

    for lists in import_lists:
        for dictionaries in lists:
            for key, value in dictionaries.items():
                if key not in unique_list:
                    unique_list.append(key)

    header = prettytable.PrettyTable(unique_list)

    for lists in import_lists:
        for dictionary in lists:
            header.add_row(dictionary.values())

    print(header)
