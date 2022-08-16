#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()

with open('dev-requirements.txt') as dev_requirements_file:
    tests_require = [r.strip() for r in dev_requirements_file.readlines()]

setup(
    name="related",
    version='0.7.3',
    url="https://github.com/genomoncology/related",

    package_dir={
        '': 'src'
    },

    packages=[
        "related",
    ],

    include_package_data=True,

    install_requires=[
        "attrs>=19.3.0",
        "PyYAML",
        "future",
        "singledispatch;python_version<'3.4'",
        "python-dateutil",
    ],

    setup_requires=[
        'pytest-runner',
    ],

    extras_require={
        'toml': ['toml'],
    },

    tests_require=tests_require,

    license="MIT license",

    keywords='related object models yaml json dict nested',
    description="Related: Straightforward nested object models in Python",
    long_description="%s\n\n%s" % (readme, history),
    long_description_content_type="text/markdown",

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
