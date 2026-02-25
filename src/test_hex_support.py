import sys
from io import StringIO
from optfunc2 import cmdline, cmdline_start
import pytest

def capture_output(argv, globals=None, locals=None):
    """捕获命令行输出"""
    origin_stdout = sys.stdout
    origin_stderr = sys.stderr
    sys.stdout = StringIO()
    sys.stderr = StringIO()
    try:
        res = ''
        output = cmdline_start(globals=globals, argv=argv, locals=locals)
        stdout = sys.stdout.getvalue()
        stderr = sys.stderr.getvalue()
        
        if output:
            res = output
        if stdout:
            res += stdout
        if stderr:
            res += stderr
        
        return res
    finally:
        sys.stdout = origin_stdout
        sys.stderr = origin_stderr

# 测试十六进制支持的命令
@cmdline
def hex_test(number: int):
    """测试十六进制数字转换
    Args:
        number: 整数参数（支持十进制和十六进制）
    """
    return f"Number: {number} (decimal), Hex: {hex(number)}"

@cmdline
def hex_math(a: int, b: int):
    """十六进制数学运算
    Args:
        a: 第一个数字
        b: 第二个数字
    """
    result = a + b
    return f"{a} + {b} = {result} (0x{result:x})"

@cmdline
def mixed_types(value: int|float):
    """混合类型测试
    Args:
        value: 数字值（支持int和float）
    """
    return f"Value: {value}, Type: {type(value).__name__}"

class TestHexSupport:
    """测试十六进制格式支持"""
    
    def test_decimal_input(self):
        """测试十进制输入"""
        output = capture_output(["test_hex_support.py", "hex_test", "--number", "42"], globals())
        assert "Number: 42 (decimal)" in output
        assert "Hex: 0x2a" in output

    def test_hex_lowercase_input(self):
        """测试小写十六进制输入"""
        output = capture_output(["test_hex_support.py", "hex_test", "--number", "0x2a"], globals())
        assert "Number: 42 (decimal)" in output
        assert "Hex: 0x2a" in output

    def test_hex_uppercase_input(self):
        """测试大写十六进制输入"""
        output = capture_output(["test_hex_support.py", "hex_test", "--number", "0X2A"], globals())
        assert "Number: 42 (decimal)" in output
        assert "Hex: 0x2a" in output

    def test_hex_zero_input(self):
        """测试十六进制零值"""
        output = capture_output(["test_hex_support.py", "hex_test", "--number", "0x0"], globals())
        assert "Number: 0 (decimal)" in output
        assert "Hex: 0x0" in output

    def test_hex_large_number(self):
        """测试大数值的十六进制"""
        output = capture_output(["test_hex_support.py", "hex_test", "--number", "0xFFFF"], globals())
        assert "Number: 65535 (decimal)" in output
        assert "Hex: 0xffff" in output

    def test_hex_math_operations(self):
        """测试十六进制数学运算"""
        output = capture_output([
            "test_hex_support.py", "hex_math", 
            "--a", "0x10", "--b", "0x20"
        ], globals())
        assert "16 + 32 = 48 (0x30)" in output

    def test_mixed_decimal_hex_math(self):
        """测试十进制和十六进制混合运算"""
        output = capture_output([
            "test_hex_support.py", "hex_math", 
            "--a", "10", "--b", "0xF"
        ], globals())
        assert "10 + 15 = 25 (0x19)" in output

    def test_union_type_with_hex(self):
        """测试联合类型中的十六进制支持"""
        # 测试int分支
        output = capture_output([
            "test_hex_support.py", "mixed_types", 
            "--value", "0xFF"
        ], globals())
        assert "Value: 255" in output
        assert "Type: int" in output

    def test_invalid_hex_format(self):
        """测试无效的十六进制格式"""
        with pytest.raises(ValueError) as excinfo:
            capture_output([
                "test_hex_support.py", "hex_test", 
                "--number", "0xGG"  # 无效的十六进制字符
            ], globals())
        assert "should be int" in str(excinfo.value).lower()

if __name__ == "__main__":
    pytest.main(["-v", __file__])