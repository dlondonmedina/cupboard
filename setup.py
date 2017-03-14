"""Setup the module."""
from setuptools import setup

setup(
    name='cupboard',
    packages=['cupboard'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
