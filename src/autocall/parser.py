#!/bin/python3
import inspect
import sys

__register_funcs = []

def cmdline(func):
    __register_funcs.append(func)
    globals()[func.__name__] = func
    return func

def parse_run(argv = sys.argv[1:]):
    __argv = []

    def str_to_any(_str, _type):
        if _type == int:
            return int(_str, 0)
        elif _type == str:
            return _str
        else:
            raise Exception("Don't know the type")

    def match_and_check(name):
        res = [f for f in __register_funcs if f.__name__ == name]
        if not res:
            raise Exception("Couldn't found function")

        #if len(getfullargspec(res[0]).args) != len(res[0].__annotations__):
            #raise Exception("Target function's arguments should have determinded types")

        return res[0]

    
    @cmdline
    def help(verbose :str = 'notverbose'):
        'Give the argument \"verbose\" instead of \"notverbose\" to print detail information.'
        print('Help Tips Provided by Autocall.')
        print('  option:')
        for func in __register_funcs:
            parameters = inspect.signature(func).parameters
            print(f'    --{func.__name__:<10s}', end='')
            for name in parameters:
                anno = parameters[name].annotation
                defa = parameters[name].default

                if anno != inspect._empty:
                    if type(anno) != type:
                        anno = f'({anno})'
                    else:
                        anno = f'({anno.__name__})'
                else:
                    anno = ''

                if verbose == 'notverbose':
                    anno = ''
                    
                if defa != inspect._empty:
                    defa = f'[{name}{anno} = {defa}]'
                else:
                    defa = f'{name}{anno}'
                
                print(f'{defa}  ', end='')
                
            print()
            if func.__doc__:
                print(f'                {func.__doc__:>20s}')
            print()

    
    # Parsing
    for arg in argv:
        if arg.startswith('--'):
            __argv.append([arg[2:]])
        elif arg.startswith('-'):
            __argv.append([arg[2:]])
        else:
            if not len(__argv):
                continue
            __argv[-1].append(arg)
    
    # Call function
    for item in __argv:
        name = item[0]
        func = match_and_check(name)
        args = inspect.getfullargspec(func).args
        anns = func.__annotations__

        arguments = ', '.join([(lambda argname, passvalue:
                          passvalue if anns.get(argname) != str
                          else f'\'{passvalue}\'')(k, v)
                         for k, v in zip(args, item[1:])])

        #print(globals())
        eval(f'{name}({arguments})')

        
