import click

from dict.app import DictApp
from dict.config import Config

def config(data_path: str):
    c = Config()
    c.load(data_path)

def common_options(func):
    """Decorator for common options."""
    func = click.option('--data-path', default=None, help='Path for the dict data folder')(func)
    return func

@click.group(invoke_without_command=True)
@click.pass_context
@common_options
def cli(ctx, data_path: str):
    if ctx.invoked_subcommand is None:
        config(data_path)
        c = Config()
        click.echo('I was invoked without subcommand, app will be started')
        app = DictApp()
        app.run()
    else:
        click.echo(f"I am about to invoke {ctx.invoked_subcommand}")

@cli.command()
@common_options
def app(data_path):
    config(data_path)
    click.echo('The subcommand app')
    app = DictApp()
    app.run()

@cli.command()
@common_options
@click.argument('word')
def search(data_path, word: str):
    config(data_path)
    click.echo(f'The subcommand search {word}')

@cli.command()
@common_options
@click.argument('word')
def meaning(data_path, word: str):
    config(data_path)
    click.echo(f'The subcommand meaning {word}')

@cli.command()
@common_options
@click.argument('phrase')
def play(data_path, phrase: str):
    config(data_path)
    click.echo(f'The subcommand play {phrase}')
