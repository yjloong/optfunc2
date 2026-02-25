#!/usr/bin/env python3
"""
十六进制转换器示例
演示optfunc2对十六进制格式命令行参数的支持
"""

from optfunc2 import cmdline, cmdline_default, cmdline_start

@cmdline_default
def convert(number: int):
    """将数字转换为不同进制格式
    支持十进制和十六进制输入
    
    Args:
        number: 输入的数字（可以是十进制如42或十六进制如0x2A）
    """
    print(f"输入数字: {number}")
    print(f"十进制: {number}")
    print(f"十六进制: {hex(number)}")
    print(f"八进制: {oct(number)}")
    print(f"二进制: {bin(number)}")

@cmdline
def add_hex(a: int, b: int):
    """十六进制加法计算器
    
    Args:
        a: 第一个数字（支持十进制和十六进制）
        b: 第二个数字（支持十进制和十六进制）
    """
    result = a + b
    print(f"计算: {a} + {b} = {result}")
    print(f"十六进制结果: 0x{result:x}")
    print(f"二进制结果: 0b{result:b}")

@cmdline
def bitwise_ops(x: int, y: int):
    """位运算操作演示
    
    Args:
        x: 第一个数字
        y: 第二个数字
    """
    print(f"数字1: {x} (0x{x:x})")
    print(f"数字2: {y} (0x{y:x})")
    print(f"按位与: {x & y} (0x{x & y:x})")
    print(f"按位或: {x | y} (0x{x | y:x})")
    print(f"按位异或: {x ^ y} (0x{x ^ y:x})")
    print(f"左移2位: {x << 2} (0x{x << 2:x})")
    print(f"右移1位: {x >> 1} (0x{x >> 1:x})")

@cmdline
def memory_address(addr: int, size: int = 1):
    """内存地址计算工具
    
    Args:
        addr: 内存起始地址（通常用十六进制表示）
        size: 数据大小（字节）
    """
    end_addr = addr + size - 1
    print(f"起始地址: 0x{addr:x}")
    print(f"结束地址: 0x{end_addr:x}")
    print(f"大小: {size} 字节")
    print(f"地址范围: 0x{addr:x} - 0x{end_addr:x}")

if __name__ == "__main__":
    cmdline_start(
        header_doc="""🔧 十六进制转换器
支持十进制和十六进制格式的命令行参数输入
示例用法:
  python example_hex_converter.py 42          # 十进制输入
  python example_hex_converter.py 0x2A        # 十六进制输入
  python example_hex_converter.py add_hex --a 0x10 --b 0x20
""",
        has_abbrev=True
    )