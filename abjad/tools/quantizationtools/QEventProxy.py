# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadObject


class QEventProxy(AbjadObject):
    r'''Proxies a `QEvent`, mapping that QEvent's offset with the range of
    its beatspan to the range 0-1.

    ::

        >>> q_event = quantizationtools.PitchedQEvent(130, [0, 1, 4])
        >>> proxy = quantizationtools.QEventProxy(q_event, 0.5)
        >>> print(format(proxy, 'storage'))
        quantizationtools.QEventProxy(
            quantizationtools.PitchedQEvent(
                offset=durationtools.Offset(130, 1),
                pitches=(
                    pitchtools.NamedPitch("c'"),
                    pitchtools.NamedPitch("cs'"),
                    pitchtools.NamedPitch("e'"),
                    ),
                ),
            durationtools.Offset(1, 2)
            )

    Not composer-safe.

    Used internally by ``Quantizer``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_offset',
        '_q_event',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import quantizationtools
        if len(args) == 2:
            q_event, offset = args[0], durationtools.Offset(args[1])
            assert isinstance(q_event, quantizationtools.QEvent)
            assert 0 <= offset <= 1
        elif len(args) == 3:
            q_event, minimum, maximum = args[0], \
                durationtools.Offset(args[1]), \
                durationtools.Offset(args[2])
            assert isinstance(q_event, quantizationtools.QEvent)
            assert minimum <= q_event.offset <= maximum
            offset = (q_event.offset - minimum) / (maximum - minimum)
        elif len(args) == 0:
            q_event = None
            offset = durationtools.Offset(0)
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, args)
            raise ValueError(message)
        self._q_event = q_event
        self._offset = durationtools.Offset(offset)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a q-event proxy with offset and q-event
        equal to those of this q-event proxy. Otherwise false.

        Returns true or false.
        '''
        if type(self) == type(expr):
            if self.offset == expr.offset:
                if self.q_event == expr.q_event:
                    return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats q-event.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __hash__(self):
        r'''Hashes q-event proxy.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(QEventProxy, self).__hash__()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = []
        if self.q_event:
            values.append(self.q_event)
        if self.offset:
            values.append(self.offset)
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def index(self):
        r'''Index of q-event proxy.
        '''
        return self._q_event.index

    @property
    def offset(self):
        r'''Offset of q-event proxy.
        '''
        return self._offset

    @property
    def q_event(self):
        r'''Q-event of q-event proxy.
        '''
        return self._q_event
