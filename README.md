# optfunc2

> Auto-generate CLI from Python functions with type annotations and docstrings.

Turn any Python function into a CLI command — no argparse, no click, no boilerplate. Just add a decorator and your function's signature becomes the interface.

## Features

- **Zero boilerplate** — `@cmdline` decorator + type annotations = full CLI
- **Auto-generated help** — parsed from docstrings (Google style) and type hints
- **Type coercion** — `int`, `float`, `bool`, `str`, `list`, `dict`, `Union` types
- **Hex support** — `0x2A` input for integer arguments
- **Default command** — `@cmdline_default` for the "run with no args" experience
- **Shell abbreviations** — `-a value` as shortcut for `--arg value`

## Install

```bash
pip install optfunc2
```

## Quick Start

```python
from optfunc2 import cmdline, cmdline_default, cmdline_start

@cmdline_default
def add(a: float, b: float):
    """Add two numbers

    Args:
        a: The first number
        b: The second number
    """
    print(f"{a} + {b} = {a + b}")

@cmdline
def multiply(x: int | float, y: int = 5):
    """Multiply two numbers

    Args:
        x: The first number
        y: The second number (default 5)
    """
    print(f"{x} × {y} = {x * y}")

if __name__ == "__main__":
    cmdline_start(header_doc="✨ calc CLI", has_abbrev=True)
```

```bash
$ python calc.py add --a 2.3 --b 3        # 2.3 + 3.0 = 5.3
$ python calc.py add -a 2.3 -b 3           # abbreviation works too
$ python calc.py multiply --x 3            # 3 × 5 = 15
$ python calc.py                           # uses default command
$ python calc.py help                      # show all commands
$ python calc.py add -h                    # show command help
```

## How It Works

### Decorators

| Decorator | Description |
|---|---|
| `@cmdline` | Register a function as a CLI command |
| `@cmdline_default` | Same as above, but also the default when no command is given |

### Type Support

| Type | Input Example | Notes |
|---|---|---|
| `int` | `--n 42` or `--n 0x2A` | Hex format supported |
| `float` | `--r 3.14` | |
| `str` | `--name hello` | |
| `bool` | `--verbose` (no value needed) | |
| `list` | `--items '[1, 2, 3]'` | Parsed via `ast.literal_eval` |
| `dict` | `--cfg '{"key": "val"}'` | Parsed via `ast.literal_eval` |
| `int \| float` | `--x 3` or `--x 2.5` | Union types supported |

### Argument Styles

```bash
# All of these are equivalent:
python app.py my_cmd --name hello --count 3
python app.py my_cmd --name=hello --count=3
python app.py my_cmd -n hello -c 3        # abbreviations (when has_abbrev=True)
python app.py my_cmd -nhello -c3          # abbreviation + value combined
```

### `cmdline_start()` Options

```python
cmdline_start(
    header_doc="My App",      # Header text shown in help
    has_abbrev=True,          # Enable single-char abbreviation (-a for --arg)
    print_retval=False,       # Print return value to stdout
)
```

### `called_directly()`

Check if the current function was invoked by optfunc2 (vs. called by another function):

```python
@cmdline
def main():
    if called_directly():
        print("Called from CLI")
    else:
        print("Called from another function")
```

## Help Output

```bash
$ python calc.py help
Usage: calc.py [command] [<args>|--help]

✨ calc CLI

commands:
    add          [default] Add two numbers
    multiply     Multiply two numbers

$ python calc.py add -h
Usage: calc.py add [OPTIONS]

Add two numbers

Arguments:
+------+--------+-------+---------+------------------+
| Opt  | Abbrev |  Type | Default |      Desc       |
+------+--------+-------+---------+------------------+
| --a  |   -a   | float |         | The first number |
| --b  |   -b   | float |         | The second number|
+------+--------+-------+---------+------------------+
```

## Real-World Example

```python
from optfunc2 import cmdline, cmdline_default, cmdline_start
import os

@cmdline_default
def list_files(directory: str = ".", show_size: bool = False):
    """List files in a directory

    Args:
        directory: Target directory (default ".")
        show_size: Show file size in bytes
    """
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if show_size and os.path.isfile(path):
            print(f"{f} ({os.path.getsize(path)} bytes)")
        else:
            print(f)

if __name__ == "__main__":
    cmdline_start(header_doc="📁 file manager", has_abbrev=True)
```

## Limitations

- Variadic arguments (`*args`, `**kwargs`) are not supported
- Abbreviation conflicts (e.g., `text` and `test` both want `-t`) are resolved silently — first one wins
- Negative numbers as values require `--arg=-1` syntax (not `--arg -1`)

## License

PyPA License — see [LICENSE.txt](LICENSE.txt)
