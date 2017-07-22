import unittest
import textwrap
import contextlib


@contextlib.contextmanager
def _capture():
    from io import StringIO
    buf = StringIO()

    with contextlib.redirect_stdout(buf):
        yield buf


class Tests(unittest.TestCase):
    def test_it(self):
        from yieldfixture import create
        run, yield_fixture = create()

        @yield_fixture
        def f():
            print(">>> f")
            yield 1
            print(">>> f")

        @yield_fixture
        def g():
            print("  >>> g")
            yield 2
            print("  >>> g")

        with _capture() as buf:

            @run
            def use_it(x, y):
                print("{} + {} = {}".format(x, y, x + y))

        expected = textwrap.dedent(
            """
        >>> f
          >>> g
        1 + 2 = 3
          >>> g
        >>> f
        """
        )
        self.assertEqual(buf.getvalue().strip(), expected.strip())

    def test_it__with_context(self):
        from yieldfixture import create, with_context
        run, yield_fixture = create()

        @yield_fixture
        @with_context
        def f(ctx):
            i = ctx["i"] = 0
            print("{}>>> f".format("  " * i))
            yield 1
            print("{}>>> f".format("  " * i))

        @yield_fixture
        @with_context
        def g(ctx):
            i = ctx["i"] = ctx["i"] + 1
            print("{}>>> g".format("  " * i))
            yield 2
            print("{}>>> g".format("  " * i))

        with _capture() as buf:

            @run
            def use_it(x, y, *, i=0):
                print("{}{} + {} = {}".format("  " * (i + 1), x, y, x + y))

        expected = textwrap.dedent(
            """
        >>> f
          >>> g
            1 + 2 = 3
          >>> g
        >>> f
        """
        )
        self.assertEqual(buf.getvalue().strip(), expected.strip())
