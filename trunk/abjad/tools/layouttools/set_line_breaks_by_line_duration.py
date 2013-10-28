# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools import marktools
from abjad.tools import measuretools
from abjad.tools.scoretools import attach


# TODO: make public and possibly improve function name
def set_line_breaks_by_line_duration(
    expr,
    line_duration,
    line_break_class=None,
    kind='prolated',
    adjust_eol=False,
    add_empty_bars=False,
    ):
    r'''Iterate `line_break_class` instances in `expr` 
    and accumulate `kind` duration.

    Add line break after every total less than or equal to `line_duration`.

    Set `line_break_class` to measure when `line_break_class` is none.
    '''

    if line_break_class is None:
        line_break_class = measuretools.Measure

    prev = None
    cum_duration = durationtools.Duration(0)
    for cur in iterationtools.iterate_components_in_expr(
        expr, line_break_class):
        # compress these 4 lines to only the 4th line after duration migration
        if kind == 'seconds':
            current_duration = cur._get_duration(in_seconds=True)
        elif kind == 'prolated':
            current_duration = cur._get_duration()
        elif kind == 'preprolated':
            current_duration = cur._preprolated_duration
        else:
            current_duration = getattr(cur._get_duration(), kind)
        candidate_duration = cum_duration + current_duration
        if candidate_duration < line_duration:
            cum_duration += current_duration
        elif candidate_duration == line_duration:
            command = marktools.LilyPondCommandMark('break', 'closing')
            attach(command, cur)
            if adjust_eol:
                marktools.LilyPondCommandMark(
                    'adjustEOLTimeSignatureBarlineExtraOffset',
                    'closing')(cur)
            if add_empty_bars:
                if cur.bar_line.kind is None:
                    cur.bar_line.kind = ''
            cum_duration = durationtools.Duration(0)
        else:
            if prev is not None:
                command = marktools.LilyPondCommandMark('break', 'closing')
                attach(command, prev)
                if adjust_eol:
                    marktools.LilyPondCommandMark(
                        'adjustEOLTimeSignatureBarlineExtraOffset',
                        'closing')(prev)
                if add_empty_bars:
                    if cur.bar_line.kind is None:
                        cur.bar_line.kind = ''
            cum_duration = current_duration
        prev = cur
