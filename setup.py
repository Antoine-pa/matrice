from setuptools import setup

setup(
   name='matrice',
   version='1.0',
   description='a matricial calculus module',
   author='Antoine Pa',
   author_email='antoine.pascal@gmx.fr',
   packages=['matrice'],  #same as name
   install_requires=['numpy'], #external packages as dependencies
)