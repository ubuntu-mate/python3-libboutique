from setuptools import find_packages, setup


with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="python3-libboutique",
    version="0.1.0",
    description="Software Boutique's management for curated applications with interfaces for Apt, Snapd and others.",
    long_description=readme,
    author="Jeff Labonte",
    author_email="jeff.labonte12@gmail.com",
    url="https://github.com/ubuntu-mate/python3-boutique",
    packages=find_packages(exclude=("tests", "docs")),
)
