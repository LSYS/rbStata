"""cookiecutter distutils configuration."""
from setuptools import setup, find_packages

version = "dev"

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

install_requires = [
    # 'pandas',
    # 'click'
]    

setup(
    name='wbstata',
    version=version,
    description=(
        'A command-line utility that creates projects from project '
        'templates, e.g. creating a Python package project from a '
        'Python package project template.'
    ),
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Lucas Shen',
    author_email='lucas@lucasshen.com',
    url='https://github.com/lsys/wbStata',
    packages=find_packages(),
    entry_points={'console_scripts': ['wbstata = wbStata.cli:wbstata']},
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=install_requires,
    license='BSD',
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    keywords=[
        "cookiecutter",
        "Python",
        "projects",
        "project templates",
        "Jinja2",
        "skeleton",
        "scaffolding",
        "project directory",
        "package",
        "packaging",
    ],
)