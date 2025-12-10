import os
import tempfile

import allure

# 创建临时文件目录
temp_dir = tempfile.mkdtemp()


@allure.feature("综合测试")
@allure.story("成功场景")
def test_passed_with_allure_logs():
    """测试成功并带有Allure日志"""
    allure.step("执行测试步骤1")
    allure.attach("步骤1日志", "这是步骤1的详细日志信息", allure.attachment_type.TEXT)

    allure.step("执行测试步骤2")
    allure.attach("步骤2日志", "这是步骤2的详细日志信息", allure.attachment_type.TEXT)

    assert True, "测试成功完成"


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
        assert False, f"测试失败，原因: {e}"


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

    assert False, "带有截图附件的测试成功"


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

    assert False, "带有视频附件的测试成功"


@allure.feature("综合测试")
@allure.story("完整流程")
def test_complete_workflow():
    """测试完整的工作流程，包含多个步骤和附件"""
    allure.step("初始化测试环境")
    allure.attach("环境信息", "操作系统: Windows 10, Python版本: 3.10", allure.attachment_type.TEXT)

    allure.step("执行核心功能测试")
    allure.attach("功能测试日志", "核心功能执行成功", allure.attachment_type.TEXT)

    # 添加截图附件
    screenshot_path = os.path.join(temp_dir, "workflow_screenshot.png")
    with open(screenshot_path, "wb") as f:
        f.write(
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x90\x91\xb6\x5b\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\x09pHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xe5\x0c\x15\x09\x11\x16\x12\xe8\x94y\x00\x00\x00\x19tEXtComment\x00Created with Python\xca\xe4\x95\xa3\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xcc\x59\xe7\x00\x00\x00\x00IEND\xaeB`\x82')

    with open(screenshot_path, 'rb') as f:
        allure.attach(f.read(), name="工作流程截图", attachment_type=allure.attachment_type.PNG)

    allure.step("验证测试结果")
    allure.attach("验证日志", "所有步骤执行成功，结果符合预期", allure.attachment_type.TEXT)

    assert True, "完整工作流程测试成功完成"


@allure.feature("性能测试")
@allure.story("响应时间")
def test_performance_check():
    """测试性能指标"""
    import time

    allure.step("测量响应时间")
    start_time = time.time()

    # 模拟耗时操作
    time.sleep(0.1)

    end_time = time.time()
    response_time = end_time - start_time

    allure.attach("响应时间", f"执行耗时: {response_time:.4f}秒", allure.attachment_type.TEXT)
    allure.attach("性能指标", "响应时间在可接受范围内", allure.attachment_type.TEXT)

    assert response_time < 1.0, f"响应时间过长: {response_time:.4f}秒"
