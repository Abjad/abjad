# -*- coding: utf-8 -*-
import copy
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import override
from abjad.tools.datastructuretools.TypedList import TypedList


class ClefList(TypedList):
    r'''Clef list.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> clefs = abjad.instrumenttools.ClefList(['treble', 'bass'])

        ::

            >>> f(clefs)
            instrumenttools.ClefList(
                [
                    abjad.Clef(
                        name='treble',
                        ),
                    abjad.Clef(
                        name='bass',
                        ),
                    ]
                )

        ::

            >>> 'treble' in clefs
            True

        ::

            >>> abjad.Clef('treble') in clefs
            True

        ::

            >>> 'alto' in clefs
            False

        ::

            >>> show(clefs) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = clefs.__illustrate__()
            >>> f(lilypond_file[abjad.Staff])
            \new Staff \with {
                \override Clef.full-size-change = ##t
                \override Rest.transparent = ##t
                \override TimeSignature.stencil = ##f
            } {
                \clef "treble"
                r8
                \clef "bass"
                r8
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __illustrate__(self):
        r'''Illustrates clefs.

        ..  container:: example

            ::

                >>> show(clefs) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = clefs.__illustrate__()
                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override Clef.full-size-change = ##t
                    \override Rest.transparent = ##t
                    \override TimeSignature.stencil = ##f
                } {
                    \clef "treble"
                    r8
                    \clef "bass"
                    r8
                }

        Returns LilyPond file.
        '''
        import abjad
        staff = abjad.Staff()
        for clef in self:
            rest = abjad.Rest((1, 8))
            clef = copy.copy(clef)
            attach(clef, rest)
            staff.append(rest)
        override(staff).clef.full_size_change = True
        override(staff).rest.transparent = True
        override(staff).time_signature.stencil = False
        lilypond_file = abjad.LilyPondFile.new(staff)
        lilypond_file.header_block.tagline = False
        return lilypond_file

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import indicatortools
        return indicatortools.Clef
