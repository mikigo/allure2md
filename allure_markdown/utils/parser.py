import json
import os
import shutil
from typing import Dict, List, Tuple


def read_environment_file(environment_path: str) -> Dict[str, str]:
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


def scan_allure_results(results_dir: str) -> Tuple[List[Dict], Dict[str, str]]:
    test_results = []
    environment = {}

    environment_file = os.path.join(results_dir, 'environment.properties')
    if os.path.exists(environment_file):
        environment = read_environment_file(environment_file)

    for filename in os.listdir(results_dir):
        if filename.endswith('.json') and not filename.startswith('categories'):
            file_path = os.path.join(results_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('name') and data.get('status'):
                        test_results.append(data)
            except json.JSONDecodeError:
                continue

    return test_results, environment


def parse_test_results(test_results: List[Dict], results_dir, output) -> Tuple[Dict, List[Dict]]:
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
            fail_details.append(_parse_fail_details(test, results_dir, output))
        elif status == 'skipped':
            summary['skipped'] += 1
        elif status == 'broken':
            summary['broken'] += 1
            fail_details.append(_parse_fail_details(test, results_dir, output))

    return summary, fail_details


def _parse_fail_details(test: Dict, results_dir, output) -> Dict:
    attachments = []
    try:
        output_dir = os.path.dirname(output)
        os.makedirs(output_dir, exist_ok=True)
    except:
        output_dir = "."
    if 'attachments' in test:
        for attachment in test['attachments']:

            at = {
                'name': attachment.get('name', 'Attachment'),
                'path': attachment.get('source', ''),
                'type': attachment.get('type', ''),
            }

            if attachment.get('type', '') == "text/plain":
                with open(os.path.join(results_dir, attachment.get('source', '')), "r", encoding="utf-8") as f:
                    at['content'] = f.read()
            if attachment.get('type') in ("video/mp4", "image/png"):
                # 拷贝到output_dir目录下
                shutil.copyfile(
                    os.path.join(results_dir, attachment.get('source')),
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


def get_allure_results(results_dir: str) -> Tuple[Dict, List[Dict], Dict[str, str]]:
    test_results, environment = scan_allure_results(results_dir)
    summary, fail_details = parse_test_results(test_results)
    return summary, fail_details, environment
