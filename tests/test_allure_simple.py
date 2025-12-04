import allure


@allure.feature("简单功能")
def test_allure_simple_passed():
    """Allure test that passes"""
    allure.attach("Test log", "This is a simple log", allure.attachment_type.TEXT)
    assert True


@allure.feature("简单功能")
def test_allure_simple_failed():
    """Allure test that fails"""
    allure.attach("Test log", "This is a simple log for failed test", allure.attachment_type.TEXT)
    assert False, "This test intentionally fails"
