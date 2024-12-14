#!/bin/python3
import sys
import os
# sys.path.append("Z:\\autocall\\src")
current_dir = os.path.dirname(os.path.realpath(__file__))
autocall_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, current_dir)
# print(sys.path)
# sys.path.append(autocall_dir)
# print(current_dir)
from autocall import *
import autocall

@cmdline
def arg_test_positional_only(pos_only0, pos_only1: int, pos_only2 = 5, pos_only3: int = 6):
    """summary for the function

    Args:
        pos_only0 (_type_): This is the first positional-only argument.
        pos_only1 (int): This is the second positional-only argument.
        pos_only2 (int, optional): This is the third positional-only argument. Defaults to 5.
        pos_only3 (int, optional): This is the fourth positional-only argument. Defaults to 6.
    """
    " Argument test for positional-only arguments. "
    print(f'pos_only0: {pos_only0}, pos_only1: {pos_only1}, pos_only2: {pos_only2}, pos_only3: {pos_only3}')
    pass

@cmdline
def arg_test_positional_or_keyword(pos_or_kw, pos_or_kw1: int, pos_or_kw2 = 3, pos_or_kw3: int = 4):
    " Argument test for positional-or-keyword arguments. "
    print(f'pos_or_kw: {pos_or_kw}, pos_or_kw1: {pos_or_kw1}, pos_or_kw2: {pos_or_kw2}, pos_or_kw3: {pos_or_kw3}')
    pass

@cmdline
def arg_test_kw_only(*, kw_only0, kw_only1: int, kw_only2 = 9, kw_only3: int = 10):
    " Argument test for keyword-only arguments. "
    print(f'kw_only0: {kw_only0}, kw_only1: {kw_only1}, kw_only2: {kw_only2}, kw_only3: {kw_only3}')
    pass

if __name__ == '__main__':
    cmdline_start(globals=globals(), has_abbrev=False, header_doc='This is a test file for the module "autocall".')
