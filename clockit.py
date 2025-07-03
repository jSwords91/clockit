from __future__ import annotations

import time
from typing import Callable, Optional


class clockit:
    """
    A minimal context manager for wall-clock timing.

    Parameters
    ----------
    name : str | None, default None
        Label for this timer. If given, the final read-out becomes
        e.g. ``"data-load: 0.537 s"``.
    printer : Callable[[str], None] | None, default None
        Callback that receives the read-out when the context exits.
        Pass ``print``, ``logger.info``, etc. If ``None`` nothing is
        printed automatically.

    Examples
    --------
    >>> with clockit("train-step") as ct:
    ...     time.sleep(1)
    ...
    >>> print(ct)
    train-step: 1.001 s

    >>> with clockit(printer=print) as ct:
    ...     time.sleep(0.5)
    ...
    0.501 s
    """

    def __init__(
        self,
        name: str | None = None,
        *,
        printer: Optional[Callable[[str], None]] = None,
    ) -> None:
        self.name = name
        self._printer = printer
        self.elapsed: float | None = None
        self.readout: str | None = None
        self._start: float | None = None

    def __enter__(self) -> "clockit":
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.elapsed = time.perf_counter() - self._start
        if self.name is not None:
            self.readout = f"{self.name}: {self.elapsed:.3f} seconds"
        else:
            self.readout = f"Time: {self.elapsed:.3f} seconds"
        if self._printer:
            self._printer(self.readout)
        return False

    def __str__(self) -> str:
        return self.readout or ""

    __repr__ = __str__
