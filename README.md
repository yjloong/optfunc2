# Call function directly in cmd line

#### Features
1. Allow user call functions directly in command line.
2. Generate help tips automatically.

#### TODO
1. Support class's function with self as the first argument.

#### Code example
``` python
#!/bin/bash
from autocall import *

# The tar @cmdline is used to register the function.
@cmdline
def test1():
	pass
    
@cmdline
def test2(arg):
	pass
    
@cmdline
def test3(arg1, arg2: str = 'this is a string'):
	print(arg2)
    
@cmdline
def test4(arg1, arg2: int):
	'You can add some extra information here.'
	pass
    
# main function
parse_and_run()
```
#### Run the code
``` bash
$ ./main.py --help
Help Tips Provided by Autocall.
  option:
    --test1
    
    --test2     arg
    
    --test3     arg1  [arg2 = this is a string]
    
    --test4     arg1  arg2
	            You can add some extra information here.
    
    --help      [verbose = notverbose]
    		    Give the argument "verbose" instead of "notverbose" to print detail information.
    
$ ./main.py --help verbose
Help Tips Provided by Autocall.
  option:
    --test1
    
    --test2     arg
    
    --test3     arg1  [arg2(str) = this is a string]
    
    --test4     arg1  arg2(int)
	            You can add some extra information here.
    
    --help      [verbose(str) = notverbose]
    		    Give the argument "verbose" instead of "notverbose" to print detail information.

$ # call function test3 and pass arguments arg1=1
$ ./main.py --test3 1
this is a string

$ # call function test3 and pass arguments arg1=1, arg2="this will be showed."     
$ ./main.py --test3 1 "this will be showed."
this will be showed.
```
