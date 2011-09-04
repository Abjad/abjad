from abjad.exceptions import MissingTempoError
from abjad.interfaces._Interface import _Interface
from abjad.tools import durationtools


class _OffsetInterface(_Interface):
    '''Offset interface.
    '''

    __slots__ = ('_start', '_start_in_seconds', '_stop', '_stop_in_seconds')

    def __init__(self, _client):
        _Interface.__init__(self, _client)
        self._start = None
        self._start_in_seconds = None
        self._stop = None
        self._stop_in_seconds = None

    ### PRIVATE ATTRIBUTES ###

    @property
    def _component(self):
        return self._client

    ### PRIVATE METHODS ###

    def _update_offset_values_of_component_in_seconds(self):
        try:
            cur_duration_in_seconds = self._client.duration_in_seconds
            prev = self._client._navigator._prev
            if prev:
                self._start_in_seconds = prev._offset._stop_in_seconds
            else:
                #self._start_in_seconds = durationtools.Duration(0)
                self._start_in_seconds = durationtools.Offset(0)
            # this one case is possible for containers only
            if self._start_in_seconds is None:
                raise MissingTempoError
            self._stop_in_seconds = self._start_in_seconds + cur_duration_in_seconds
        except MissingTempoError:
            pass

    def _update_prolated_offset_values_of_component(self):
        prev = self._client._navigator._prev
        if prev:
            self._start = prev._offset._stop
        else:
            #self._start = durationtools.Duration(0)
            self._start = durationtools.Offset(0)
        self._stop = self._start + self._client.prolated_duration

    ### PUBLIC ATTRIBUTES ###

    @property
    def start(self):
#      return self._start
        self._component._update_prolated_offset_values_of_entire_score_tree_if_necessary( )
        return self._start

    @property
    def stop(self):
#      #return self.start + self._client.prolated_duration
#      self._component._update_entire_score_tree_if_necessary( )
#      return self._stop
        return self.start + self._client.prolated_duration

    @property
    def start_in_seconds(self):
#      return self._start_in_seconds
        self._component._update_marks_of_entire_score_tree_if_necessary( )
        if self._start_in_seconds is None:
            raise MissingTempoError
        return self._start_in_seconds

    @property
    def stop_in_seconds(self):
#      return self.start_in_seconds + self._client.duration_in_seconds
#      self._component._update_entire_score_tree_if_necessary( )
#      if self._stop_in_seconds is None:
#         raise MissingTempoError
#      return self._stop_in_seconds
        return self.start_in_seconds + self._client.duration_in_seconds
