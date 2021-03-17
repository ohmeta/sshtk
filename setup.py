#!/usr/bin/env python3

from setuptools import setup


setup(
    name='sshtk',
    version="0.2.0",
    author='Zhun Shi, Jie Zhu',
    author_email='shizhun@genomics.cn, zhujie@genomics.cn',
    scripts=['bin/sshtk.py'],
    url='http://pypi.python.org/pypi/sshtk/',
    license='GPL3',
    description='ssh toolkit',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        "pexpect",
        "pyotp",
        "setuptools"],
    zip_safe=False
)
