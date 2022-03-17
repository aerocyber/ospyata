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
    version='2.0.0',
    description='Python library for the open source bookmark app Osmata.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aerocyber/ospyata',
    author='aerocyber',

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='osmata, development, osmata-bindings, osmata-python-bindings, bookmarks',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.8, <4',
    install_requires=['pycryptodomex', 'validators'],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
            'sample=sample:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/aerocyber/ospyata/issues',
        'Source': 'https://github.com/aerocyber/ospyata/',
    },
)