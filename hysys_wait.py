"""Utilities for waiting until HYSYS spreadsheet results are ready."""

import math
import time
from typing import Sequence, Tuple


CellReference = Tuple[str, str]


def wait_for_spreadsheet_cells(
    simulation,
    cells: Sequence[CellReference],
    timeout: float = 40.0,
    polling_interval: float = 0.5,
) -> bool:
    """
    Wait until all specified HYSYS spreadsheet cells contain valid numbers.

    Parameters
    ----------
    simulation:
        A HYSYS simulation case exposed through the COM interface.

    cells:
        Spreadsheet and cell references in the following format:

        [
            ("Results", "A1"),
            ("Constraints", "B2"),
        ]

    timeout:
        Maximum waiting time, in seconds.

    polling_interval:
        Time between consecutive checks, in seconds.

    Returns
    -------
    bool
        True when all cells contain valid numeric values.
        False when the timeout is reached.
    """

    start_time = time.monotonic()

    while time.monotonic() - start_time < timeout:
        all_cells_ready = True

        for spreadsheet_name, cell_address in cells:
            try:
                value = (
                    simulation.Flowsheet.Operations
                    .Item(spreadsheet_name)
                    .Cell(cell_address)
                    .CellValue
                )

                if value is None or value == "":
                    all_cells_ready = False
                    break

                if not math.isfinite(float(value)):
                    all_cells_ready = False
                    break

            except Exception:
                # Cells may be temporarily unavailable while HYSYS
                # is recalculating the simulation.
                all_cells_ready = False
                break

        if all_cells_ready:
            return True

        time.sleep(polling_interval)

    return False
