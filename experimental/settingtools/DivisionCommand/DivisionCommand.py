from experimental.settingtools.Command import Command


class DivisionCommand(Command):
    r'''.. versionadded:: 1.0

    Command indicating durated period of time 
    to which an evaluated request will apply.
    '''

    ### INITIALIZER ###

    def __init__(self, request, context_name, 
        start_offset, stop_offset,
        start_segment_identifier, segment_start_offset, segment_stop_offset, 
        duration, 
        index=None, count=None, reverse=None, rotation=None, callback=None,
        fresh=None, truncate=None):
        Command.__init__(self, request, context_name, 
            start_offset, stop_offset,
            start_segment_identifier, segment_start_offset, segment_stop_offset, 
            duration, 
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            fresh=fresh)
        assert isinstance(truncate, (bool, type(None))), repr(truncate)
        self._truncate = truncate

    ## READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        return 'divisions'

    @property
    def truncate(self):
        return self._truncate

    ### PUBLIC METHODS ###

    def can_fuse(self, expr):
        '''True when self can fuse `expr` to the end of self. Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if self.truncate:
            return False
        if expr.fresh or expr.truncate:
            return False
        if expr.request != self.request:
            return False
        return True
