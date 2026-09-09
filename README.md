# HYSYS Spreadsheet Wait

A small Python utility for waiting until Aspen HYSYS spreadsheet
results are available through the COM interface.

## Why is this necessary?

When the HYSYS solver is enabled through COM automation, Python may
continue executing before the spreadsheet operations have finished
updating.

As a result, reading spreadsheet cells immediately after enabling the
solver may return empty or temporarily unavailable values.

This utility periodically checks a configurable collection of cells.
Execution continues only when all selected cells contain valid numeric
values or when a timeout is reached.

## Important distinction

This is a result-readiness check, not a complete mathematical
convergence test.

The function confirms that the selected spreadsheet results are
available. Depending on the simulation, additional checks may be
required to confirm that every operation has converged successfully.

## Requirements

- Python 3
- Aspen HYSYS with COM automation available
- A HYSYS simulation containing spreadsheet operations

If Python is also responsible for opening and controlling HYSYS, the
`pywin32` package is commonly used to access the COM interface.

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

# It is now safe to read the selected results.
```

## How it works

1. The HYSYS solver is enabled.
2. Python checks the selected spreadsheet cells.
3. Empty, unavailable, non-numeric, or non-finite values are rejected.
4. The cells are checked again after a short interval.
5. The function returns `True` when all cells are ready.
6. It returns `False` if the timeout is reached.

## Customization

Replace the example spreadsheet names and cell addresses with references
from your own simulation:

```python
cells_to_check = [
    ("SpreadsheetName", "A1"),
    ("SpreadsheetName", "B2"),
]
```

You can also change the timeout and polling interval:

```python
wait_for_spreadsheet_cells(
    simulation,
    cells_to_check,
    timeout=60.0,
    polling_interval=1.0,
)
```

## Disclaimer

This project is an independent utility and is not affiliated with,
endorsed by, or maintained by Aspen Technology.

Aspen HYSYS is a trademark of Aspen Technology, Inc.

## License

This project is available under the MIT License.
