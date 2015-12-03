from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='generateFiles',
      version=version,
      description="Programa para gerar arquivos .csv e .txt de dados extraidos de tabelas do banco de dados",
      long_description='',
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='lucas lamounier',
      author_email='lucasls.oas@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'bottle',
          'bottledaemon',
          'pyodbc',
          'setuptools',
          'configparser',
          'sqlalchemy',
          'zope.sqlalchemy',
          'transaction',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
