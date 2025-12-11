import json
import os
import pathlib
import shutil
from typing import Tuple, List, Dict

from jinja2 import Environment, PackageLoader, select_autoescape

from allure_markdown.config import config

class AllureMarkdown:

    def __init__(
            self,
            *,
            results_dir: str = None,
            output: str = None,
            title: str = None,
            description: str = None,
            custom_content: str = None,
    ):
        self.results_dir = results_dir or config.results_dir
        if not pathlib.Path(self.results_dir).exists():
            raise FileNotFoundError("Results directory does not exist")

        self.output = output or config.output
        self.title = title or config.title
        self.description = description or config.description
        self.custom_content = custom_content

    def read_environment_file(self, environment_path: str) -> Dict[str, str]:
        environment = {}
        if os.path.exists(environment_path):
            with open(environment_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            environment[key.strip()] = value.strip()
        return environment

    def scan_allure_results(self) -> Tuple[List[Dict], Dict[str, str]]:
        test_results = []
        environment = {}

        environment_file = os.path.join(self.results_dir, 'environment.properties')
        if os.path.exists(environment_file):
            environment = self.read_environment_file(environment_file)

        for filename in os.listdir(self.results_dir):
            if filename.endswith('.json') and not filename.startswith('categories'):
                file_path = os.path.join(self.results_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get('name') and data.get('status'):
                            test_results.append(data)
                except json.JSONDecodeError:
                    continue

        return test_results, environment

    def parse_test_results(self, test_results: List[Dict]) -> Tuple[Dict, List[Dict]]:
        summary = {
            'total': len(test_results),
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'broken': 0
        }

        fail_details = []

        for test in test_results:
            status = test.get('status', 'unknown')

            if status == 'passed':
                summary['passed'] += 1
            elif status == 'failed':
                summary['failed'] += 1
                fail_details.append(self._parse_fail_details(test))
            elif status == 'skipped':
                summary['skipped'] += 1
            elif status == 'broken':
                summary['broken'] += 1
                fail_details.append(self._parse_fail_details(test))

        return summary, fail_details

    def _parse_fail_details(self, test: Dict) -> Dict:
        attachments = []
        output_dir = pathlib.Path(self.output).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        output_dir = output_dir.as_posix()
        if 'attachments' in test:
            for attachment in test['attachments']:

                at = {
                    'name': attachment.get('name', 'Attachment'),
                    'path': attachment.get('source', ''),
                    'type': attachment.get('type', ''),
                }

                if attachment.get('type', '') == "text/plain":
                    with open(os.path.join(self.results_dir, attachment.get('source', '')), "r", encoding="utf-8") as f:
                        at['content'] = f.read()
                if attachment.get('type') in ("video/mp4", "image/png"):
                    # 拷贝到output_dir目录下
                    shutil.copyfile(
                        os.path.join(self.results_dir, attachment.get('source')),
                        os.path.join(output_dir, attachment.get('source'))
                    )
                attachments.append(at)

        error_message = ''
        traceback = ''

        if 'statusDetails' in test:
            details = test['statusDetails']
            if 'message' in details:
                error_message = details['message']
            if 'trace' in details:
                traceback = details['trace']

        return {
            'name': test.get('name', 'Unnamed Test'),
            'nodeid': test.get('fullName', ''),
            'status': test.get('status', 'unknown'),
            'error_message': error_message,
            'traceback': traceback,
            'attachments': attachments
        }

    def get_allure_results(self) -> Tuple[Dict, List[Dict], Dict[str, str]]:
        test_results, environment = self.scan_allure_results()
        summary, fail_details = self.parse_test_results(test_results)
        return summary, fail_details, environment

    def generate_markdown_report(
            self,
            *,
            summary: Dict,
            fail_details: List[Dict],
            environment: Dict[str, str],
            title: str = None,
            description: str = None,
            custom_content: str = None,
            output_path: str = None,
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

    def gen(self):
        print("Allure-Markdown: Converting Allure metadata to Markdown...")

        if not os.path.exists(self.results_dir):
            print(f"Error: Results directory '{self.results_dir}' not found.")
            return 1

        try:
            test_results, environment = self.scan_allure_results()

            if not test_results:
                print(f"Warning: No test results found in '{self.results_dir}'.")
                return 0

            summary, fail_details = self.parse_test_results(test_results)

            self.generate_markdown_report(
                summary=summary,
                fail_details=fail_details,
                environment=environment,
                title=self.title,
                description=self.description,
                custom_content=self.custom_content,
                output_path=self.output
            )

            print(f"Success: Markdown report generated at '{self.output}'")
            return 0

        except Exception as e:
            print(f"Error: {str(e)}")
            return 1
