import io
import unittest
from unittest.mock import patch

from bracket_validator.validator import main, validate_brackets


class TestBracketValidator(unittest.TestCase):
    def test_valid_strings(self):
        validate_brackets("()")
        validate_brackets("<div><p>{ test }</p></div>")
        validate_brackets("(a + {b <c>})")

    def test_basic_invalid(self):
        with self.assertRaises(ValueError) as ctx:
            validate_brackets("(()", advanced=False)
        self.assertEqual(str(ctx.exception), "Дужки незбалансовані")

    def test_advanced_invalid_positions_and_highlight(self):
        sample = "<div><p>{ test }}</p</div>"
        with self.assertRaises(ValueError) as ctx:
            validate_brackets(sample, advanced=True)
        msg = str(ctx.exception)
        self.assertIn("Дужки незбалансовані на позиціях", msg)
        self.assertIn("^", msg)

    def test_cli_valid(self):
        with patch("builtins.input", return_value="(abc)"), patch(
            "sys.stdout", new_callable=io.StringIO
        ) as out:
            main()
        self.assertIn("Строка валідна", out.getvalue())

    def test_cli_invalid_raises(self):
        with patch("builtins.input", return_value="(()"), patch(
            "sys.stdout", new_callable=io.StringIO
        ):
            with self.assertRaises(ValueError):
                main()


if __name__ == "__main__":
    unittest.main()