from abjad.core import _Immutable
from abjad.core import _StrictComparator


class SchemeColor(_StrictComparator, _Immutable):
    '''Abjad model of Scheme color::

        abjad> schemetools.SchemeColor('ForestGreen')
        SchemeColor('ForestGreen')

    Scheme colors are immutable.
    '''

    __slots__ = ('color_name',)

    def __new__(klass, color_name):
        self = object.__new__(klass)
        if isinstance(color_name, klass):
            color_name = color_name.color_name
        object.__setattr__(self, 'color_name', color_name)
        return self

    def __getnewargs__(self):
        return (self.color_name,)

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.color_name)

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        '''LilyPond input format of Scheme color::

            abjad> scheme_color = schemetools.SchemeColor('ForestGreen')
            abjad> scheme_color.format
            "#(x11-color 'ForestGreen)"

        Return string.
        '''
        return "#(x11-color '%s)" % self.color_name
