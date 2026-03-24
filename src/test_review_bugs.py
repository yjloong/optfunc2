"""
Code review bug regression tests for optfunc2.
Each test verifies a bug discovered during code review.
"""
import os
import sys
from io import StringIO
from pathlib import Path

import pytest
import optfunc2.parser as parser_mod
from optfunc2 import cmdline, cmdline_start, called_directly


RCE_FLAG = "/tmp/optfunc2_test_rce_flag"


def reset_state():
    """Reset global state between tests to avoid pollution."""
    parser_mod.registered_funcs.clear()
    parser_mod.registered_func_default = None
    parser_mod._called_func = None


def capture_output(argv, globals_dict=None, locals_dict=None):
    old_out, old_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = StringIO(), StringIO()
    try:
        result = cmdline_start(globals=globals_dict, argv=argv, locals=locals_dict)
        return result, sys.stdout.getvalue(), sys.stderr.getvalue()
    finally:
        sys.stdout, sys.stderr = old_out, old_err


# -----------------------------------------------------------------------
# Bug 1: eval() RCE — arbitrary code execution via __repr__
# -----------------------------------------------------------------------
class TestEvalRCE:
    def setup_method(self):
        reset_state()
        Path(RCE_FLAG).unlink(missing_ok=True)

    def teardown_method(self):
        Path(RCE_FLAG).unlink(missing_ok=True)
        reset_state()

    def test_rce_via_repr(self):
        """A type with malicious __repr__ gets eval'd, executing arbitrary code."""
        # Use a hardcoded path in repr (no self reference)
        class Evil:
            def __init__(self, v):
                self.v = v
            def __repr__(self):
                return "__import__('pathlib').Path('/tmp/optfunc2_test_rce_flag').write_text('pwned')"

        @cmdline
        def f(x: Evil):
            return x

        capture_output(["prog", "f", "--x", "anything"],
                       globals_dict=globals(), locals_dict=locals())
        assert Path(RCE_FLAG).exists(), "eval() executed arbitrary code via __repr__"


# -----------------------------------------------------------------------
# Bug 2: called_directly() crashes when _called_func is None
# -----------------------------------------------------------------------
class TestCalledDirectlyNull:
    def setup_method(self):
        reset_state()
    def teardown_method(self):
        reset_state()

    def test_called_directly_no_prior_start(self):
        with pytest.raises(AttributeError, match="NoneType.*__name__"):
            called_directly()


# -----------------------------------------------------------------------
# Bug 3: UnionType (int|float) has no __name__ — crashes --help
# -----------------------------------------------------------------------
class TestUnionTypeHelpCrash:
    def setup_method(self):
        reset_state()
    def teardown_method(self):
        reset_state()

    def test_union_type_help_raises(self):
        @cmdline
        def uf(v: int | float):
            return v
        with pytest.raises(AttributeError, match="UnionType.*__name__"):
            capture_output(["prog", "uf", "--help"],
                          globals_dict=globals(), locals_dict=locals())


# -----------------------------------------------------------------------
# Bug 4: Negative number argument parsed as new option
# -----------------------------------------------------------------------
class TestNegativeNumberArg:
    def setup_method(self):
        reset_state()
    def teardown_method(self):
        reset_state()

    def test_negative_int_rejected(self):
        @cmdline
        def nf(n: int):
            return n
        with pytest.raises(ValueError, match="Unknown argument -1"):
            capture_output(["prog", "nf", "--n", "-1"],
                          globals_dict=globals(), locals_dict=locals())

    def test_negative_int_via_equals(self):
        @cmdline
        def nf(n: int):
            return n
        result, *_ = capture_output(["prog", "nf", "--n=-1"],
                                   globals_dict=globals(), locals_dict=locals())
        assert result == -1


# -----------------------------------------------------------------------
# Bug 5: Empty registered_funcs causes help() to crash
# -----------------------------------------------------------------------
class TestEmptyHelpCrash:
    def setup_method(self):
        reset_state()
    def teardown_method(self):
        reset_state()

    def test_empty_registry_help_crash(self):
        with pytest.raises(ValueError, match="max.*iterable"):
            capture_output(["prog", "help"], globals_dict=globals())


# -----------------------------------------------------------------------
# Bug 6: dict annotation — behavior check
# -----------------------------------------------------------------------
class TestDictFallback:
    def setup_method(self):
        reset_state()
    def teardown_method(self):
        reset_state()

    def test_dict_invalid_string_raises(self):
        @cmdline
        def df(d: dict):
            return d
        with pytest.raises(ValueError, match="should be dict"):
            capture_output(["prog", "df", "--d", "abc"],
                          globals_dict=globals(), locals_dict=locals())

    def test_dict_valid_input_works(self):
        @cmdline
        def df(d: dict):
            return d
        result, *_ = capture_output(["prog", "df", "--d", '{"key": "value"}'],
                                   globals_dict=globals(), locals_dict=locals())
        assert result == {"key": "value"}


if __name__ == "__main__":
    pytest.main(["-v", __file__])
