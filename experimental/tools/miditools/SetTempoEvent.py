# -*- encoding: utf-8 -*-
from experimental.tools.miditools.TrackEvent import TrackEvent


class SetTempoEvent(TrackEvent):
    r'''Set tempo event.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
       )

    ### INITIALIZER ###

    def __init__(
        self,
        delta_time=0,
        ):
        TrackEvent.__init__(
            self,
            delta_time=delta_time,
            )