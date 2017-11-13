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

import purestorage_rest_api.flash_array as flash_array


def parse_arguments():
    """
    Pass user arguments to main.
    Subparser arguments are dependant on the root subparser invoked.
    """
    knowledge_articles = 'rest_session.py Copyright (C) 2017  Mitch O\'Donnell\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions.'
    pypi_purestorage = 'https://pythonhosted.org/purestorage/quick_start.html'
    epilog = '{}\n\nPure Storage PyPi Documentation: \n{}'.format(
        knowledge_articles, pypi_purestorage)

    parser = argparse.ArgumentParser(
        description=__doc__, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        'working_array', help='subdomain.domain.com or <ip address>.')
    parser.add_argument('api_token', help='API token generated for user.')
    parser.add_argument('-s', '--secure', action='store_true',
                        help='Enable HTTPS to the array, use only if HTTPS is configured.')

    subparsers = parser.add_subparsers(help='commands', dest='command')

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

    create_parser = subparsers.add_parser(
        'create', help='Create an option on the array.')
    create_parser.add_argument(
        '--volume', nargs=2, help='Create Volume syntax: <volume_name> <1TB>')
    create_parser.add_argument(
        '--snapshot', nargs='+', help='Add snapshot, multiple names will create a pgroup.')
    create_parser.add_argument(
        '--host', nargs='+', help='<hostname> and <wwn\'s or iqn\'s>.')
    create_parser.add_argument(
        '--hgroup', nargs='+', help='<host group name> and <host names>.')

    disconnect_parser = subparsers.add_parser(
        'disconnect', help='Disconnect options on the array.')
    disconnect_parser.add_argument(
        '--host', nargs='+', help='Disconnect <host name> from <volume name>.')
    disconnect_parser.add_argument(
        '--array', nargs='+', help='DNS name or IP address of other array.')
    disconnect_parser.add_argument(
        '--hgroup', nargs='+', help='Delete a shared connection between a host group and a volume.')

    destroy_parser = subparsers.add_parser(
        'destroy', help='Destroy an option on the array.')
    destroy_parser.add_argument(
        '--volume', nargs='*', help='Destroy volumes passed as arguments.')
    destroy_parser.add_argument(
        '--pgroup', nargs='+', help='Name of pgroup to be destroyed.')

    args = parser.parse_args()

    return args

def main():
    """
    Pull from one subparser; list, create, disconnect, and destroy.
    Then execute on subparser's argument's.
    """
    args = parse_arguments()

    print '[*] Connecting to {}'.format(args.working_array)

    if args.command == 'list':
        array = flash_array.ListFlashArray(args.working_array, args.api_token, args.secure, args.volumes,
                                           args.initiators, args.initiator_connections, args.hgroup_connect, args.connect)
        if array.volumes:
            decorated = flash_array.DecorateData(array.list_volumes())
            decorated.decorate_volumes()
        if array.initiators:
            decorated = flash_array.DecorateData(array.list_initiators())
            decorated.decorated_initiators()
        if array.initiator_connections:
            decorated = flash_array.DecorateData(
                array.list_initiator_connections())
            decorated.decorate_initiator_connections()
        if array.hgroup_connect:
            decorated = flash_array.DecorateData(array.list_hgroup_connect())
            decorated.decorated_hgroups()
        if array.connect:
            decorated = flash_array.DecorateData(array.list_connected_arrays())
            decorated.decorated_connected_arrays()

    if args.command == 'create':
        array = flash_array.CreateFlashArray(
            args.working_array, args.api_token, args.secure, args.volume, args.snapshot, args.host, args.hgroup)
        if args.volume:
            array.create_volume()

    if args.command == 'disconnect':
        array = flash_array.FlashArray(
            args.working_array, args.api_token, args.secure, args.host, args.array, args.hgroup)

    if args.command == 'destroy':
        array = flash_array.DestroyFlashArray(
            args.working_array, args.api_token, args.secure, args.volume, args.pgroup)
        if args.volume:
            array.destroy_volume()

    array.disconnect_from_flasharray()


if __name__ == '__main__':
    main()
