from abjad.tools.componenttools._Component import _Component
from abjad.tools import mathtools
from abjad.tools.marktools.Mark import Mark


class StemTremolo(Mark):
    '''.. versionadded:: 2.0

    Abjad model of stem tremolo::

        abjad> note = Note("c'4")

    ::

        abjad> marktools.StemTremolo(16)(note)
        StemTremolo(16)(c'4)

    ::

        abjad> f(note)
        c'4 :16

    Stem tremolos implement ``__slots__``.
    '''

    __slots__ = ('_format_slot', '_tremolo_flags')

    def __init__(self, *args):
        Mark.__init__(self)
        self._format_slot = 'right'
        if len(args) == 1 and isinstance(args[0], type(self)):
            self.tremolo_flags = args[0].tremolo_flags
        elif len(args) == 1 and not isinstance(args[0], type(self)):
            self.tremolo_flags = args[0]
        else:
            raise ValueError('can not initialize stem tremolo.')

    ### OVERLOADS ###

    def __copy__(self, *args):
        return type(self)(self.tremolo_flags)

    __deepcopy__ = __copy__

    def __eq__(self, expr):
        assert isinstance(expr, type(self))
        if self.tremolo_flags == expr.tremolo_flags:
            return True
        return False

    def __str__(self):
        return ':%s' % str(self.tremolo_flags)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _contents_repr_string(self):
        return '%s' % self.tremolo_flags

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        '''Read-only LilyPond format string::

            abjad> stem_tremolo = marktools.StemTremolo(16)
            abjad> stem_tremolo.format
            ':16'

        Return string.
        '''
        return str(self)

    @apply
    def tremolo_flags():
        def fget(self):
            '''Get tremolo flags::

                abjad> stem_tremolo = marktools.StemTremolo(16)
                abjad> stem_tremolo.tremolo_flags
                16

            Set tremolo flags::

                abjad> stem_tremolo.tremolo_flags = 32
                abjad> stem_tremolo.tremolo_flags
                32

            Set integer.
            '''
            return self._tremolo_flags
        def fset(self, tremolo_flags):
            if not mathtools.is_nonnegative_integer_power_of_two(tremolo_flags):
                raise ValueError('tremolo flags must be nonnegative integer power of 2.')
            self._tremolo_flags = tremolo_flags
        return property(**locals())
