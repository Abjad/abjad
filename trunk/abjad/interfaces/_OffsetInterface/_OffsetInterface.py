from abjad.interfaces._Interface import _Interface


class _OffsetInterface(_Interface):

    ### CLASS ATTRIBUTES ###

    #__slots__ = ('_start', '_start_in_seconds', '_stop', '_stop_in_seconds')
    __slots__ = ('_start', '_start_in_seconds', '_stop')

    ### INITIALIZER ###

    def __init__(self, _client):
        _Interface.__init__(self, _client)
        self._start = None
        self._start_in_seconds = None
        self._stop = None
        #self._stop_in_seconds = None

    ### PRIVATE PROPERTIES ###

    @property
    def _component(self):
        return self._client

    ### PUBLIC PROPERTIES ###

    @property
    def start(self):
        self._component._update_prolated_offset_values_of_entire_score_tree_if_necessary()
        return self._start

    @property
    def stop(self):
#      #return self.start + self._client.prolated_duration
#      self._component._update_entire_score_tree_if_necessary()
#      return self._stop
        return self.start + self._client.prolated_duration

    @property
    def start_in_seconds(self):
#      return self._start_in_seconds
        self._component._update_marks_of_entire_score_tree_if_necessary()
        if self._start_in_seconds is None:
            raise MissingTempoError
        return self._start_in_seconds
