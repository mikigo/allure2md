import os

import click

from allure_markdown.utils.parser import scan_allure_results, parse_test_results
from allure_markdown.utils.report_generator import generate_markdown_report
from allure_markdown.config import config


@click.command()
@click.option('--results-dir', '-r', default=config.metadata,
              help='Path to allure results directory (default: allure-results)')
@click.option('--output', '-o', default=config.output,
              help='Output markdown file path (default: allure_report.md)')
@click.option('--title', '-t', default=config.title,
              help='Report title (default: Allure Markdown Report)')
@click.option('--description', '-d', default=config.description,
              help='Report description (default: This is a markdown report generated from Allure metadata)')
@click.option('--custom-content', '-c', default='',
              help='Custom content to add after title (default: none)')
def main(results_dir, output, title, description, custom_content):
    click.echo("Allure-Markdown: Converting Allure metadata to Markdown...")

    if not os.path.exists(results_dir):
        click.echo(f"Error: Results directory '{results_dir}' not found.")
        return 1

    try:
        test_results, environment = scan_allure_results(results_dir)

        if not test_results:
            click.echo(f"Warning: No test results found in '{results_dir}'.")
            return 0

        summary, fail_details = parse_test_results(test_results, results_dir, output)

        generate_markdown_report(
            summary=summary,
            fail_details=fail_details,
            environment=environment,
            title=title,
            description=description,
            custom_content=custom_content,
            output_path=output
        )

        click.echo(f"Success: Markdown report generated at '{output}'")
        return 0

    except Exception as e:
        click.echo(f"Error: {str(e)}")
        return 1


if __name__ == '__main__':
    main()
