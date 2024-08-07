# Welcome to CluMS
[![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)](https://mariadb.org) [![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com) [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://python.org) [![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](https://linux.org) [![Manjaro](https://img.shields.io/badge/Manjaro-35BF5C?style=for-the-badge&logo=Manjaro&logoColor=white)](https://manjaro.org) [![Visual Studio Code](https://img.shields.io/badge/Visual_Studio_Code-0078d7?style=for-the-badge)](https://code.visualstudio.com)

[![GitHub contributors](https://img.shields.io/github/contributors/Pranay-Chopra/CluMS?style=for-the-badge)](https://GitHub.com/Pranay-Chopra/CluMS/graphs/contributors/) [![Maintenance](https://img.shields.io/badge/Maintained%3F-no-red.svg?style=for-the-badge)](https://bitbucket.org/lbesson/ansi-colors) [![Maintainer](https://img.shields.io/badge/Maintainer-Pranay&minus;Chopra-blue?style=for-the-badge)](https://github.com/Pranay-Chopra)

[![Gnome](https://img.shields.io/badge/Gnome-blue?style=for-the-badge&logo=gnome&logoColor=black)](https://gnome.org) [![GTK - 3.0](https://img.shields.io/badge/GTK-3.0-green?style=for-the-badge&logo=gtk)](https://gtk.org) [![dependency - hashlib](https://img.shields.io/badge/dependency-hashlib-blue?style=for-the-badge)](https://pypi.org/project/hashlib) [![dependency - json](https://img.shields.io/badge/dependency-json-blue?style=for-the-badge)](https://pypi.org/project/json) [![dependency - gi](https://img.shields.io/badge/dependency-gi-blue?style=for-the-badge)](https://pypi.org/project/gi) [![dependency - mysql.connector](https://img.shields.io/badge/dependency-mysql.connector-blue?style=for-the-badge)](https://pypi.org/project/mysql.connector) [![Theme - Flat-Remix-XXX-Darkest](https://img.shields.io/badge/Theme-Flat--Remix--XXX--Darkest-191919?logo=gnome&style=for-the-badge)](https://github.com/daniruiz/Flat-Remix-Gtk)

CluMS (or Club Management Software) is a proprietary software developed by [FORCE-Club](https://github.com/FORCE-Fest) for managing the members, teams and events organized and contained within the club.

# Back Story
The project was initially intended as the Grade 12 CBSE Computer Science project of the club leaders [Pranay Chopra](https://github.com/Pranay-Chopra) and [Neil Virmani](https://github.com/NVirCX) for AY 2024-25. However, due to its highly practical use case and its almost flawless nature, it was quickly adopted by the club and is now in use as the Official Club Management System.

# General Information
1. The Software is built for [![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](https://linux.org) ONLY and works with [![GTK - 3.0](https://img.shields.io/badge/GTK-3.0-green?logo=gtk)](https://gtk.org) The maintainers are working on a [![Windows](https://img.shields.io/badge/Windows-0078D6?logo=windows&logoColor=white)](https://www.microsoft.com/en-us/windows) port, but so far there has been no positive progress made towards it. The UI looks good in DARK MODE ONLY, and it is recommended you use [![Theme - Flat-Remix-XXX-Darkest](https://img.shields.io/badge/Theme-Flat--Remix--XXX--Darkest-191919?logo=gnome)](https://github.com/daniruiz/Flat-Remix-Gtk)

2. The system works on password authentication. Right now, there is only one user and it is hardcoded into the system. For the future, however, the maintainers are working on a User Management System.

3. Database Structure (everything is hardcoded except Database name):
   
```
clums_db (Database) (Can be changed)  
  |  
  |-> members (Table)  
  |     |-> s_no (int)  
  |     |-> name (varchar 255)  
  |     |-> post (varchar 255)  
  |     '-> mob_no (varchar 255)
  |  
  |-> teams (Table)  
  |     |-> s_no (int)
  |     |-> team_name (varchar 255)
  |     '-> team_members (varchar 255)
  |
  '-> events (Table)
        |-> s_no (int)
        |-> name (varchar 255)
        |-> domain (varchar 255)
        |-> part_no (varchar 255)
        '-> head (varchar 255)
```

4. The Login screen allows the user to connect a MySQL database. By default, this option is disabled and the system uses JSON files to store the data. The data can be edited, added or deleted by the user.
5. The changes are committed directly to the database and the JSON files, so rolling back to a previous version is not possible. Please exercise caution while manipulating the data.
