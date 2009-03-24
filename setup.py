"""Installs package using setuptools

Run:
    python setup.py install

to install this package.
"""

try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup

from distutils.command.install import INSTALL_SCHEMES
import sys
import sneakylang

required_python_version = '2.4'

###############################################################################
# arguments for the setup command
###############################################################################
name = "sneakylang"
version = sneakylang.__versionstr__
desc = "Extensible framework for easy creation of extensible WikiLanguages"
long_desc = """"""
classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development :: Documentation",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Text Processing",
    "Topic :: Text Processing :: Markup :: HTML",
    "Topic :: Text Processing :: Markup :: XML",
]
author="Lukas Almad Linhart"
author_email="bugs@almad.net"
url="http://projects.almad.net/sneakylang"
cp_license="BSD"
packages=[
    "sneakylang"
]
download_url="http://www.almad.net/download/sneakylang/sneakylang-"+version+".tar.gz"
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
