# Author: Ahmed Husam Elsers
# Email: ahmed.elsersi@gmail.com

# This is a Python3 script to install/upgrade Atom for Linux (Fedora, Ubuntu)

# Check The Host Linux Distro (Fedora/Ubuntu)
# Check if Atom installed or Not
#   If Installed:
#       check the latest version on Atom web page
#       then compare it to installed
#           if latest > installed:
#               upgrade()
#           if latest == installed:
#               inform and exit
#   If Not Installed:
#       download()
#       install()

import os
import platform
import re
import subprocess
import sys
import urllib.request


def check_linux_distro():
    if platform.architecture()[0] == '64bit':
        if 'fedora' in (platform.platform()).lower():
            linux_distro = 'fedora'
        if 'ubuntu' in (platform.platform()).lower():
            linux_distro = 'ubuntu'
        return linux_distro
    else:
        print("Sorry, Unsupported Linux Distro.")
        sys.exit(1)


def atom_latest(atom_base_url, atom_latest_url, linux_distro):
    try:
        with urllib.request.urlopen(atom_latest_url) as atom_urlopened:
            atom_url_read = str(atom_urlopened.read())
            latest_version_num = re.search(
                r"/atom/atom/releases/tag/v([\w.]+)", atom_url_read).group(1)

        if linux_distro == 'fedora':
            rpm_link = atom_base_url + \
                re.search(r"/atom/atom/releases/download/v{0}/atom[.-]+[^\d][a-zA-Z\d_]+[.]{1}".format(
                    latest_version_num, 'rpm'), atom_url_read).group()
            return rpm_link, latest_version_num
        if linux_distro == 'ubuntu':
            deb_link = atom_base_url + \
                re.search(r"/atom/atom/releases/download/v{0}/atom[.-]+[^\d][a-zA-Z\d_]+[.]{1}".format(
                    latest_version_num, 'deb'), atom_url_read).group()
            return deb_link, latest_version_num
    except:
        print("Atom website is not reachable!!")
        print("Please Check Your Internet Connection.")
        sys.exit(1)


def atom_installed(linux_distro):
    try:
        if linux_distro == 'fedora':
            installed_status = subprocess.getstatusoutput('rpm -q atom')[0]
            if installed_status == 0:
                installed_version = re.search(
                    r"atom-([\d.]+)-\w+", subprocess.getoutput('rpm -q atom')).group(1)

        if linux_distro == 'ubuntu':
            installed_status = subprocess.getstatusoutput('dpkg -s atom')[0]
            if installed_status == 0:
                installed_version = re.search(
                    r"Version: ([\d.]+)", subprocess.getoutput('dpkg -s atom')).group(1)
        return (True, installed_version)
    except:
        return (False, '')


def get_atom_install(linux_distro, atom_link):
    if linux_distro == 'fedora':
        subprocess.run(['wget', '-c', atom_link, '-O', os.path.join('/tmp/', os.path.basename(atom_link))])
        subprocess.run(['sudo', 'dnf', 'install', os.path.join('/tmp/', os.path.basename(atom_link))])
        print("Thank You for using my Script.")

    if linux_distro == 'ubuntu':
        subprocess.run(['wget', '-c', atom_link, '-O', os.path.join('/tmp/', os.path.basename(atom_link))])
        subprocess.run(['sudo', 'dpkg', '-i', os.path.join('/tmp/', os.path.basename(atom_link))])
        print("Thank You for using my Script.")


def main():
    atom_base_url = 'https://github.com'
    atom_latest_url = 'https://github.com/atom/atom/releases/latest'

    linux_distro = check_linux_distro()
    atom_link_pkgver_latest = atom_latest(
        atom_base_url, atom_latest_url, linux_distro)
    is_atom_installed = atom_installed(linux_distro)

    if is_atom_installed[0]:
        if atom_link_pkgver_latest[1] > is_atom_installed[1]:
            get_atom_install(linux_distro, atom_link_pkgver_latest[0])
        if atom_link_pkgver_latest[1] == is_atom_installed[1]:
            print("You already have atom latest installed, Good for You.")
            print("Thank You for using my Script.")
            sys.exit(0)
    else:
        get_atom_install(linux_distro, atom_link_pkgver_latest[0])


if __name__ == '__main__':
    main()
