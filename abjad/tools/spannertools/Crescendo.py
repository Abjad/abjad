# -*- coding: utf-8 -*-
from abjad.tools.spannertools.Hairpin import Hairpin


class Crescendo(Hairpin):
    r'''Crescendo.

    ..  container:: example

        ::

            >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
            >>> crescendo = spannertools.Crescendo()
            >>> attach(crescendo, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                r4
                c'8 \<
                d'8
                e'8
                f'8 \!
                r4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        direction=None,
        include_rests=False,
        overrides=None,
        ):
        Hairpin.__init__(
            self,
            descriptor='<',
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

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> crescendo = Crescendo()
                >>> attach(crescendo, staff[:])
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

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> crescendo = Crescendo(direction=Up)
                >>> attach(crescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> crescendo = Crescendo(include_rests=True)
                >>> attach(crescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> crescendo = Crescendo()
                >>> attach(crescendo, staff[:])
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

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> crescendo = Crescendo()
                >>> attach(crescendo, staff[:])
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

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> crescendo = Crescendo()
                >>> attach(crescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> crescendo.stop_dynamic is None
                True

        Returns dynamic or none.
        '''
        return self._stop_dynamic