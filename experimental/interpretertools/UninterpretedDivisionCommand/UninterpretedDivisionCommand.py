import fractions
from experimental.interpretertools.DivisionCommand import DivisionCommand


class UninterpretedDivisionCommand(DivisionCommand):
    r'''.. versionadded:: 1.0

    Command indicating durated period of time over which a division payload will apply.

    Uninterpreted division commands appear relatively early in the process of interpretation.
    '''

    ### INITIALIZER ###

    def __init__(self, payload, start_segment_identifier, context_name, 
        segment_start_offset, segment_stop_offset, duration, fresh, truncate):
        DivisionCommand.__init__( self, payload, start_segment_identifier, context_name,
            segment_start_offset, segment_stop_offset, duration, fresh)
        assert isinstance(truncate, bool), repr(truncate)
        self._truncate = truncate

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def truncate(self):
        '''Not yet implemented.
        '''
        return self._truncate
