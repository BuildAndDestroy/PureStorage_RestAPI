#!/usr/bin/env python3.6
"""REST API client for hosts connecting to Pure Storage Flash Arrays.
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

import purestorage_rest_api.flasharray_library as flasharray_library


def parse_arguments():
    """Pass user arguments to main.

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
        '--drives', action='store_true', help='List drives on the array.')
    list_parser.add_argument('--alert_distro', action='store_true',
                             help='Print a list of distros that receive alerts.')
    list_parser.add_argument('--initiator_connections',
                             nargs='*', help='Parse host names to see volume connections.')
    list_parser.add_argument(
        '--hgroup_connect', action='store_true', help='List hosts within host groups.')
    list_parser.add_argument(
        '--connect', action='store_true', help='List connected arrays.')
    list_parser.add_argument(
        '--hosts', action='store_true', help='List all hosts registered.')
    list_parser.add_argument('--snapshots', nargs='*',
                             help='List snapshots for all requested volumes.')
    list_parser.add_argument('--pgroups', action='store_true',
                             help='Print pgroups stored on the FlashArray.')
    list_parser.add_argument(
        '--api_tokens', action='store_true', help='List all user\'s api tokens.')

    create_parser = subparsers.add_parser(
        'create', help='Create an option on the array.')
    create_parser.add_argument(
        '--volume', nargs=2, help='Create Volume syntax: <volume_name> <1TB>')
    create_parser.add_argument(
        '--snapshots', nargs='*', help='Create snapshots, provide volume names.')
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
        'destroy', help='Destroy an option on the array.\n!!### ~WARNING DATA LOSS~ ###!!')
    destroy_parser.add_argument(
        '--volumes', nargs='*', help='Name of volumes and/or volume-snapshots to be destroyed.')
    destroy_parser.add_argument(
        '--pgroups', nargs='*', help='Name of pgroups to be destroyed.')

    args = parser.parse_args()

    return args


def main():
    """Pull from one subparser; list, create, disconnect, and destroy.

    Then execute on subparser's argument's to administer a Pure Storage FlashArray.
    """
    args = parse_arguments()

    print(f'[*] Connecting to {args.working_array}')

    if args.command == 'list':
        array = flasharray_library.ListFlashArray(args.working_array, args.api_token, args.secure, args.volumes, args.drives, args.alert_distro,
                                                  args.initiator_connections, args.connect, args.hosts, args.hgroup_connect, args.snapshots, args.pgroups, args.api_tokens)

        if array.volumes:
            flasharray_library.decorate_single_list(array.list_volumes())
        if array.drives:
            flasharray_library.decorate_single_list(array.list_array_drives())
        if array.alert_distro:
            flasharray_library.decorate_single_list(array.list_alert_distro())
        if array.initiator_connections:
            flasharray_library.decorate_multiple_lists(
                array.list_initiator_connections())
        if array.connect:
            flasharray_library.decorate_single_list(
                array.list_connected_arrays())
        if array.hosts:
            flasharray_library.decorate_single_list(
                array.list_flasharray_hosts())
        if array.hgroup_connect:
            flasharray_library.decorate_single_list(
                array.list_hgroup_connect())
        if args.snapshots:
            flasharray_library.decorate_multiple_lists(array.list_snapshots())
        if args.pgroups:
            flasharray_library.decorate_single_list(array.list_pgroups())
        if args.api_tokens:
            flasharray_library.decorate_single_list(array.user_api_tokens())

    if args.command == 'create':
        array = flasharray_library.CreateFlashArray(
            args.working_array, args.api_token, args.secure, args.volume, args.snapshots, args.host, args.hgroup)
        if args.volume:
            array.create_volume()
        if args.snapshots:
            array.create_snapshots()
        if args.host:
            flasharray_library.create_host()
        if args.hgroup:
            flasharray_library.create_hgroup()

    if args.command == 'disconnect':
        # array = flasharray_library.FlashArray(
        #     args.working_array, args.api_token, args.secure, args.host, args.array, args.hgroup)
        print('Coming Soon!')

    if args.command == 'destroy':
        array = flasharray_library.DestroyFlashArray(
            args.working_array, args.api_token, args.secure, args.volumes, args.pgroups)
        if args.volumes:
            flasharray_library.decorate_single_list(array.destroy_volumes())
        if args.pgroups:
            print('Coming Soon!')

    array.disconnect_from_flasharray()


if __name__ == '__main__':
    main()
