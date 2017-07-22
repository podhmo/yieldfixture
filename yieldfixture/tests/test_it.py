import os.path
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
        with _capture() as buf:
            with open(os.path.join(os.path.dirname(__file__), "../../examples/00simple.py")) as rf:
                exec(rf.read())

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
        with _capture() as buf:
            with open(os.path.join(os.path.dirname(__file__), "../../examples/01usecontext.py")
                      ) as rf:
                exec(rf.read())

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

    def test_it__with_exception(self):
        with _capture() as buf:
            with self.assertRaises(ZeroDivisionError):
                with open(
                    os.path.join(os.path.dirname(__file__), "../../examples/02withexception.py")
                ) as rf:
                    exec(rf.read())

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
