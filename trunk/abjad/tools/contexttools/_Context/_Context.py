from abjad.tools.containertools.Container import Container
from abjad.tools.contexttools._Context._ContextFormatter import _ContextFormatter
import copy


class _Context(Container):
    '''Abjad model of a horizontal layer of music.
    '''

    __slots__ = ('_context', '_engraver_consists', '_engraver_removals',
        '_is_nonsemantic', '_name', )

    def __init__(self, music = None):
        Container.__init__(self, music)
        self._context = '_Context'
        self._formatter = _ContextFormatter(self)
        self._engraver_consists = set([])
        self._engraver_removals = set([])
        self._name = None
        self.is_nonsemantic = False

    ### OVERLOADS ###

    def __copy__(self, *args):
        new = Container.__copy__(self, *args)
        new._engraver_consists = copy.copy(self.engraver_consists)
        new._engraver_removals = copy.copy(self.engraver_removals)
        new.name = copy.copy(self.name)
        new.is_nonsemantic = copy.copy(self.is_nonsemantic)
        return new

    def __repr__(self):
        '''.. versionchanged:: 2.0
        Named contexts now print name at the interpreter.'''
        if 0 < len(self):
            summary = str(len(self))
        else:
            #summary = ' '
            summary = ''
        if self.is_parallel:
            open, close = '<<', '>>'
        else:
            open, close = '{', '}'
        name = self.name
        if name is not None:
            name = '-"%s"' % name
        else:
            name = ''
        return '%s%s%s%s%s' % (self.context, name, open, summary, close)

    ### PUBLIC ATTRIBUTES ###

    @apply
    def context():
        def fget(self):
            '''Read / write name of context as a string.'''
            return self._context
        def fset(self, arg):
            assert isinstance(arg, str)
            self._context = arg
        return property(**locals())

    @property
    def engraver_consists(self):
        r'''.. versionadded:: 2.0

        Unordered set of LilyPond engravers to include in context definition.

        Manage with add, update, other standard set commands. ::

            abjad> staff = Staff([])
            abjad> staff.engraver_consists.add('Horizontal_bracket_engraver')
            abjad> f(staff)
            \new Staff \with {
                \consists Horizontal_bracket_engraver
            } {
            }

        '''
        return self._engraver_consists

    @property
    def engraver_removals(self):
        r'''.. versionadded:: 2.0

        Unordered set of LilyPond engravers to remove from context.

        Manage with add, update, other standard set commands. ::

            abjad> staff = Staff([])
            abjad> staff.engraver_removals.add('Time_signature_engraver')
            abjad> f(staff)
            \new Staff \with {
                \remove Time_signature_engraver
            } {
            }

        '''
        return self._engraver_removals

    @apply
    def is_nonsemantic():
        def fget(self):
            r'''Set indicator of nonsemantic voice::

                abjad> measures = measuretools.make_measures_with_full_measure_spacer_skips([(1, 8), (5, 16), (5, 16)])
                abjad> voice = Voice(measures)
                abjad> voice.name = 'HiddenTimeSignatureVoice'

            ::

                abjad> voice.is_nonsemantic = True

            ::

                abjad> f(voice)
                \context Voice = "HiddenTimeSignatureVoice" {
                    {
                        \time 1/8
                        s1 * 1/8
                    }
                    {
                        \time 5/16
                        s1 * 5/16
                    }
                    {
                        \time 5/16
                        s1 * 5/16
                    }
                }

            ::

                abjad> voice.is_nonsemantic
                True

            Get indicator of nonsemantic voice::

                abjad> voice = Voice([])

            ::

                abjad> voice.is_nonsemantic
                False

            Return boolean.

            The intent of this read / write attribute is to allow composers to tag invisible
            voices used to house time signatures indications, bar number directives or other
            pieces of score-global non-musical information. Such nonsemantic voices can then
            be omitted from voice interation and other functions.
            '''
            return self._is_nonsemantic
        def fset(self, arg):
            if not isinstance(arg, bool):
                raise TypeError
            self._is_nonsemantic = arg
        return property(**locals())

    @property
    def is_semantic(self):
        return not self.is_nonsemantic

    @apply
    def name():
        def fget(self):
            '''Read-write name of component. Must be string or none.'''
            return self._name
        def fset(self, arg):
            assert isinstance(arg, (str, type(None)))
            self._name = arg
        return property(**locals())
