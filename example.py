from hysys_wait import wait_for_spreadsheet_cells


def read_results(simulation):
    """
    Enable the HYSYS solver and wait until the selected spreadsheet
    cells contain valid numeric results.
    """

    cells_to_check = [
        ("Results", "A1"),
        ("Results", "A2"),
        ("Constraints", "B1"),
    ]

    simulation.Solver.CanSolve = True

    results_ready = wait_for_spreadsheet_cells(
        simulation=simulation,
        cells=cells_to_check,
        timeout=40.0,
        polling_interval=0.5,
    )

    if not results_ready:
        raise TimeoutError(
            "HYSYS spreadsheet results were not updated "
            "within the specified time limit."
        )

    result = (
        simulation.Flowsheet.Operations
        .Item("Results")
        .Cell("A1")
        .CellValue
    )

    return result
