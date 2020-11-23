from distutils.core import setup
from setuptools import find_packages

with open("requirement.txt", 'r') as file:
    requirement = file.readlines()


setup(
    name="chaos",
    version="1.0",
    description="",
    author="zazbone",
    author_email="coczaz@gmail.com",
    packages=find_packages(),
    install_requires=requirement,
)
