"""setup.py"""
from setuptools import setup, find_packages

__version__ = "1.1.2.1"
__author__ = "plusls<plusls@qq.com>"
__name__ = "uestc"
__doc__ = "一个和电子科大有关的模块"

setup(author=__author__,
      author_email='plusls@qq.com',
      maintainer=__author__,
      name=__name__,
      packages=find_packages(exclude=('test', 'test.*')),
      long_description=open('README.rst', encoding='utf-8').read(),
      version=__version__,
      keywords='uestc catch course login',
      description=__doc__,
      url="https://github.com/plusIs/uestc",
      install_requires=['bs4>=0.0.1',
                        'requests>=2.17'],
      classifiers=[
          'Environment :: Console',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],)
