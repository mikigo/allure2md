# Allure-Markdown

Allure-Markdown是一个Python项目，能将Allure的元数据转换为Markdown格式的报告，不需要Java环境和Allure报告生成工具即可使用。

## 功能特性

- 将Allure JSON元数据转换为Markdown报告
- 无需Java环境和Allure命令行工具
- 支持pytest钩子自动生成报告
- 提供命令行界面手动转换
- 美观易读的Markdown输出格式

## 依赖

- allure-pytest
- pytest
- jinja2
- click

## 安装

使用pip安装：

```bash
pip install allure-markdown
```

或使用poetry安装：

```bash
poetry add allure-markdown
```

## 使用方法

### 1. 命令行使用

```bash
allure-markdown [OPTIONS]
```

**参数说明：**

- `--results-dir, -r`: Allure结果目录路径（默认：allure-results）
- `--output, -o`: 输出Markdown文件路径（默认：allure_report.md）
- `--title, -t`: 报告标题（默认：Allure Markdown Report）
- `--description, -d`: 报告描述（默认：This is a markdown report generated from Allure metadata）
- `--custom-content, -c`: 标题后添加的自定义内容（默认：无）

**示例：**

```bash
# 使用默认配置生成报告
allure-markdown

# 指定结果目录和输出文件
allure-markdown -r my-allure-results -o my_report.md

# 自定义标题和描述
allure-markdown -t "My Test Report" -d "This is my custom description"
```

### 2. Pytest钩子使用

在pytest命令中添加参数启用自动报告生成：

```bash
pytest --alluredir=allure-results --allure-markdown-generate
```

**可用的pytest参数：**

- `--allure-markdown-generate`: 测试会话结束后从Allure结果生成Markdown报告
- `--allure-markdown-title`: 生成的Markdown报告标题
- `--allure-markdown-description`: 生成的Markdown报告描述
- `--allure-markdown-output`: 生成的Markdown报告输出路径
- `--allure-markdown-results-dir`: Allure结果目录路径

**示例：**

```bash
# 基本使用
pytest --alluredir=allure-results --allure-markdown-generate

# 自定义报告配置
pytest --alluredir=my-results --allure-markdown-generate --allure-markdown-title="My Test Report" --allure-markdown-output="test_report.md"
```

## Markdown报告内容

生成的Markdown报告包含以下部分：

```markdown
# Title

## Description

## Environment

## Summary

## Fail Details
```

**内容说明：**

- **Title**: 报告标题，可自定义
- **Description**: 报告描述，可自定义
- **Environment**: 环境信息，从environment.properties文件读取
- **Summary**: 测试汇总结果，包括通过、失败、跳过等统计
- **Fail Details**: 失败测试的详细信息，包括错误信息、堆栈跟踪和附件

## 基本原理

1. 依赖allure-pytest生成的元数据（json文件及其附件）
2. 扫描并读取allure的json结果数据
3. 基于jinja2模板引擎生成markdown报告
4. 提供命令行和pytest钩子两种调用方式

## 项目结构

```
allure-markdown/
├── allure_markdown/
│   ├── utils/
│   │   ├── parser.py         # Allure元数据解析
│   │   └── report_generator.py  # Markdown报告生成
│   ├── templates/
│   │   └── report.md.j2      # Jinja2模板
│   ├── cli.py                # 命令行界面
│   ├── pytest_plugin.py      # Pytest插件
│   └── __init__.py
├── README.md
├── LICENSE
└── pyproject.toml
```