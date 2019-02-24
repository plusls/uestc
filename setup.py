"""setup.py"""
from setuptools import setup, find_packages
from uestc import __version__, __author__, __name__, __doc__


setup(author=__author__,
      author_email='plusls@qq.com',
      maintainer=__author__,
      name=__name__,
      packages=find_packages(exclude=('test', 'test.*')),
      long_description=open('README.rst', encoding='utf-8').read(),
      version=__version__,
      keywords='uestc catch course login',
      description=__doc__,
      url="https://github.com/plusls/uestc",
      install_requires=['bs4',
                        'requests', 'Crypto', 'pycryptodome'],
      classifiers=[
          'Environment :: Console',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],)
