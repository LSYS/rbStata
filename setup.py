"""cookiecutter distutils configuration."""
from setuptools import find_packages, setup

version = "dev"

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

install_requires = [
    "pandas",
    "anyascii",
    "click>=8.*",
]

setup(
    name="rbstata",
    version=version,
    description=(
        "A command-line utility that converts (or roll back) versions of Stata dta data files."
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Lucas Shen",
    author_email="lucas@lucasshen.com",
    url="https://github.com/lsys/rbStata",
    packages=find_packages(),
    entry_points={"console_scripts": ["rbstata = rbStata.cli:rbstata"]},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=install_requires,
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    keywords=[
        "Stata",
        "Python",
        "cli",
        "compatibility",
        "version",
    ],
)
