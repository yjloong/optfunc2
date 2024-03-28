
# Table of Contents

1.  [Call function directly in cmd line](#org214ef56)


<a id="org214ef56"></a>

# Call function directly in cmd line

[Python Logo](https:www.python.org/static/community_logos/python-logo.png)

    from autocall import *
    
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

