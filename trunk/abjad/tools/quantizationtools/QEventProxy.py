# -*- encoding: utf-8 -*-
import inspect
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class QEventProxy(AbjadObject):
    r'''Proxies a `QEvent`, mapping that QEvent's offset with the range of 
    its beatspan to the range 0-1:

    ::

        >>> q_event = quantizationtools.PitchedQEvent(130, [0, 1, 4])
        >>> proxy = quantizationtools.QEventProxy(q_event, 0.5)
        >>> proxy
        quantizationtools.QEventProxy(
            quantizationtools.PitchedQEvent(
                durationtools.Offset(130, 1),
                (NamedPitch("c'"), NamedPitch("cs'"), NamedPitch("e'")),
                attachments=()
                ),
            durationtools.Offset(1, 2)
            )

    Not composer-safe.

    Used internally by ``Quantizer``.

    Returns `QEventProxy` instance.
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
        else:
            raise ValueError

        self._q_event = q_event
        self._offset = offset

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(self) == type(expr):
            if self.offset == expr.offset:
                if self.q_event == expr.q_event:
                    return True
        return False

    def __getnewargs__(self):
        return (self.q_event, self.offset)

    def __getstate__(self):
        state = {}
        for current_class in inspect.getmro(self.__class__):
            if hasattr(current_class, '__slots__'):
                for slot in current_class.__slots__:
                    if slot not in state:
                        state[slot] = getattr(self, slot)
        return state

    def __repr__(self):
        return '\n'.join(self._get_tools_package_qualified_repr_pieces())

    def __setstate__(self, state):
        for key, value in state.iteritems():
            setattr(self, key, value)

    ### PRIVATE PROPERTIES ###

    @property
    def _positional_argument_names(self):
        return ('q_event', 'offset')

    ### PUBLIC PROPERTIES ###

    @property
    def index(self):
        return self._q_event.index

    @property
    def offset(self):
        return self._offset

    @property
    def q_event(self):
        return self._q_event
