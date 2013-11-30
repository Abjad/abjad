# -*- encoding: utf-8 -*-
import inspect
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class QEventProxy(AbjadObject):
    r'''Proxies a `QEvent`, mapping that QEvent's offset with the range of 
    its beatspan to the range 0-1.

    ::

        >>> q_event = quantizationtools.PitchedQEvent(130, [0, 1, 4])
        >>> proxy = quantizationtools.QEventProxy(q_event, 0.5)
        >>> print format(proxy, 'storage')
        quantizationtools.QEventProxy(
            q_event=quantizationtools.PitchedQEvent(
                offset=durationtools.Offset(130, 1),
                pitches=(
                    pitchtools.NamedPitch("c'"),
                    pitchtools.NamedPitch("cs'"),
                    pitchtools.NamedPitch("e'"),
                    ),
                ),
            offset=durationtools.Offset(1, 2),
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
        self._offset = offset

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''True when `expr` is a q-event proxy with offset and q-event equal
        to those of this q-event proxy. Otherwise false.

        Returns boolean.
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
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        return (self.q_event, self.offset)

    def __getstate__(self):
        r'''Gets state.
        '''
        state = {}
        for current_class in inspect.getmro(type(self)):
            if hasattr(current_class, '__slots__'):
                for slot in current_class.__slots__:
                    if slot not in state:
                        state[slot] = getattr(self, slot)
        return state

    def __setstate__(self, state):
        r'''Sets state.
        '''
        for key, value in state.iteritems():
            setattr(self, key, value)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        keyword_argument_names = (
            'q_event',
            'offset',
            )
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
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
