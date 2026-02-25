#!/bin/bash

echo "=== optfunc2 十六进制支持演示 ==="
echo

echo "1. 基本十六进制转换:"
python src/example_hex_converter.py convert --number 0xFF
echo

echo "2. 十进制与十六进制对比:"
echo "十进制输入:"
python src/example_hex_converter.py convert --number 255
echo "十六进制输入:"
python src/example_hex_converter.py convert --number 0xFF
echo

echo "3. 十六进制数学运算:"
python src/example_hex_converter.py add_hex --a 0x10 --b 0x20
echo

echo "4. 位运算演示:"
python src/example_hex_converter.py bitwise_ops --x 0xF0 --y 0x0F
echo

echo "5. 内存地址计算:"
python src/example_hex_converter.py memory_address --addr 0x1000 --size 16
echo

echo "6. 混合输入格式:"
python src/example_hex_converter.py add_hex --a 100 --b 0x64
echo

echo "演示完成!"
