# -*- encoding: utf-8 -*-
from abjad.tools.scoretools.Container import Container


class GraceContainer(Container):
    r'''A container of grace music.

    ::

        >>> voice = Voice("c'8 d'8 e'8 f'8")
        >>> beam = spannertools.Beam()
        >>> attach(beam, voice[:])
        >>> show(voice) # doctest: +SKIP

    ..  doctest::

        >>> print(format(voice))
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> grace_notes = [Note("c'16"), Note("d'16")]
        >>> grace_container = scoretools.GraceContainer(grace_notes, kind='grace')
        >>> attach(grace_container, voice[1])
        >>> show(voice) # doctest: +SKIP

    ..  doctest::

        >>> print(format(voice))
        \new Voice {
            c'8 [
            \grace {
                c'16
                d'16
            }
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> notes = [Note("e'16"), Note("f'16")]
        >>> after_grace = scoretools.GraceContainer(notes, kind='after')
        >>> attach(after_grace, voice[1])
        >>> show(voice) # doctest: +SKIP

    ..  doctest::

        >>> print(format(voice))
        \new Voice {
            c'8 [
            \grace {
                c'16
                d'16
            }
            \afterGrace
            d'8
            {
                e'16
                f'16
            }
            e'8
            f'8 ]
        }

    Fill grace containers with notes, rests or chords.

    Attach grace containers to nongrace notes, rests or chords.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = (
        '_carrier',
        '_kind',
        )

    ### INITIALIZER ###

    def __init__(self, music=None, kind='grace'):
        # self._carrier is a reference to the leaf carrying grace music
        self._carrier = None
        Container.__init__(self, music)
        self.kind = kind

#    ### SPECIAL METHODS ###
#
#    def __repr__(self):
#        r'''Gets interpreter representation of grace container.
#
#        Returns string.
#        '''
#        return '{}({})'.format(type(self).__name__, self._summary)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()

    ### PRIVATE METHODS ###

    def _attach(self, arg):
        from abjad.tools import scoretools
        if not isinstance(arg, scoretools.Leaf):
            message = 'object to which grace container attaches'
            message += ' must be leaf: {!r}.'
            message = message.format(arg)
            raise TypeError(message)
        if self.kind == 'after':
            arg._after_grace = self
        else:
            arg._grace = self
        self._carrier = arg

    def _copy_with_indicators_but_without_children_or_spanners(self):
        new = Container._copy_with_indicators_but_without_children_or_spanners(self)
        new.kind = self.kind
        return new

    def _detach(self):
        if self._carrier is not None:
            carrier = self._carrier
            if self.kind == 'after':
                #delattr(carrier, '_after_grace')
                carrier._after_grace = None
            else:
                #delattr(carrier, '_grace')
                carrier._grace = None
            self._carrier = None
            self[:] = []
        return self

    def _format_open_brackets_slot(self, bundle):
        result = []
        kind = self.kind
        if kind == 'after':
            result.append([('grace_brackets', 'open'), ['{']])
        else:
            contributor = ('grace_brackets', 'open')
            contributions = [r'\{} {{'.format(kind)]
            result.append([contributor, contributions])
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def kind(self):
        r'''Gets `kind` of grace container.

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> note = Note("cs'16")
            >>> grace = scoretools.GraceContainer([note], kind='grace')
            >>> attach(grace, staff[1])
            >>> grace.kind
            'grace'

        Sets `kind` of grace container:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> note = Note("cs'16")
            >>> grace = scoretools.GraceContainer([note], kind='grace')
            >>> attach(grace, staff[1])
            >>> grace.kind = 'acciaccatura'
            >>> grace.kind
            'acciaccatura'

        Valid options include ``'after'``, ``'grace'``,
        ``'acciaccatura'``, ``'appoggiatura'``.

        Returns string.
        '''
        return self._kind

    @kind.setter
    def kind(self, arg):
        assert arg in (
            'after',
            'grace',
            'acciaccatura',
            'appoggiatura',
            )
        self._kind = arg