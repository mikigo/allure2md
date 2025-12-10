#  Allure Markdown Report

url:https://mikigo.site

## Description
This is a markdown report generated from Allure metadata.
## Environment

| Name | Value |
|------|-------|
| System | Windows |
| version | 10 |
| Python | 3.8 |

## Summary

| Passed | Failed | Skipped | Broken | Total |
|--------|-------|--------|-------|--------|
| 5 | 5 | 0 | 0 | 10 |
## Fail Details
###  test_allure_simple_failed

**Node ID:** tests.test_allure_simple#test_allure_simple_failed

**Status:** failed

**Error Message:**

```python
AssertionError: This test intentionally fails
assert False
```

**Traceback:**

```python
@allure.feature("简单功能")
    def test_allure_simple_failed():
        """Allure test that fails"""
        allure.attach("Test log", "This is a simple log for failed test", allure.attachment_type.TEXT)
>       assert False, "This test intentionally fails"
E       AssertionError: This test intentionally fails
E       assert False

tests\test_allure_simple.py:15: AssertionError
```
**Attachments:**
```python
Test log
```
###  test_simple_failed

**Node ID:** tests.test_simple#test_simple_failed

**Status:** failed

**Error Message:**

```python
AssertionError: This test intentionally fails
assert False
```

**Traceback:**

```python
def test_simple_failed():
        """Simple test that fails"""
>       assert False, "This test intentionally fails"
E       AssertionError: This test intentionally fails
E       assert False

tests\test_simple.py:8: AssertionError
```
###  test_with_screenshot

**Node ID:** tests.test_comprehensive#test_with_screenshot

**Status:** failed

**Error Message:**

```python
AssertionError: 带有截图附件的测试成功
assert False
```

**Traceback:**

```python
@allure.feature("附件测试")
    @allure.story("截图附件")
    def test_with_screenshot():
        """测试带有截图附件"""
        # 创建一个简单的PNG文件作为截图
        screenshot_path = os.path.join(temp_dir, "test_screenshot.png")
        with open(screenshot_path, "wb") as f:
            f.write(
                b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x90\x91\xb6\x5b\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\x09pHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xe5\x0c\x15\x09\x11\x16\x12\xe8\x94y\x00\x00\x00\x19tEXtComment\x00Created with Python\xca\xe4\x95\xa3\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xcc\x59\xe7\x00\x00\x00\x00IEND\xaeB`\x82')
    
        # 附加截图
        with open(screenshot_path, 'rb') as f:
            allure.attach(f.read(), name="测试截图", attachment_type=allure.attachment_type.PNG)
    
>       assert False, "带有截图附件的测试成功"
E       AssertionError: 带有截图附件的测试成功
E       assert False

tests\test_comprehensive.py:51: AssertionError
```
**Attachments:**
![测试截图](78efcf09-b11b-49d5-80ac-1b5fb55652ac-attachment.png)
###  test_with_video

**Node ID:** tests.test_comprehensive#test_with_video

**Status:** failed

**Error Message:**

```python
AssertionError: 带有视频附件的测试成功
assert False
```

**Traceback:**

```python
@allure.feature("附件测试")
    @allure.story("视频附件")
    def test_with_video():
        """测试带有视频附件"""
        # 创建一个简单的MP4文件作为视频
        video_path = os.path.join(temp_dir, "test_video.mp4")
        with open(video_path, "wb") as f:
            f.write(b'\x00\x00\x00 ftypisom\x00\x00\x02\x00isomiso2mp41\x00\x00\x00\x08free\x00\x00\x00mdat')
    
        # 附加视频
        with open(video_path, 'rb') as f:
            allure.attach(f.read(), name="测试视频", attachment_type=allure.attachment_type.MP4)
    
>       assert False, "带有视频附件的测试成功"
E       AssertionError: 带有视频附件的测试成功
E       assert False

tests\test_comprehensive.py:67: AssertionError
```
**Attachments:**

<video controls width="100%">
    <source src="d51a2056-50b4-4e11-8b8f-10204bd8258d-attachment.mp4" type="video/mp4">
</video>
###  test_failed_with_error_details

**Node ID:** tests.test_comprehensive#test_failed_with_error_details

**Status:** failed

**Error Message:**

```python
AssertionError: 测试失败，原因: division by zero
assert False
```

**Traceback:**

```python
@allure.feature("综合测试")
    @allure.story("失败场景")
    def test_failed_with_error_details():
        """测试失败并带有错误详情"""
        try:
            allure.step("执行可能失败的操作")
            allure.attach("操作参数", "这是导致失败的参数值", allure.attachment_type.TEXT)
>           result = 10 / 0  # 制造除零错误
E           ZeroDivisionError: division by zero

tests\test_comprehensive.py:30: ZeroDivisionError

During handling of the above exception, another exception occurred:

    @allure.feature("综合测试")
    @allure.story("失败场景")
    def test_failed_with_error_details():
        """测试失败并带有错误详情"""
        try:
            allure.step("执行可能失败的操作")
            allure.attach("操作参数", "这是导致失败的参数值", allure.attachment_type.TEXT)
            result = 10 / 0  # 制造除零错误
        except ZeroDivisionError as e:
            allure.attach("错误信息", str(e), allure.attachment_type.TEXT)
            allure.attach("异常类型", type(e).__name__, allure.attachment_type.TEXT)
>           assert False, f"测试失败，原因: {e}"
E           AssertionError: 测试失败，原因: division by zero
E           assert False

tests\test_comprehensive.py:34: AssertionError
```
**Attachments:**
```python
操作参数
```
```python
错误信息
```
```python
异常类型
```