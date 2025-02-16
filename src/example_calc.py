from optfunc2 import cmdline, cmdline_default, cmdline_start

@cmdline_default
def add(a: float, b: float):
    """add two numbers

    Args:
        a (float): The First number
        b (float): The Second number
    """
    print(f"{a} + {b} = {a + b}")

@cmdline
def multiply(x: int|float, y: int = 5):
    """multiply two numbers. The second number is optional.

    Args:
        x (int): The First number
        y (int, optional): The Second number. Defaults to 5.
    """
    print(f"{x} × {y} = {x * y}")

@cmdline
def stats(numbers: list):
    """statistics of numbers in list

    Args:
        numbers (list): Target List.
    """ 
    print(f"sum: {sum(numbers)}")
    print(f"average: {sum(numbers)/len(numbers):.2f}")

if __name__ == "__main__":
    cmdline_start(header_doc="✨ calc CLI", has_abbrev=True)