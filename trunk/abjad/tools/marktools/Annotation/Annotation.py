from abjad.tools.componenttools._Component import _Component
from abjad.tools.marktools.Mark import Mark
import copy


class Annotation(Mark):
    r'''.. versionadded:: 2.0

    User-defined annotation::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> marktools.Annotation('special pitch', pitchtools.NamedChromaticPitch('ds'))(staff[0])
        Annotation('special pitch', NamedChromaticPitch('ds'))(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    Annotations contribute no formatting.

    Annotations implement ``__slots__``.
    '''

    #__slots__ = ('_contents', '_format_slot', )
    __slots__ = ('_format_slot', '_name', '_value', )

    _format_slot = None

    #def __init__(self, contents):
    def __init__(self, name, value = None):
        Mark.__init__(self)
        #self._contents = copy.copy(contents)
        self._name = copy.copy(name)
        self._value = copy.copy(value)

    ## OVERLOADS ##

    def __copy__(self, *args):
        #return type(self)(self.contents_string)
        return type(self)(self.name, self.value)

    __deepcopy__ = __copy__

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            #return self.contents_string == arg.contents_string
            if self.name == arg.name:
                if self.value == self.value:
                    return True
        return False

    ## PRIVATE ATTRIBUTES ##

    @property
    def _contents_repr_string(self):
        #return repr(self.contents_string)
        if self.value is None:
            return repr(self.name)
        return ', '.join([repr(self.name), repr(self.value)])

    ## PUBLIC ATTRIBUTES ##

#   @apply
#   def contents_string( ):
#      def fget(self):
#         '''Get contents string of annotation::
#
#            abjad> annotation = marktools.Annotation('annotation contents')
#            abjad> annotation.contents_string
#            'annotation contents'
#
#         Set contents string of annotation::
#
#            abjad> annotation.contents_string = 'new annotation contents'
#            abjad> annotation.contents_string
#            'new annotation contents'
#         '''
#         return self._contents
#      def fset(self, contents_string):
#         assert isinstance(contents_string, str)
#         self._contents = contents_string
#      return property(**locals( ))

    @apply
    def name( ):
        def fget(self):
            '''Get name of annotation::

                abjad> annotation = marktools.Annotation('special_pitch', pitchtools.NamedChromaticPitch('ds'))
                abjad> annotation.name
                'special_pitch'

            Set name of annotation::

                abjad> annotation.name = 'revised special pitch'
                abjad> annotation.name
                'revised special pitch'

            Set string.
            '''
            return self._name
        def fset(self, name):
            assert isinstance(name, str)
            self._name = name
        return property(**locals( ))

    @apply
    def value( ):
        def fget(self):
            '''Get value of annotation::

                abjad> annotation = marktools.Annotation('special_pitch', pitchtools.NamedChromaticPitch('ds'))
                abjad> annotation.value
                NamedChromaticPitch('ds')

            Set value of annotation::

                abjad> annotation.value = pitchtools.NamedChromaticPitch('e')
                abjad> annotation.value
                NamedChromaticPitch('e')

            Set arbitrary object.
            '''
            return self._value
        def fset(self, value):
            self._value = value
        return property(**locals( ))

