"""Installs package using distutils

Run:
    python setup.py install

to install this package.
"""

###
#RPGPlanet Wiki engine: Fuel for your Wiki system
#Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/ and contributors,
# for a full list see http://projects.almad.net/rpgplanet-tools
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
###


from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES
import sys

required_python_version = '2.4'

###############################################################################
# arguments for the setup command
###############################################################################
name = "sneakylang"
version = "0.2_alpha1"
desc = "Extensible framework for easy creation of extensible WikiLanguages"
long_desc = """"""
classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development :: Documentation",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Text Processing",
    "Topic :: Text Processing :: Markup :: HTML",
    "Topic :: Text Processing :: Markup :: XML"
]
author="Lukas Almad Linhart"
author_email="bugs@almad.net"
url="http://projects.almad.net/sneakylang"
cp_license="LGPL"
packages=[
    "sneakylang"
]
download_url="http://projects.almad.net/sneakylang/wiki/Download"
data_files=[]
###############################################################################
# end arguments for setup
###############################################################################

def main():
    if sys.version < required_python_version:
        s = "I'm sorry, but %s %s requires Python %s or later."
        print s % (name, version, required_python_version)
        sys.exit(1)

    # set default location for "data_files" to platform specific "site-packages"
    # location
    for scheme in INSTALL_SCHEMES.values():
        scheme['data'] = scheme['purelib']

    setup(
        name=name,
        version=version,
        description=desc,
        long_description=long_desc,
        classifiers=classifiers,
        author=author,
        author_email=author_email,
        url=url,
        license=cp_license,
        packages=packages,
        download_url=download_url,
        data_files=data_files,
    )

if __name__ == "__main__":
    main()
