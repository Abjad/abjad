from abjad.core import _Immutable


class _Interval(_Immutable):
    '''.. versionadded:: 2.0

    Interval base class.
    '''

    ### OVERLOADS ###

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

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return str(self.number)

    ### PUBLIC ATTRIBUTES ###

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
