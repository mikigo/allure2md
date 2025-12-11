# Allure-Markdown

Allure-Markdown 是一个 Python 项目，能将 Allure 的元数据转换为 Markdown 格式的报告。

## 功能特性

- 将 Allure JSON 元数据转换为 Markdown 报告
- 不需要安装 Allure 生成工具，更不需要 Java 环境
- 支持 pytest 钩子自动生成报告
- 提供命令行一键转换
- 美观易读的 Markdown 输出格式

## 安装

使用pip安装：

```bash
pip install allure-markdown
```

## 使用方法

### 1. 命令行使用

```bash
allure-markdown [OPTIONS]
```

**参数说明：**

- `--results-dir, -r`: Allure结果目录路径（默认：allure-results）
- `--output, -o`: 输出Markdown文件路径（默认：allure_markdown_report.md）
- `--title, -t`: 报告标题（默认：Allure Markdown Report）
- `--description, -d`: 报告描述（默认：This is a markdown report generated from Allure metadata）
- `--custom-content, -c`: 标题后添加的自定义内容（默认：无）

**示例：**

```bash
# 使用默认配置生成报告
allure-markdown

# 指定结果目录和输出文件
allure-markdown -r allure-results -o my_report.md

# 自定义标题和描述
allure-markdown -t "My Test Report" -d "This is my custom description"
```

### 2. Pytest 钩子使用

在 pytest 命令中添加参数启用自动报告生成：

```bash
pytest --alluredir=allure-results --allure-markdown-generate
```

**可用的 pytest 参数：**

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

## Markdown 报告内容

查看报告示例：

[allure_markdown_report.md](allure_markdown_report.md)

生成的 Markdown 报告包含以下部分：

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
