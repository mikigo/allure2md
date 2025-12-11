

import click

from allure_markdown.config import config
from allure_markdown.main import AllureMarkdown


@click.command()
@click.help_option("-h", "--help", help="查看帮助信息")
@click.option('--results-dir', '-r', default=None,
              help=f'Path to allure metadata results directory (default: {config.results_dir})')
@click.option('--output', '-o', default=None, help=f'Output markdown file path (default: {config.output})')
@click.option('--title', '-t', default=None, help=f'Report title (default: {config.title})')
@click.option('--description', '-d', default=None, help=f'Report description (default: {config.description})')
@click.option('--custom-content', '-c', default=None, help='Custom content to add after title')
def cli(results_dir, output, title, description, custom_content):
    AllureMarkdown(
        results_dir=results_dir,
        output=output,
        title=title,
        description=description,
        custom_content=custom_content,
    ).gen()


if __name__ == '__main__':
    cli()