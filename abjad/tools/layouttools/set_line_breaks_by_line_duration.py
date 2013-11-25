# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


# TODO: replace kind='prolated' keyword with in_seconds=False keyword
def set_line_breaks_by_line_duration(
    expr,
    line_duration,
    line_break_class=None,
    kind='prolated',
    add_empty_bars=False,
    ):
    r'''Iterate `line_break_class` instances in `expr` 
    and accumulate `kind` duration.

    Add line break after every total less than or equal to `line_duration`.

    Set `line_break_class` to measure when `line_break_class` is none.
    '''

    if line_break_class is None:
        line_break_class = scoretools.Measure

    previous = None
    cumulative_duration = durationtools.Duration(0)
    for current in iterate(expr).by_class(line_break_class):
        # TODO: compress these 4 lines to only the 4th line 
        #       after duration migration
        if kind == 'seconds':
            current_duration = current._get_duration(in_seconds=True)
        elif kind == 'prolated':
            current_duration = current._get_duration()
        elif kind == 'preprolated':
            current_duration = current._preprolated_duration
        else:
            current_duration = getattr(current._get_duration(), kind)
        candidate_duration = cumulative_duration + current_duration
        if candidate_duration < line_duration:
            cumulative_duration += current_duration
        elif candidate_duration == line_duration:
            command = indicatortools.LilyPondCommand('break', 'closing')
            attach(command, current)
            if add_empty_bars:
                if current.bar_line.kind is None:
                    current.bar_line.kind = ''
            cumulative_duration = durationtools.Duration(0)
        else:
            if previous is not None:
                command = indicatortools.LilyPondCommand('break', 'closing')
                attach(command, previous)
                if add_empty_bars:
                    if current.bar_line.kind is None:
                        current.bar_line.kind = ''
            cumulative_duration = current_duration
        previous = current
