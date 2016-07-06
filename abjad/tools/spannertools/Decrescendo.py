# -*- coding: utf-8 -*-
from abjad.tools.spannertools.Hairpin import Hairpin


class Decrescendo(Hairpin):
    r'''Decrescendo.

    ..  container:: example

        ::

            >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
            >>> decrescendo = spannertools.Decrescendo()
            >>> attach(decrescendo, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                r4
                c'8 \>
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
            descriptor='>',
            direction=direction,
            include_rests=include_rests,
            overrides=overrides,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def descriptor(self):
        r'''Gets descriptor of decrescendo.

        ..  container:: example

            ::

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> decrescendo = Decrescendo()
                >>> attach(decrescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> decrescendo.descriptor
                '>'

        Returns string.
        '''
        return self._descriptor

    @property
    def direction(self):
        r'''Gets direction.

        ..  container:: example

            Positions decrescendo above staff:

            ::

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> decrescendo = Decrescendo(direction=Up)
                >>> attach(decrescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                r4
                c'8 ^ \>
                d'8
                e'8
                f'8 \!
                r4
            }

            ::

                >>> decrescendo.direction
                '^'

        Defaults to none.

        Set to up, down or none.

        Returns up, down or none.
        '''
        return self._direction

    @property
    def include_rests(self):
        r'''Gets include-rests flag of decrescendo.

        ..  container:: example

            ::

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> decrescendo = Decrescendo(include_rests=True)
                >>> attach(decrescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                r4 \>
                c'8
                d'8
                e'8
                f'8
                r4 \!
            }

            ::

                >>> decrescendo.include_rests
                True

        Returns true or false.
        '''
        return self._include_rests

    @property
    def shape_string(self):
        r'''Gets shape string of decrescendo.

        ..  container:: example

            ::

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> decrescendo = Decrescendo()
                >>> attach(decrescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> decrescendo.shape_string
                '>'

        Returns string.
        '''
        return self._shape_string

    @property
    def start_dynamic(self):
        r'''Gets start dynamic of decrescendo.

        ..  container:: example

            ::

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> decrescendo = Decrescendo()
                >>> attach(decrescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> decrescendo.start_dynamic is None
                True

        Returns dynamic or none.
        '''
        return self._start_dynamic

    @property
    def stop_dynamic(self):
        r'''Gets stop dynamic of decrescendo.

        ..  container:: example

            ::

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> decrescendo = Decrescendo()
                >>> attach(decrescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> decrescendo.stop_dynamic is None
                True

        Returns dynamic or none.
        '''
        return self._stop_dynamic