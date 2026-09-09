# HYSYS Spreadsheet Wait

A small Python utility for waiting until Aspen HYSYS spreadsheet results
are available through the COM interface.

## Why is this necessary?

When the HYSYS solver is enabled through COM automation, Python may continue
executing before the spreadsheet operations have finished updating.

As a result, reading spreadsheet cells immediately after enabling the solver
may return empty or temporarily unavailable values.

This utility periodically checks a configurable collection of cells. Execution
continues only when all selected cells contain valid numeric values or when a
timeout is reached.

## Why this can be mistaken for a convergence failure

This issue becomes more noticeable when multiple simulations are executed in
sequence, such as during optimization, sensitivity analysis, or parameter
studies.

A simulation may converge successfully while its spreadsheet operations are
still being updated. If Python attempts to read the results during this short
interval, the selected cells may still be empty or temporarily unavailable.

Empty values can then cause exceptions during numeric conversion, comparisons,
or subsequent calculations. This may look like a convergence failure even
though the HYSYS solver has already completed the calculation successfully.

In other words, solver convergence and spreadsheet result availability are
related but separate events:

1. HYSYS solves the simulation.
2. HYSYS updates the spreadsheet operations.
3. Python reads the updated results.

This utility synchronizes steps 2 and 3 by waiting until the selected cells
contain valid numeric values.

## Important distinction

This is a result-readiness check, not a complete mathematical convergence test.

The function confirms that the selected spreadsheet results are available.
Depending on the simulation, additional checks may be required to confirm that
every operation has converged successfully.

A successful result-readiness check means that the selected cells contain
numeric values. It does not guarantee that every unit operation or internal
solver in the simulation has reached a valid converged state.

## Usage

```python
from hysys_wait import wait_for_spreadsheet_cells


cells_to_check = [
    ("Results", "A1"),
    ("Results", "A2"),
    ("Constraints", "B1"),
]

simulation.Solver.CanSolve = True

results_ready = wait_for_spreadsheet_cells(
    simulation,
    cells_to_check,
    timeout=40.0,
    polling_interval=0.5,
)

if not results_ready:
    raise TimeoutError("HYSYS results were not ready before the timeout.")

# The selected spreadsheet cells are now available.
```

## How it works

1. The HYSYS solver is enabled.
2. Python checks the selected spreadsheet cells.
3. Empty, unavailable, non-numeric, or non-finite values are rejected.
4. The cells are checked again after a short interval.
5. The function returns `True` as soon as all selected cells are ready.
6. The function returns `False` if the timeout is reached.

The timeout is a maximum waiting time, not a fixed delay. The function returns
immediately when all selected cells contain valid numeric values.

For example, with a 40-second timeout, if all cells become ready after 5
seconds, execution continues after approximately 5 seconds. The remaining 35
seconds are not awaited.

The `polling_interval` controls how often the cells are checked. For example,
a polling interval of `0.5` seconds means that the function checks the cells
approximately twice per second.

## Customization

Replace the example spreadsheet names and cell addresses with references from
your own simulation:

```python
cells_to_check = [
    ("SpreadsheetName", "A1"),
    ("SpreadsheetName", "B2"),
]
```

You can also change the maximum waiting time and polling interval:

```python
wait_for_spreadsheet_cells(
    simulation,
    cells_to_check,
    timeout=60.0,
    polling_interval=1.0,
)
```

Choose cells that are expected to contain numeric results only after the
relevant part of the simulation has been calculated.

## Disclaimer

This project is an independent utility and is not affiliated with, endorsed
by, or maintained by Aspen Technology.

Aspen HYSYS is a trademark of Aspen Technology, Inc.

## License

This project is available under the MIT License.
