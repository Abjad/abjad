import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class IntervalObject(AbjadObject):
    '''.. versionadded:: 2.0

    Interval base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta
    __slots__ = ('_format_string', )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        raise NotImplementedError('abs needs to be implemented on %s.' % type(self))

    def __float__(self):
        raise NotImplementedError('float needs to be implemented on %s.' % type(self))

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        raise NotImplementedError('int needs to be implemented on %s.' % type(self))

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    def __str__(self):
        return str(self.number)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return str(self.number)

    ### PUBLIC PROPERTIES ###

    @property
    def cents(self):
        return 100 * self.semitones

    # TODO: remove
    @property
    def interval_class(self):
        pass

    # TODO: remove
    @property
    def number(self):
        return self._number

    @property
    def semitones(self):
        pass
