# -*- coding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools.quantizationtools.QEvent import QEvent


class PitchedQEvent(QEvent):
    r'''A ``QEvent`` which indicates the onset of a period of pitched material
    in a ``QEventSequence``.

    ::

        >>> pitches = [0, 1, 4]
        >>> q_event = quantizationtools.PitchedQEvent(1000, pitches)
        >>> print(format(q_event, 'storage'))
        quantizationtools.PitchedQEvent(
            offset=durationtools.Offset(1000, 1),
            pitches=(
                pitchtools.NamedPitch("c'"),
                pitchtools.NamedPitch("cs'"),
                pitchtools.NamedPitch("e'"),
                ),
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_attachments',
        '_index',
        '_offset',
        '_pitches',
        )

    ### INITIALIZER ###

    def __init__(self, offset=0, pitches=None, attachments=None, index=None):
        QEvent.__init__(self, offset=offset, index=index)
        pitches = pitches or []
        pitches = tuple([pitchtools.NamedPitch(x) for x in pitches])
        if attachments is None:
            attachments = ()
        else:
            attachments = tuple(attachments)
        self._pitches = pitches
        self._attachments = attachments

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a pitched q-event with offset, pitches,
        attachments and index equal to those of this pitched q-event. Otherwise
        false.

        Returns true or false.
        '''
        if type(self) == type(expr) and \
            self.offset == expr.offset and \
            self.pitches == expr.pitches and \
            self.attachments == expr.attachments and \
            self.index == expr.index:
            return True
        return False

    def __hash__(self):
        r'''Hashes pitched q-event.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(PitchedQEvent, self).__hash__()

    ### PUBLIC PROPERTIES ###

    @property
    def attachments(self):
        r'''Attachments of pitched q-event.
        '''
        return self._attachments

    @property
    def pitches(self):
        r'''Pitches of pitched q-event.
        '''
        return self._pitches
