from abjad.demos.ferneyhough.make_row_of_nested_tuplets import make_row_of_nested_tuplets


def make_rows_of_nested_tuplets(tuplet_duration, row_count, column_count):
    rows_of_nested_tuplets = []
    for n in range(row_count):
        outer_tuplet_proportions = (1, n + 1, 1)
        row_of_nested_tuplets = make_row_of_nested_tuplets(
            tuplet_duration, outer_tuplet_proportions, column_count)
        rows_of_nested_tuplets.append(row_of_nested_tuplets)
    return rows_of_nested_tuplets

