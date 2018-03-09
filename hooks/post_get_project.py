import os
import shutil

print(os.getcwd())  # prints /absolute/path/to/{{cookiecutter.project_slug}}

def remove(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)


if not bool('{{cookiecutter.cli_app}}'):
    # Remove the cli app
    remove(os.path.join('{{cookiecutter.app_name}}', '__main__.py'))

