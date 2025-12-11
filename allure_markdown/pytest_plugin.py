import os

from allure_markdown.config import config
from allure_markdown.main import AllureMarkdown


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
        default=config.title,
        help="Title for the generated markdown report"
    )
    group.addoption(
        "--allure-markdown-description",
        default=config.description,
        help="Description for the generated markdown report"
    )
    group.addoption(
        "--allure-markdown-output",
        default=config.output,
        help="Output path for the generated markdown report"
    )
    group.addoption(
        "--allure-markdown-custom-content",
        default="",
        help="Custom content to add after title"
    )


def pytest_configure(config):
    if hasattr(config, "slaveinput"):
        return  # xdist compatibility

    config.addinivalue_line(
        "markers",
        "allure_markdown: Mark tests for allure-markdown report"
    )


def pytest_sessionfinish(session):
    config = session.config

    if not config.getoption("--allure-markdown-generate"):
        return

    results_dir = config.getoption("--alluredir")
    title = config.getoption("--allure-markdown-title")
    description = config.getoption("--allure-markdown-description")
    output = config.getoption("--allure-markdown-output")
    custom_content = config.getoption("--allure-markdown-custom-content")

    try:
        AllureMarkdown(
            results_dir=results_dir,
            output=output,
            title=title,
            description=description,
            custom_content=custom_content,
        ).gen()

    except Exception as e:
        session.config.pluginmanager.getplugin("terminalreporter").write(
            f"\nERROR: Failed to generate markdown report: {str(e)}\n"
        )
