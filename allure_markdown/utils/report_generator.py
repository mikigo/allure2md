from typing import Dict, List

from jinja2 import Environment, PackageLoader, select_autoescape


def generate_markdown_report(
        summary: Dict,
        fail_details: List[Dict],
        environment: Dict[str, str],
        title: str = "Allure Markdown Report",
        description: str = "This is a markdown report generated from Allure metadata",
        custom_content: str = "",
        output_path: str = "allure_report.md"
) -> None:
    env = Environment(
        loader=PackageLoader("allure_markdown", "templates"),
        autoescape=select_autoescape()
    )

    template = env.get_template("report.md.j2")

    report_content = template.render(
        title=title,
        description=description,
        custom_content=custom_content,
        environment=environment,
        summary=summary,
        fail_details=fail_details
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"Report generated successfully: {output_path}")
