PureStorage_RestAPI

Required modules:

  prettytable
  purestorage

  Install via Linux:
  Clone this repo or download ZIP under /opt/ (should look like /opt/PureStorage_RestAPI/) and run in the PureStorage_RestAPI directory:
    sudo pip install .
  Upgrading will need to be ran in the same directory as setup.py, run:
    sudo pip install --upgrade .

Work in progress. 
"List" is the only fully functioning subparser. Create, Disconnect, and Destroy options will be added for hosts, volumes, and protection groups.

"Create" a volume and "Destroy" a volume subparser is now up and running.


Help Menu

usage: rest_api [-h] [-s]
                       working_array api_token
                       {list,create,disconnect,destroy} ...

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

positional arguments:
  working_array         subdomain.domain.com or <ip address>.
  api_token             API token generated for user.
  {list,create,disconnect,destroy}
                        commands
    list                List contents.
    create              Create an option on the array.
    disconnect          Disconnect options on the array.
    destroy             Destroy an option on the array.

optional arguments:
  -h, --help            show this help message and exit
  -s, --secure          Enable HTTPS to the array, use only if HTTPS is configured.

rest_api Copyright (C) 2017  Mitch O'Donnell
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.

Pure Storage PyPi Documentation: 
https://pythonhosted.org/purestorage/quick_start.html
