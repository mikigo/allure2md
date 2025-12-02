import json
import os
from typing import List, Dict, Union

from allure_markdown._setting import setting


class AllureMarkdown:
    def __init__(
            self,
            metadata_path: str,
            output_dir: str,
            title: str = None,
            description: str = None,
    ):
        self.metadata_path = metadata_path
        self.output_dir = output_dir
        self.title = title or setting.title
        self.description = description or setting.description
        self.mds = []

    def content_level(self, level: int):
        return level * "#"

    def mds_append(self, line: str, bland_line: bool = True, new_line_symbol: str = "markdown"):
        if new_line_symbol == "markdown":
            new_line_symbol = "\n"
        elif new_line_symbol == "html":
            new_line_symbol = "<br/>"
        if bland_line:
            self.mds.append(f"{line}{new_line_symbol * 2}")
        else:
            self.mds.append(f"{line}{new_line_symbol * 1}")

    def set_title(self, title: str):
        self.title = title

    def set_description(self, description: str):
        self.description = description

    def get_json_files(self):
        json_files = []
        for root, _, files in os.walk(self.metadata_path):
            for file in files:
                if file.endswith('.json'):
                    json_files.append(os.path.join(root, file))
        return json_files

    def append_title(self):
        self.mds_append(f"{self.content_level(1)} {self.title}")

    def append_description(self):
        self.mds_append(f"{self.content_level(2)} Description")
        self.mds_append(self.description)

    def append_cases(self):
        self.mds_append(f"{self.content_level(2)} Test Cases")
        json_files = self.get_json_files()
        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                titlePath: List[str, str] = data.get("titlePath")
                fullName: str = data.get("fullName")
                test_CaseId: str = data.get("testCaseId")
                start: int = data.get("start")
                labels: List[Dict[str, str]] = data.get("labels")
                attachments: List[Dict[str, str]] = data.get("attachments")
                steps: List[Dict[str, Union[str, Dict]]] = data.get("steps")
                stage: str = data.get("stage")
                statusDetails: Dict[str, str] = data.get("statusDetails")
                status: str = data.get("status")
                historyId: str = data.get("historyId")
                name: str = data.get("name")
                uuid: str = data.get("uuid")

                self.mds_append(f"{self.content_level(3)} {f'✅' if status == 'passed' else '❌'} {fullName}")
                self.mds_append(name)
                self.mds_append(f"{self.content_level(4)} Status")
                self.mds_append(f"{status} {f'✅' if status == 'passed' else '❌'}")

                if attachments:
                    self.mds_append(f"{self.content_level(4)} Attachments")
                    for attachment in attachments:
                        name = attachment.get('name')
                        type = attachment.get('type')
                        source = attachment.get('source')
                        if type == "text/plain":
                            with open(os.path.join(self.metadata_path, source), 'r', encoding='utf-8') as f:
                                self.mds_append(f"{name}")
                                self.mds_append("```python", bland_line=False)
                                self.mds_append(f"{f.read()}", bland_line=False)
                                self.mds_append("```")
                        else:
                            self.mds_append(f"![{name}]({source})")

                if steps:
                    self.mds_append(f"{self.content_level(4)} Steps")

                    self.mds_append("<details>", bland_line=False)
                    self.mds_append(f"<summary><strong>Steps Details</strong></summary>", bland_line=False)
                    for step in steps:
                        name = step.get('name')
                        if name not in ["screenshot", "video"]:
                            self.mds_append(f"{name}", bland_line=False, new_line_symbol="html")
                    self.mds_append("</details>")

                    for step in steps:
                        name = step.get('name')
                        if name == "screenshot":
                            self.mds_append(f"{self.content_level(5)} ScreenShot")
                            for attachment in step.get('attachments'):
                                self.mds_append(
                                    f"![{name}]({os.path.join(self.metadata_path, attachment.get('source'))})")
                        elif name == "video":
                            self.mds_append(f"{self.content_level(5)} Video")
                            for attachment in step.get('attachments'):
                                self.mds_append(f"<video>", bland_line=False)
                                self.mds_append(f"<source src={os.path.join(self.metadata_path, attachment.get('source'))} type=video/mp4>")
                                self.mds_append(f"</video>")
                if statusDetails:
                    self.mds_append("#### Status Details")
                    message = statusDetails.get('message')
                    if message:
                        self.mds_append("##### message")
                        self.mds_append("```python", bland_line=False)
                        self.mds_append(rf"{message}", bland_line=False)
                        self.mds_append("```")

                    trace = statusDetails.get('trace')
                    if trace:
                        self.mds_append("##### trace")
                        self.mds_append("```python", bland_line=False)
                        self.mds_append(rf"{trace}", bland_line=False)
                        self.mds_append("```")

                if labels:
                    self.mds_append(f"{self.content_level(4)} Labels")
                    self.mds_append("<details>", bland_line=False)
                    self.mds_append(f"<summary><strong>Labels Details</strong></summary>", bland_line=False)
                    for label in labels:
                        self.mds_append(f"{label.get('name')}: {label.get('value')}", bland_line=False, new_line_symbol="html")
                    self.mds_append("</details>")

    def merge_md(self):
        self.append_title()
        self.append_description()
        self.append_cases()

    def save_md(self):
        os.makedirs(self.output_dir, exist_ok=True)
        output_file = os.path.join(self.output_dir, 'report.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(''.join(self.mds))
        print(f"Markdown report saved to {output_file}")

    def main(self):
        self.merge_md()
        self.save_md()


if __name__ == '__main__':
    am = AllureMarkdown(
        metadata_path='../metadata',
        output_dir='../md'
    )
    am.main()
