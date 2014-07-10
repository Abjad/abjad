# -*- encoding: utf-8 -*-
from abjad import *


sargasso_measures = selectiontools.ContiguousSelection(
    (
        scoretools.Measure(
            indicatortools.TimeSignature((4, 16)),
            "c'16 c'16 c'8",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((2, 10)),
            "c'8 c'8",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((3, 20)),
            "c'8 c'16",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((4, 16)),
            "c'8. c'16",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((4, 16)),
            "c'8. c'16",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((11, 30)),
            "c'16 c'16 c'8 c'8. c'4",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((15, 30)),
            "c'8 c'16 c'8 c'8. c'4 c'16 c'16 c'16",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((2, 8)),
            "c'8 c'8",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((10, 26)),
            "c'8 c'8. c'4 c'16",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((4, 30)),
            "c'16 c'16 c'16 c'16",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((15, 30)),
            "c'16 c'4 c'16 c'16 c'8 c'8. c'16 c'8",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((7, 26)),
            "c'16 c'4 c'16 c'16",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((3, 26)),
            "c'16 c'16 c'16",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((1, 4)),
            "c'4",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((10, 19)),
            "c'8. c'4 c'16 c'16 c'16",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((6, 26)),
            "c'16 c'16 c'4",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((6, 20)),
            "c'4 c'16 c'16",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((2, 20)),
            "c'16 c'16",
            implicit_scaling=True,
            ),
        scoretools.Measure(
            indicatortools.TimeSignature((9, 19)),
            "c'16 c'4 c'16 c'16 c'8",
            implicit_scaling=True,
            ),
        )
    )