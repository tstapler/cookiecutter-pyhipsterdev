import re
from os import path
from codecs import open

from setuptools import setup, find_packages

__version__ = '{{cookiecutter.version}}'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [re.sub(r"--hash=.*", "",x.strip()) for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='{{cookiecutter.app_name}}',
    version=__version__,
    description="{{cookiecutter.project_short_description}}",
    long_description=long_description,
    url='https://github.com/{{cookiecutter.github_project_owner}}/{{cookiecutter.app_name}}',
    download_url='https://github.com/{{cookiecutter.github_project_owner}}/{{cookiecutter.app_name}}/tarball/' + __version__,
    {%- if cookiecutter.license %}
    license='{{ cookiecutter.license }}',
    {%- endif %}
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='{{cookiecutter.full_name}}',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='{{cookiecutter.email}}',
    {%- if cookiecutter.cli_app == 'true' %}
    entry_points={
        'console_scripts': [
            "{{cookiecutter.app_name}} = {{cookiecutter.app_name}}.__main__:run"
        ]
    },
    {%- endif %}
)
