# Call function directly in cmd line

#### Features
1. Allow user call functions directly in command line.
2. Generate help tips automatically.
3. Add default called functions if not function was specific.

#### Notice
1. It's better to add argument type for each autocall functions.
2. Function with @optfunc_default has @optfunc implicitly.
3. Arguments of function with @optfunc_default should be optional or no argument.
4. Not support two type of variadic arguments.

#### TODO
1. Beautiful print.

#### Code example
``` python
from optfunc import *

@optfunc
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

@optfunc
def arg_test_positional_or_keyword(pos_or_kw, pos_or_kw1: int, pos_or_kw2 = 3, pos_or_kw3: int = 4):
    " Argument test for positional-or-keyword arguments. "
    print(f'pos_or_kw: {pos_or_kw}, pos_or_kw1: {pos_or_kw1}, pos_or_kw2: {pos_or_kw2}, pos_or_kw3: {pos_or_kw3}')
    pass

@optfunc
def arg_test_kw_only(*, kw_only0, kw_only1: int, kw_only2 = 9, kw_only3: int = 10):
    " Argument test for keyword-only arguments. "
    print(f'kw_only0: {kw_only0}, kw_only1: {kw_only1}, kw_only2: {kw_only2}, kw_only3: {kw_only3}')
    pass

if __name__ == '__main__':
    optfunc_start(globals=globals(), has_abbrev=False, header_doc='This is a test file for the module "autocall".')
```
#### Run the code
``` bash
~/:$ python3 test.py -h
Usage: test.py [command] [<args>|--help]

This is a test file for the module "autocall".

commands:
    arg_test_positional_only           summary for the function
    arg_test_positional_or_keyword     Argument test for positional-or-keyword arguments.
    arg_test_kw_only                   Argument test for keyword-only arguments.

~/:$ python3 test.py arg_test_positional_only -h
Usage: test.py arg_test_positional_only [OPTIONS]

summary for the function


Arguments:
+-------------+------+---------+-------------------------------------------------------------+
|     Opt     | Type | Default |                             Desc                            |
+-------------+------+---------+-------------------------------------------------------------+
| --pos_only0 | any  |         |         This is the first positional-only argument.         |
| --pos_only1 | int  |         |         This is the second positional-only argument.        |
| --pos_only2 | any  |    5    |  This is the third positional-only argument. Defaults to 5. |
| --pos_only3 | int  |    6    | This is the fourth positional-only argument. Defaults to 6. |
+-------------+------+---------+-------------------------------------------------------------+
~/:$ python3 test.py arg_test_positional_only --pos_only0 "good day" --pos_only1 2
pos_only0: good day, pos_only1: 2, pos_only2: 5, pos_only3: 6
```
