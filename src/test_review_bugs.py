"""
Code review bug regression tests for optfunc2.
Tests verify that previously reported bugs are now fixed.
Uses module-scoped isolation to avoid polluting other test files.
"""
import sys
from io import StringIO
from pathlib import Path

import pytest
import optfunc2.parser as parser_mod
from optfunc2 import cmdline, cmdline_start, called_directly


RCE_FLAG = "/tmp/optfunc2_test_rce_flag"


def reset_state():
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


# Save and restore global state around the entire module
@pytest.fixture(scope="module", autouse=True)
def isolate_parser_state():
    saved_funcs = list(parser_mod.registered_funcs)
    saved_default = parser_mod.registered_func_default
    saved_called = parser_mod._called_func
    yield
    parser_mod.registered_funcs.clear()
    parser_mod.registered_funcs.extend(saved_funcs)
    parser_mod.registered_func_default = saved_default
    parser_mod._called_func = saved_called


# -----------------------------------------------------------------------
# Bug 1 (FIXED): eval() RCE
# -----------------------------------------------------------------------
class TestEvalRCE:
    def setup_method(self):
        reset_state()
        Path(RCE_FLAG).unlink(missing_ok=True)
    def teardown_method(self):
        Path(RCE_FLAG).unlink(missing_ok=True)
        reset_state()

    def test_rce_no_longer_possible(self):
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
        assert not Path(RCE_FLAG).exists(), "RCE should be fixed"


# -----------------------------------------------------------------------
# Bug 2 (FIXED): called_directly() null guard
# -----------------------------------------------------------------------
class TestCalledDirectlyNull:
    def setup_method(self):
        reset_state()
    def teardown_method(self):
        reset_state()

    def test_called_directly_returns_false_when_not_started(self):
        assert called_directly() is False


# -----------------------------------------------------------------------
# Bug 3 (FIXED): UnionType support
# -----------------------------------------------------------------------
class TestUnionTypeHelpCrash:
    def setup_method(self):
        reset_state()
    def teardown_method(self):
        reset_state()

    def test_union_type_help_no_crash(self):
        @cmdline
        def uf(v: int | float):
            return v
        result, out, _ = capture_output(["prog", "uf", "--help"],
                                         globals_dict=globals(), locals_dict=locals())
        assert "int | float" in out

    def test_union_type_execution(self):
        @cmdline
        def add(x: int | float, y: int | float):
            return x + y
        result, _, _ = capture_output(["prog", "add", "--x", "3", "--y", "2.5"],
                                     globals_dict=globals(), locals_dict=locals())
        assert result == 5.5


# -----------------------------------------------------------------------
# Bug 4 (open): Negative number arg
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
        result, _, _ = capture_output(["prog", "nf", "--n=-1"],
                                     globals_dict=globals(), locals_dict=locals())
        assert result == -1


# -----------------------------------------------------------------------
# Bug 5 (open): Empty help crash
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
# Bug 6: dict annotation
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
        result, _, _ = capture_output(["prog", "df", "--d", '{"key": "value"}'],
                                     globals_dict=globals(), locals_dict=locals())
        assert result == {"key": "value"}
