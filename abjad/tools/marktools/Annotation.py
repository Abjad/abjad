# -*- encoding: utf-8 -*-
import copy
from abjad.tools.marktools.Mark import Mark


class Annotation(Mark):
    r'''An annotation.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> pitch = pitchtools.NamedPitch('ds')
        >>> annotation = marktools.Annotation('special pitch', pitch)
        >>> attach(annotation, staff[0])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    Annotations contribute no formatting.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_format_slot', 
        '_name', 
        '_value',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        Mark.__init__(self)
        if len(args) == 1 and isinstance(args[0], type(self)):
            self._name = copy.copy(args[0].name)
            self._value = copy.copy(args[0].value)
        elif len(args) == 1 and not isinstance(args[0], type(self)):
            self._name = copy.copy(args[0])
            self._value = None
        elif len(args) == 2:
            self._name = copy.copy(args[0])
            self._value = copy.copy(args[1])
        else:
            message = 'unknown annotation initialization signature.'
            raise ValueError(message)
        self._format_slot = None

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies annotation.

        Returns new annotation.
        '''
        return type(self)(self.name, self.value)

    def __eq__(self, arg):
        r'''True when arg is an annotation with name and value
        equal to those of this annotation. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.name == arg.name:
                if self.value == self.value:
                    return True
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        if self.value is None:
            return repr(self.name)
        return ', '.join([repr(self.name), repr(self.value)])

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        r'''Name of annotation.

        ::

            >>> annotation.name
            'special pitch'

        Returns string.
        '''
        return self._name

    @property
    def value(self):
        r'''Value of annotation.

        ::

            >>> annotation.value
            NamedPitch('ds')

        Returns arbitrary object.
        '''
        return self._value
