import unittest
import time
from clockit import clockit
from typing import Callable, Optional

class TestClockit(unittest.TestCase):
    def test_elapsed_and_readout(self):
        """Elapsed time should be >0 and readout should be formatted."""
        with clockit() as ct:
            time.sleep(0.05)  # 50 ms
        self.assertIsNotNone(ct.elapsed)
        self.assertGreater(ct.elapsed, 0)
        self.assertTrue(ct.readout.startswith("Time: "))
        # Allow a generous ±30 ms tolerance
        self.assertAlmostEqual(ct.elapsed, 0.05, delta=0.03)

    def test_printer_callback_invoked(self):
        """Printer callable should be invoked exactly once with the readout."""
        messages = []
        with clockit(printer=messages.append):
            time.sleep(0.01)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0], messages[0].strip())  # no trailing newline
        self.assertTrue(messages[0].startswith("Time: "))

    def test_no_printer_no_output(self):
        """When printer is None, nothing should be added to an external list."""
        output = []
        with clockit():  # no printer
            time.sleep(0.01)
        self.assertEqual(output, [])  # still empty

    def test_str_and_repr(self):
        """__str__ and __repr__ should return the readout string."""
        with clockit() as ct:
            time.sleep(0.01)
        self.assertEqual(str(ct), ct.readout)
        self.assertEqual(repr(ct), ct.readout)

    def test_exception_propagation(self):
        """Exceptions inside the with-block must propagate (no swallowing)."""
        with self.assertRaises(ValueError):
            with clockit():
                raise ValueError("boom")


if __name__ == "__main__":
    unittest.main(argv=["ignored", "-v"], exit=False)
