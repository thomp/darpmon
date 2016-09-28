# from distutils.core import setup
from setuptools import setup, find_packages
setup(
    name='darpmon',
    version = "0.1",
    # dependencies (project's PyPI name)
    install_requires = [],

    packages = find_packages(),

    # distutils only?
    #py_modules=['darpmon'],

    # metadata for upload to PyPI
    author = "D Thompson",
    author_email = "darpmon-pypi.thomp@mailhero.io",
    description = "Monitor LAN",
    #license = "PSF",
    #keywords = "hello world example examples",
    #url = "http://example.com/HelloWorld/",   # project home page, if any
)
