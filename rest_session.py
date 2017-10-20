#!/usr/bin/env python
"""
    REST API client for hosts connecting to Pure Storage Flash Arrays.
    Copyright (C) 2017  Mitch O'Donnell devreap1@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import argparse

import prettytable
import purestorage


class FlashArray(object):
    """Class to compile array requests through REST API."""

    def __init__(self, host, api_token, secure, volumes, initiators, initiator_connections, hgroup_connect, connect):
        self.host = host
        self.api_token = api_token
        self.https = secure
        self.array = purestorage.FlashArray(
            self.host, api_token=self.api_token, verify_https=self.https)
        self.volumes = volumes
        self.initiators = initiators
        self.initiator_connections = initiator_connections
        self.hgroup_connect = hgroup_connect
        self.connect = connect

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
        print '[*] Arrays connected to {}'.format(self.host)
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

    def disconnect_from_flasharray(self):
        """Disconnect from the array."""
        print '[*] Disconnecting from {}'.format(self.host)
        self.array.invalidate_cookie()


class DecorateData(object):
    """Format the list subparser to a table format."""

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
        """Format initiators in to table format."""
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


def parse_arguments():
    """Pass user arguments to main."""
    knowledge_articles = 'rest_session.py Copyright (C) 2017  Mitch O\'Donnell\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions.'
    pypi_purestorage = 'https://pythonhosted.org/purestorage/quick_start.html'
    epilog = '{}\n\nPure Storage PyPi Documentation: \n{}'.format(
        knowledge_articles, pypi_purestorage)

    parser = argparse.ArgumentParser(
        description=__doc__, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('host', help='subdomain.domain.com or <ip address>.')
    parser.add_argument('api_token', help='API token generated for user.')
    parser.add_argument('-s', '--secure', action='store_true',
                        help='Enable HTTPS to the array, use only if HTTPS is configured.')

    subparsers = parser.add_subparsers(help='commands')

    list_parser = subparsers.add_parser('list', help='List contents.')
    list_parser.add_argument(
        '--volumes', action='store_true', help='List volumes on array.')
    list_parser.add_argument(
        '--initiators', action='store_true', help='List hosts connected to the array.')
    list_parser.add_argument('--initiator_connections',
                             nargs='+', help='List connection host argument.')
    list_parser.add_argument(
        '--hgroup_connect', action='store_true', help='List host group connections.')
    list_parser.add_argument(
        '--connect', action='store_true', help='List connected arrays.')

    # create_parser = subparsers.add_parser(
    #     'create', help='Create an option on the array.')
    # create_parser.add_argument(
    #     '--volumes', nargs='+', help='Add hostnames, multiple names supported.')
    # create_parser.add_argument(
    #     '--snapshot', nargs='+', help='Add snapshot, multiple names will create a pgroup.')
    # create_parser.add_argument(
    #     '--host', nargs='+', help='<hostname> and <wwn\'s or iqn\'s>.')
    # create_parser.add_argument(
    #     '--hgroup', nargs='+', help='<host group name> and <host names>.')

    # disconnect_parser = subparsers.add_parser(
    #     'disconnect', help='Disconnect options on the array.')
    # disconnect_parser.add_argument(
    #     '--host', nargs='+', help='Disconnect <host name> from <volume name>.')
    # disconnect_parser.add_argument('--array')
    # disconnect_parser.add_argument('--hgroup')

    # destroy_parser = subparsers.add_parser(
    #     'destroy', help='Destroy an option on the array.')
    # destroy_parser.add_argument(
    #     '--volume', nargs='+', help='Destroy <volume name>.')

    args = parser.parse_args()
    return args


def main():
    """
    Run a check on the array with user's API token.
    """
    args = parse_arguments()

    print '[*] Connecting to {}'.format(args.host)
    array = FlashArray(args.host, args.api_token, args.secure, args.volumes,
                       args.initiators, args.initiator_connections, args.hgroup_connect, args.connect)

    """Parse the list subparser arguments."""
    if args.volumes:
        decorated = DecorateData(array.list_volumes())
        decorated.decorate_volumes()
    if args.initiators:
        decorated = DecorateData(array.list_initiators())
        decorated.decorated_initiators()
    if args.initiator_connections:
        decorated = DecorateData(array.list_initiator_connections())
        decorated.decorate_initiator_connections()
    if args.hgroup_connect:
        decorated = DecorateData(array.list_hgroup_connect())
        decorated.decorated_hgroups()
    if args.connect:
        decorated = DecorateData(array.list_connected_arrays())
        decorated.decorated_connected_arrays()

    array.disconnect_from_flasharray()


if __name__ == '__main__':
    main()
