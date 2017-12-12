from abjad.tools import systemtools
from abjad.tools.abctools import AbjadObject


class QEventProxy(AbjadObject):
    r'''Q-event proxy.

    Maps Q-event offset with the range of its beatspan to the range 0-1.

    ..  container:: example

        >>> q_event = abjad.quantizationtools.PitchedQEvent(130, [0, 1, 4])
        >>> proxy = abjad.quantizationtools.QEventProxy(q_event, 0.5)
        >>> abjad.f(proxy)
        abjad.quantizationtools.QEventProxy(
            abjad.quantizationtools.PitchedQEvent(
                offset=abjad.Offset(130, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    abjad.NamedPitch("cs'"),
                    abjad.NamedPitch("e'"),
                    ),
                ),
            abjad.Offset(1, 2)
            )

    Not composer-safe.

    Used internally by ``Quantizer``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_offset',
        '_q_event',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, *arguments):
        import abjad
        from abjad.tools import quantizationtools
        if len(arguments) == 2:
            q_event, offset = arguments[0], abjad.Offset(arguments[1])
            assert isinstance(q_event, quantizationtools.QEvent)
            assert 0 <= offset <= 1
        elif len(arguments) == 3:
            q_event, minimum, maximum = arguments[0], \
                abjad.Offset(arguments[1]), \
                abjad.Offset(arguments[2])
            assert isinstance(q_event, quantizationtools.QEvent)
            assert minimum <= q_event.offset <= maximum
            offset = (q_event.offset - minimum) / (maximum - minimum)
        elif len(arguments) == 0:
            q_event = None
            offset = abjad.Offset(0)
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, arguments)
            raise ValueError(message)
        self._q_event = q_event
        self._offset = abjad.Offset(offset)

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is a q-event proxy with offset and q-event
        equal to those of this q-event proxy. Otherwise false.

        Returns true or false.
        '''
        if type(self) == type(argument):
            if self.offset == argument.offset:
                if self.q_event == argument.q_event:
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
            return systemtools.StorageFormatManager(self).get_storage_format()
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
