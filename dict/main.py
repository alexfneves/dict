import click
from dict.app import DictApp

def common_options(func):
    """Decorator for common options."""
    func = click.option('--config-path', default=None, help='Path for the configuration file')(func)
    return func

@click.group(invoke_without_command=True)
@click.pass_context
@common_options
def cli(ctx, config_path):
    if ctx.invoked_subcommand is None:
        click.echo('I was invoked without subcommand, app will be started')
        app = DictApp()
        app.run()
    else:
        click.echo(f"I am about to invoke {ctx.invoked_subcommand}")

@cli.command()
@common_options
def app(config_path):
    click.echo('The subcommand app')
    app = DictApp()
    app.run()

@cli.command()
@common_options
@click.argument('word')
def search(config_path, word: str):
    click.echo(f'The subcommand search {word}')
    click.echo(f'The subcommand search')

@cli.command()
@common_options
@click.argument('word')
def meaning(config_path, word: str):
    click.echo(f'The subcommand meaning {word}')

@cli.command()
@common_options
@click.argument('phrase')
def play(config_path, phrase: str):
    click.echo(f'The subcommand play {phrase}')
