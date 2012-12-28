import copy
from experimental.tools.settingtools.Command import Command


class DivisionCommand(Command):
    r'''

    Command indicating durated period of time 
    to which an evaluated request will apply.
    '''

    ### INITIALIZER ###

    def __init__(self, request, context_name, start_offset, stop_offset, 
        fresh=None, truncate=None):
        Command.__init__(self, request, context_name, start_offset, stop_offset, fresh=fresh)
        assert isinstance(truncate, (bool, type(None))), repr(truncate)
        self._truncate = truncate

    ## READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        return 'divisions'

    @property
    def truncate(self):
        return self._truncate

    @property
    def voice_name(self):
        '''Aliased to ``self.context_name``.
        '''
        return self.context_name

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
