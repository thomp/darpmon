# from distutils.core import setup
from setuptools import setup, find_packages
setup(
    name='darpmon',
    description = "Monitor LAN",    
    # versions:
    # http://semver.org/ ?
    # comply with PEP440 ?
    version = "0.1.3",
    entry_points={
        'console_scripts': [
            'darpmon=darpmon.darpmon:main',
            'dmparse=darpmon.parser.dmparse:main'
        ]
    },    
    # dependencies (project's PyPI name)
    install_requires = [],
    packages = find_packages(),
    # metadata for upload to PyPI
    author = "D Thompson",
    author_email = "darpmon-pypi.thomp@mailhero.io",
    #license = "PSF",
    #keywords = "hello world example examples",
    #url = "http://example.com/HelloWorld/",   # project home page, if any
)
