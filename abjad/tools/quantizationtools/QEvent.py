import abc
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class QEvent(AbjadObject):
    r'''Abstract Q-event.

    Represents an attack point to be quantized.

    All ``QEvents`` possess a rational offset in milliseconds, and an optional
    index for disambiguating events which fall on the same offset in a
    ``QGrid``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_index',
        '_offset',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, offset=0, index=None):
        import abjad
        offset = abjad.Offset(offset)
        self._offset = offset
        self._index = index

    ### SPECIAL METHODS ###

    def __lt__(self, argument):
        r'''Is true when `epxr` is a q-event with offset greater than that of this
        q-event. Otherwise false.

        Returns true or false.
        '''
        if type(self) == type(self):
            if self.offset < argument.offset:
                return True
        return False

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        agent = systemtools.StorageFormatManager(self)
        names = agent.signature_keyword_names
        for name in ('attachments',):
            if not getattr(self, name, None) and name in names:
                names.remove(name)
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_kwargs_names=names,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def index(self):
        r'''The optional index, for sorting QEvents with identical offsets.
        '''
        return self._index

    @property
    def offset(self):
        r'''The offset in milliseconds of the event.
        '''
        return self._offset
