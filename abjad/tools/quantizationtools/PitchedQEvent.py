# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools.quantizationtools.QEvent import QEvent


class PitchedQEvent(QEvent):
    r'''A ``QEvent`` which indicates the onset of a period of pitched material
    in a ``QEventSequence``:

    ::

        >>> pitches = [0, 1, 4]
        >>> q_event = quantizationtools.PitchedQEvent(1000, pitches)
        >>> q_event
        quantizationtools.PitchedQEvent(
            durationtools.Offset(1000, 1),
            (NamedPitch("c'"), NamedPitch("cs'"), NamedPitch("e'")),
            attachments=(),
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

    def __init__(self, offset, pitches, attachments=None, index=None):
        QEvent.__init__(self, offset, index=index)
        pitches = tuple([pitchtools.NamedPitch(x) for x in pitches])
        if attachments is None:
            attachments = ()
        else:
            attachments = tuple(attachments)
        self._pitches = pitches
        self._attachments = attachments

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(self) == type(expr) and \
            self.offset == expr.offset and \
            self.pitches == expr.pitches and \
            self.attachments == expr.attachments and \
            self.index == expr.index:
            return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats q-event.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        if format_specification in ('', 'storage'):
            return self._tools_package_qualified_indented_repr
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def attachments(self):
        return self._attachments

    @property
    def pitches(self):
        return self._pitches
