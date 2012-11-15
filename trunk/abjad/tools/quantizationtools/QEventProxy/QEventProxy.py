import inspect
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class QEventProxy(AbjadObject):
    '''Proxies a `QEvent`, mapping that QEvent's offset with the range of its
    beatspan to the range 0-1:

    ::

        >>> from experimental import quantizationtools
        >>> q_event = quantizationtools.PitchedQEvent(130, [0, 1, 4])
        >>> proxy = quantizationtools.QEventProxy(q_event, 0.5)
        >>> proxy
        quantizationtools.QEventProxy(
            quantizationtools.PitchedQEvent(
                durationtools.Offset(130, 1),
                (NamedChromaticPitch("c'"), NamedChromaticPitch("cs'"), NamedChromaticPitch("e'")),
                attachments=()
                ),
            durationtools.Offset(1, 2)
            )

    Not composer-safe.

    Used internally by ``Quantizer``.

    Returns `QEventProxy` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_offset', '_q_event')

    ### INITIALIZER ###

    def __init__(self, *args):
        from experimental import quantizationtools

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

    def __eq__(self, other):
        if type(self) == type(other):
            if self.offset == other.offset:
                if self.q_event == other.q_event:
                    return True
        return False

    def __getnewargs__(self):
        return (self.q_event, self.offset)

    def __getstate__(self):
        state = {}
        for klass in inspect.getmro(self.__class__):
            if hasattr(klass, '__slots__'):
                for slot in klass.__slots__:
                    if slot not in state:
                        state[slot] = getattr(self, slot)
        return state

    def __repr__(self):
        return '\n'.join(self._get_tools_package_qualified_repr_pieces())

    def __setstate__(self, state):
        for key, value in state.iteritems():
            setattr(self, key, value)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _mandatory_argument_names(self):
        return ('q_event', 'offset')

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def index(self):
        return self._q_event.index

    @property
    def offset(self):
        return self._offset

    @property
    def q_event(self):
        return self._q_event
