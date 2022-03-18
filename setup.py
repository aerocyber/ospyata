# Copyright (c) 2022 aerocyber
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""A setuptools based setup module for ospyata, the Python bindings for Osmata.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='ospyata',
    license="MIT License",
    version='2.0.2',
    description='Python library for the open source bookmark app Osmata.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aerocyber/ospyata',
    author='aerocyber',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='osmata, development, osmata-bindings, osmata-python-bindings, bookmarks',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.9, <4',
    install_requires=['validators'],
    project_urls={
        'Bug Reports': 'https://github.com/aerocyber/ospyata/issues',
        'Source': 'https://github.com/aerocyber/ospyata/',
    },
)
