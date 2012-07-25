from abjad.tools import abctools
from abjad.tools import durationtools
from experimental.quantizationtools.QEvent import QEvent


class ProxyQEvent(abctools.AbjadObject):
    '''Proxies a `QEvent`, mapping that QEvent's offset with the range of its
    beatspan to the range 0-1:

    ::

        >>> from experimental import quantizationtools
        >>> q_event = quantizationtools.PitchedQEvent(130, [0, 1, 4])
        >>> proxy = quantizationtools.ProxyQEvent(q_event, 0.5)
        >>> proxy
        quantizationtools.ProxyQEvent(
            quantizationtools.PitchedQEvent(
                durationtools.Offset(130, 1),
                (NamedChromaticPitch("c'"), NamedChromaticPitch("cs'"), NamedChromaticPitch("e'")),
                attachments=()
                ),
            durationtools.Offset(1, 2)
            )

    Returns `ProxyQEvent` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_offset', '_q_event')

    ### INITIALIZER ###

    def __init__(self, *args):

        if len(args) == 2:
            q_event, offset = args[0], durationtools.Offset(args[1])
            assert isinstance(q_event, QEvent)
            assert 0 <= args[1] <= 1
        elif len(args) == 3:
            q_event, minimum, maximum = args[0], \
                durationtools.Offset(args[1]), \
                durationtools.Offset(args[2])
            assert isinstance(q_event, QEvent)
            assert minimum <= q_event.offset < maximum
            offset = (q_event.offset - minimum) / (maximum - minimum)
        else:
            raise ValueError

        self._q_event = q_event
        self._offset = offset

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        return (self.q_event, self.offset)

    def __repr__(self):
        return '\n'.join(self._get_tools_package_qualified_repr_pieces())

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _mandatory_argument_names(self):
        return ('q_event', 'offset')

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def offset(self):
        return self._offset

    @property
    def q_event(self):
        return self._q_event
