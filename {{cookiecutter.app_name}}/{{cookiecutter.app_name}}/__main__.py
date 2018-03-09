import click



CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """
    {{ cookiecutter.project_short_description }}
    """
    pass


def run():
    main()


if __name__ == '__main__':
    run()
