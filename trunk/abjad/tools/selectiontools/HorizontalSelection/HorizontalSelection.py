from abjad.tools.selectiontools.Selection import Selection


class HorizontalSelection(Selection):
    '''Selection of components taken horizontally.

    Horizontal selections implement duration properties.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        '''Duration of components in selection.

        Return duration.
        '''
        return sum(component.duration for component in self)

    @property
    def duration_in_seconds(self):
        '''Duration in seconds of components in selection.

        Return duration.
        '''
        return sum(component.duration_in_seconds for component in self)

    @property
    def preprolated_duration(self):
        '''Preprolated duration of components in selection.

        Return duration.
        '''
        return sum(component.preprolated_duration for component in self)

    @property
    def timespan(self):
        '''Timespan of selection.
        '''
        from abjad.tools import timespantools
        start_offset = min(x.timespan.start_offset for x in self)
        stop_offset = max(x.timespan.stop_offset for x in self)
        return timespantools.Timespan(start_offset, stop_offset)

