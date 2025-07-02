from __future__ import annotations

import time
from typing import Callable, Optional


class clockit:
    """
    A minimal context manager for wall-clock timing.

    Parameters
    ----------
    printer : Callable[[str], None] | None, default None
        Callable to receive the formatted read-out string.
        Use `print`, `logger.info`, `functools.partial(print, file=sys.stderr)`, etc.
        If None, no output is produced inside ``__exit__``.

    Examples
    --------
    >>> with clockit() as ct:
    ...     time.sleep(1)
    ...
    >>> print(ct)
    Time: 1.000 seconds

    >>> with clockit(printer=print) as ct:
    ...     time.sleep(1)
    ...
    Time: 1.000 seconds

    >>> with clockit(printer=logger.info) as ct:
    ...     time.sleep(1)
    ...
    """

    def __init__(self, *, printer: Optional[Callable[[str], None]] = None) -> None:
        self._printer = printer
        self.elapsed: float | None = None
        self.readout: str | None = None
        self._start: float | None = None

    def __enter__(self) -> "clockit":
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.elapsed = time.perf_counter() - self._start
        self.readout = f"Time: {self.elapsed:.3f} seconds"
        if self._printer:
            self._printer(self.readout)
        return False

    def __str__(self) -> str:
        return self.readout or ""

    __repr__ = __str__
