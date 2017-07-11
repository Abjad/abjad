# -*- coding: utf-8 -*-
from abjad.tools.spannertools.Hairpin import Hairpin


class Crescendo(Hairpin):
    r'''Crescendo.

    ::

        >>> import abjad

    ..  container:: example

        Initializes crescendo without start- and stop-dynamics:

        ::

            >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
            >>> crescendo = abjad.Crescendo()
            >>> abjad.attach(crescendo, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                r4
                c'8 \<
                d'8
                e'8
                f'8 \!
                r4
            }

    ..  container:: example

        Initializes crescendo with start- and stop-dynamics:

        ::

            >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
            >>> crescendo = abjad.Crescendo('p < f')
            >>> abjad.attach(crescendo, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                r4
                c'8 \< \p
                d'8
                e'8
                f'8 \f
                r4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        descriptor='<',
        direction=None,
        include_rests=False,
        overrides=None,
        ):
        assert '<' in descriptor, repr(descriptor)
        Hairpin.__init__(
            self,
            descriptor=descriptor,
            direction=direction,
            include_rests=include_rests,
            overrides=overrides,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def descriptor(self):
        r'''Gets descriptor of crescendo.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> crescendo = abjad.Crescendo()
                >>> abjad.attach(crescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> crescendo.descriptor
                '<'

        Returns string.
        '''
        return self._descriptor

    @property
    def direction(self):
        r'''Gets direction.

        ..  container:: example

            Positions crescendo above staff:

            ::

                >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> crescendo = abjad.Crescendo(direction=Up)
                >>> abjad.attach(crescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                r4
                c'8 ^ \<
                d'8
                e'8
                f'8 \!
                r4
            }

            ::

                >>> crescendo.direction
                '^'

        Defaults to none.

        Set to up, down or none.

        Returns up, down or none.
        '''
        return self._direction

    @property
    def include_rests(self):
        r'''Gets include-rests flag of crescendo.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> crescendo = abjad.Crescendo(include_rests=True)
                >>> abjad.attach(crescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                r4 \<
                c'8
                d'8
                e'8
                f'8
                r4 \!
            }

            ::

                >>> crescendo.include_rests
                True

        Returns true or false.
        '''
        return self._include_rests

    @property
    def shape_string(self):
        r'''Gets shape string of crescendo.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> crescendo = abjad.Crescendo()
                >>> abjad.attach(crescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> crescendo.shape_string
                '<'

        Returns string.
        '''
        return self._shape_string

    @property
    def start_dynamic(self):
        r'''Gets start dynamic of crescendo.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> crescendo = abjad.Crescendo()
                >>> abjad.attach(crescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> crescendo.start_dynamic is None
                True

        Returns dynamic or none.
        '''
        return self._start_dynamic

    @property
    def stop_dynamic(self):
        r'''Gets stop dynamic of crescendo.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> crescendo = abjad.Crescendo()
                >>> abjad.attach(crescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> crescendo.stop_dynamic is None
                True

        Returns dynamic or none.
        '''
        return self._stop_dynamic
