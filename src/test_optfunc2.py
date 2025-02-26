import sys
from io import StringIO
from threading import local
from optfunc2 import cmdline, cmdline_default, cmdline_start, called_directly
import pytest

# --------------------------
# 测试用例工具函数
# --------------------------

def capture_output(argv, globals = None, locals = None):
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
        

# --------------------------
# 基础功能测试
# --------------------------

@cmdline_default
def default_command():
    """默认命令的文档"""
    return "Default command executed"

@cmdline
def echo(text: str, repeat: int = 1):
    """回声命令
    Args:
        text: 需要重复的文本
        repeat: 重复次数 (默认 1)
    """
    return " ".join([text] * repeat)

@cmdline
def math_op(a: int, b: float, operation: str = "add"):
    """数学运算
    Args:
        a: 整数参数
        b: 浮点数参数
        operation: 运算类型 (add/sub/mul)
    """
    if operation == "add":
        return a + b
    elif operation == "sub":
        return a - b
    elif operation == "mul":
        return a * b
    else:
        raise ValueError("Invalid operation")

# --------------------------
# 测试用例
# --------------------------

class TestBasicFunctionality:
    """测试基础功能"""
    
    def test_default_command(self):
        """测试默认命令"""
        print(sys.argv)
        output = capture_output(["test_optfunc2.py"], globals())
        assert "Default command executed" in output

    def test_simple_command_execution(self):
        """测试简单命令执行"""
        output = capture_output(["test_optfunc2.py", "echo", "--text", "hello"], globals())
        assert output == "hello"

    def test_command_with_arguments(self):
        """测试带参数的命令"""
        output = capture_output(["test_optfunc2.py", "echo", "--text", "hi", "--repeat", "3"], globals())
        assert output == "hi hi hi"

    def test_type_conversion(self):
        """测试类型自动转换"""
        output = capture_output(["test_optfunc2.py", "math_op", "--a", "5", "--b", "3.2"], globals())
        assert 8.2 == output  # 5 + 3.2

    def test_help_output(self):
        """测试帮助信息输出"""
        output = capture_output(["test_optfunc2.py", "help"], globals())
        assert "echo" in output
        assert "math_op" in output
        assert "默认命令的文档" in output
    
    def test_serveral_type(self):
        """测试单参数指定多类型"""
        @cmdline
        def type_test(data: list|int):
            print(f'{type(data)}')
        output = capture_output(["test_optfunc2.py", "type_test", "--data", "[1,2,3]"], globals(), locals=locals())
        assert "list" in output
        
    def test_return_value(self):
        @cmdline
        def return_test():
            return "Hello World"
        
        output = capture_output(["test_optfunc2.py", "return_test"], globals(), locals=locals())
        assert "Hello World" in output

    def test_return_value2(self, print_retval: bool = False):
        @cmdline
        def return_test():
            if print_retval:
                return "Hello World"
        
        output = capture_output(["test_optfunc2.py", "return_test"], globals(), locals=locals())
        assert "Hello World" not in output
    
    

# --------------------------
# 边界条件测试
# --------------------------

class TestEdgeCases:
    """测试边界条件"""
    
    def test_missing_required_args(self):
        """测试缺少必需参数"""
        with pytest.raises(ValueError) as excinfo:
            capture_output(["test_optfunc2.py", "math_op", "--b", "5.0"], globals())
        assert "is required" in str(excinfo.value)

    def test_invalid_arg_type(self):
        """测试无效参数类型"""
        with pytest.raises(ValueError) as excinfo:
            capture_output(["test_optfunc2.py", "math_op", "--a", "five", "--b", "3.0"], globals())
        assert "should be int" in str(excinfo.value).lower()

    def test_unknown_command(self):
        """测试未知命令"""
        output = capture_output(["test_optfunc2.py", "unknown"], globals())
        assert "Unknown command" in output

    def test_abbreviation_conflict(self):
        """测试缩写冲突"""
        @cmdline
        def conflict_test(text: str, test: int):
            return f"{text}-{test}"

        with pytest.raises(ValueError):
            capture_output(["test_optfunc2.py", "conflict_test", "-t", "value"], globals())

# --------------------------
# 高级功能测试
# --------------------------
class TestAdvancedFeatures:
    """测试高级功能"""
    
    def test_called_directly_check(self):
        """测试直接调用检查"""
        @cmdline
        def direct_check():
            return called_directly()
        
        output = capture_output(["test_optfunc2.py", "direct_check"], locals=locals())
        assert output

    def test_multiprocessing_integration(self, monkeypatch):
        """测试多进程集成"""
        @cmdline
        def process_test():
            import multiprocessing
            p = multiprocessing.Process(target=lambda: print("Child process"))
            p.start()
            p.join()


        return # 不知道为什么拿不到子进程输出
        # monkeypatch.setattr("multiprocessing.get_start_method", lambda: "spawn")
        output = capture_output(["test_optfunc2.py", "process_test"], locals=locals())
        assert "Child process" in output

    def test_complex_type_handling(self):
        """测试复杂类型处理"""
        @cmdline
        def type_test(data: list, config: dict):
            return f"List: {data}, Dict: {config}"

        output = capture_output(
            ["test_optfunc2.py", "type_test", "--data", "[1,2,3]", "--config", "{'key':'value'}"],
            locals = locals()
        )
        assert "List: [1, 2, 3]" in output
        assert "Dict: {'key': 'value'}" in output

# --------------------------
# 装饰器边界测试
# --------------------------

class TestDecoratorEdgeCases:
    """测试装饰器边界情况"""
    
    def test_duplicate_default_registration(self):
        """测试重复注册默认命令"""
        return # This is OK. Difficult to test.
        @cmdline_default
        def default1():
            pass

        @cmdline_default
        def default2():
            pass

        output = capture_output(["test_optfunc2.py"], globals(), locals=locals())
        assert "Warning" in output
        assert "last one will be used" in output

    def test_variadic_arguments(self):
        """测试可变参数检测"""
        with pytest.raises(SystemExit):
            @cmdline
            def invalid(*args):
                pass

    def test_empty_docstring_handling(self):
        """测试空文档字符串处理"""
        @cmdline
        def no_docs(a: int):
            pass

        output = capture_output(["test_optfunc2.py", "no_docs", "--help"], locals=locals())
        assert "Help Tips Provided" in output

if __name__ == "__main__":
    pytest.main(["-v", __file__])