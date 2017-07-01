'''setup.py'''
from setuptools import setup, find_packages
import uestc

setup(author=uestc.__author__,
      author_email='plusls@qq.com',
      maintainer=uestc.__author__,
      name=uestc.__name__,
      packages=find_packages(exclude=('test', 'test.*')),
      long_description=open('README.rst', encoding='utf-8').read(),
      version=uestc.__version__,
      keywords='uestc catch course login',
      description=uestc.__doc__,
      url="https://github.com/plusIs/uestc",
      install_requires=['beautifulsoup4>=4.6.0',
                        'requests>=2.17.3'],
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
