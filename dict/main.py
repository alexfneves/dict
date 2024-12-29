from logging import DEBUG, INFO, basicConfig, debug, info, warning
from sys import exit

import click
from textual.logging import TextualHandler

from dict.app import DictApp
from dict.dictionary import create_db, create_words
from dict.settings import Settings


def config(verbose: bool, very_very_verbose: bool, data_path: str):
    if verbose:
        basicConfig(level=INFO, handlers=[TextualHandler()])
    if very_very_verbose:
        basicConfig(level=DEBUG, handlers=[TextualHandler()])
    s = Settings()
    s.load(data_path)
    create_db()
    create_words()


def option_data_path(func):
    """Decorator for common options."""
    func = click.option(
        "--data-path", default=None, help="Path for the dict data folder"
    )(func)
    return func


def option_verbose(func):
    func = click.option("-v", "--verbose", is_flag=True, help="Verbose")(func)
    return func


def option_very_very_verbose(func):
    func = click.option(
        "-vvv", "--very-very-verbose", is_flag=True, help="Very very verbose"
    )(func)
    return func


def common_options(func):
    return option_data_path(option_very_very_verbose(option_verbose(func)))


@click.group(invoke_without_command=True)
@click.pass_context
@common_options
def cli(ctx, verbose, very_very_verbose, data_path: str):
    if ctx.invoked_subcommand is None:
        config(verbose, very_very_verbose, data_path)
        info("Invoked without subcommand, app will be executed")
        app = DictApp()
        app.run()
        exit(app.return_code)


@cli.command()
@common_options
def app(verbose, very_very_verbose, data_path):
    config(verbose, very_very_verbose, data_path)
    info("Executing app")
    app = DictApp()
    app.run()
    sys.exit(app.return_code)


@cli.command()
@common_options
@click.argument("word")
def search(verbose, very_very_verbose, data_path, word: str):
    config(verbose, very_very_verbose, data_path)
    info(f"Executing search {word}")


@cli.command()
@common_options
@click.argument("word")
def meaning(verbose, very_very_verbose, data_path, word: str):
    config(verbose, very_very_verbose, data_path)
    info(f"Executing meaning {word}")


@cli.command()
@common_options
@click.argument("phrase")
def play(verbose, very_very_verbose, data_path, phrase: str):
    config(verbose, very_very_verbose, data_path)
    info(f"Executing play {phrase}")


if __name__ == "__main__":
    cli()
