import os

from allure_markdown.utils.parser import scan_allure_results, parse_test_results
from allure_markdown.utils.report_generator import generate_markdown_report


def pytest_addoption(parser):
    group = parser.getgroup("allure_markdown", "Allure-Markdown options")
    group.addoption(
        "--allure-markdown-generate",
        action="store_true",
        default=False,
        help="Generate markdown report from allure results after test session"
    )
    group.addoption(
        "--allure-markdown-title",
        default="Allure Markdown Report",
        help="Title for the generated markdown report"
    )
    group.addoption(
        "--allure-markdown-description",
        default="This is a markdown report generated from Allure metadata",
        help="Description for the generated markdown report"
    )
    group.addoption(
        "--allure-markdown-output",
        default="allure_report.md",
        help="Output path for the generated markdown report"
    )
    group.addoption(
        "--allure-markdown-results-dir",
        default="allure-results",
        help="Path to allure results directory"
    )


def pytest_configure(config):
    if hasattr(config, "slaveinput"):
        return  # xdist compatibility

    config.addinivalue_line(
        "markers",
        "allure_markdown: Mark tests for allure-markdown report"
    )


def pytest_sessionfinish(session, exitstatus):
    config = session.config

    if not config.getoption("--allure-markdown-generate"):
        return

    results_dir = config.getoption("--allure-markdown-results-dir")

    if not os.path.exists(results_dir):
        session.config.pluginmanager.getplugin("terminalreporter").write(
            f"\nWARNING: Allure results directory '{results_dir}' not found. No markdown report generated.\n"
        )
        return

    title = config.getoption("--allure-markdown-title")
    description = config.getoption("--allure-markdown-description")
    output_path = config.getoption("--allure-markdown-output")

    try:
        test_results, environment = scan_allure_results(results_dir)

        if not test_results:
            session.config.pluginmanager.getplugin("terminalreporter").write(
                f"\nWARNING: No test results found in '{results_dir}'. No markdown report generated.\n"
            )
            return

        summary, fail_details = parse_test_results(test_results)

        generate_markdown_report(
            summary=summary,
            fail_details=fail_details,
            environment=environment,
            title=title,
            description=description,
            output_path=output_path
        )

        session.config.pluginmanager.getplugin("terminalreporter").write(
            f"\nAllure-Markdown: Report generated successfully at '{output_path}'\n"
        )

    except Exception as e:
        session.config.pluginmanager.getplugin("terminalreporter").write(
            f"\nERROR: Failed to generate markdown report: {str(e)}\n"
        )
