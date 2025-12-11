import sys

from allure_markdown.cli import cli

if __name__ == '__main__':
    sys.argv.extend(['-r', 'metadata'])
    sys.argv.extend(['-c', 'url: https://mikigo.site'])
    cli()
