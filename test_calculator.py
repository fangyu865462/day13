from calculator import add,subtract
import pytest

def test_add():
    assert add(1,2) == 3
    assert add(2,3) ==5
def test_subtract():
    assert subtract(1,3) == -2

@pytest.fixture
def my_fixture():
    print("开始测试")
    yield
    print("测试结束")
@pytest.mark.parametrize("a,b,expected", [
    (1,2,3),(-1,1,0),(0,0,0)])
def test_add_parametrize(a,b,expected,my_fixture):
    assert add(a,b) == expected