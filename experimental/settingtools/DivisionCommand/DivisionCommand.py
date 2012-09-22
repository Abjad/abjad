import copy
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

    def fuse(self, command):
        '''Fuse `command` to the end of self.

        Return newly constructed division command.

        Raise exception when self can not fuse with `division_command`.
        '''
        assert self.can_fuse(command)
        stop_offset = self.stop_offset + command.duration
        segment_stop_offset = self.segment_stop_offset + command.duration
        duration = self.duration + command.duration
        fused_division_command = copy.deepcopy(self)
        fused_division_command._stop_offset = stop_offset
        fused_division_command._segment_stop_offset = segment_stop_offset
        fused_division_command._duration = duration
        fused_division_command._truncate = command.truncate
        return fused_division_command
