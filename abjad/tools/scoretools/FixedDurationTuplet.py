# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import systemtools
from abjad.tools.scoretools.Tuplet import Tuplet
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import mutate


class FixedDurationTuplet(Tuplet):
    r'''A tuplet with fixed duration and variable multiplier.

    ..  container:: example

            >>> tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), [])
            >>> tuplet.extend("c'8 d'8 e'8")
            >>> show(tuplet) # doctest: +SKIP

        ..  doctest::

            >>> print(format(tuplet))
            \times 2/3 {
                c'8
                d'8
                e'8
            }

        ::

            >>> tuplet.append("fs'4")
            >>> show(tuplet) # doctest: +SKIP

        ..  doctest::

            >>> print(format(tuplet))
            \times 2/5 {
                c'8
                d'8
                e'8
                fs'4
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = (
        '_target_duration',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        duration=durationtools.Duration(1, 4),
        music="c'8 c'8 c'8",
        ):
        dummy_multiplier = durationtools.Multiplier(1)
        Tuplet.__init__(self, dummy_multiplier, music)
        self._signifier = '@'
        self.target_duration = duration

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        '''Gets new arguments of fixed-duration tuplet.

        Returns tuple.
        '''
        duration = self.target_duration
        empty_components = ()
        return (duration, empty_components)

    def __repr__(self):
        '''Gets interpreter representation of fixed-duration tuplet.

        Returns string.
        '''
        result = '{}({!r}, {!r})'
        result = result.format(
            type(self).__name__,
            self.target_duration,
            self._contents_summary,
            )
        return result

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            repr_args_values=[self.target_duration, self._contents_summary],
            storage_format_args_values=[self.target_duration, self[:]],
            storage_format_kwargs_names=[],
            )

    def _scale(self, multiplier):
        from abjad.tools import scoretools
        multiplier = durationtools.Multiplier(multiplier)
        # find new target duration
        old_target_duration = self.target_duration
        new_target_duration = multiplier * old_target_duration
        # change tuplet target duration
        self.target_duration = new_target_duration
        # if multiplier is note head assignable,
        # scale contents graphically
        if multiplier.is_assignable:
            for component in self[:]:
                if isinstance(component, scoretools.Leaf):
                    new_duration = multiplier * component.written_duration
                    component._set_duration(new_duration)
        self._fix()

    ### PUBLIC METHODS ###

    def to_fixed_multiplier(self):
        r'''Changes fixed-duration tuplet to (unqualified) tuplet.

        ..  container:: example

            ::

                >>> tuplet = scoretools.FixedDurationTuplet((2, 8), [])
                >>> tuplet.extend("c'8 d'8 e'8")
                >>> show(tuplet) # doctest: +SKIP

            ::

                >>> tuplet
                FixedDurationTuplet(Duration(1, 4), "c'8 d'8 e'8")

            ::

                >>> new_tuplet = tuplet.to_fixed_multiplier()
                >>> show(new_tuplet) # doctest: +SKIP

            ::

                >>> new_tuplet
                Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")

        Returns new tuplet.
        '''
        from abjad.tools import scoretools
        new_tuplet = scoretools.Tuplet(self.multiplier, [])
        mutate(self).swap(new_tuplet)
        return new_tuplet

    def toggle_prolation(self):
        r'''Toggles prolation of fixed-duration tuplet.

        ::

            >>> tuplet = scoretools.FixedDurationTuplet((1, 4), "c'8 d'8 e'8")
            >>> show(tuplet) # doctest: +SKIP

        ::

            >>> tuplet.toggle_prolation()
            >>> show(tuplet) # doctest: +SKIP

        ::

            >>> tuplet.toggle_prolation()
            >>> show(tuplet) # doctest: +SKIP

        Returns none.
        '''
        if self.is_diminution:
            while self.is_diminution:
                for leaf in iterate(self).by_leaf():
                    leaf.written_duration /= 2
        elif not self.is_diminution:
            while not self.is_diminution:
                for leaf in iterate(self).by_leaf():
                    leaf.written_duration *= 2

    def trim(self, start, stop='unused'):
        r'''Trims fixed-duration tuplet elements from `start` to `stop`:

        ::

            >>> tuplet = scoretools.FixedDurationTuplet(
            ...     Duration(2, 8), "c'8 d'8 e'8")
            >>> tuplet
            FixedDurationTuplet(Duration(1, 4), "c'8 d'8 e'8")

        ::

            >>> tuplet.trim(2)
            >>> tuplet
            FixedDurationTuplet(Duration(1, 6), "c'8 d'8")

        Preserves fixed-duration tuplet multiplier.

        Adjusts fixed-duration tuplet duration.

        Returns none.
        '''
        if stop != 'unused':
            assert not (start == 0 and (stop is None or len(self) <= stop))
        old_multiplier = self.multiplier
        if stop == 'unused':
            del(self[start])
        else:
            del(self[start:stop])
        self.target_duration = old_multiplier * self._contents_duration

    ### PUBLIC PROPERTIES ###

    @property
    def multiplied_duration(self):
        r'''Gets multiplied duration of tuplet.

        ::

            >>> tuplet = scoretools.FixedDurationTuplet((1, 4), "c'8 d'8 e'8")
            >>> tuplet.multiplied_duration
            Duration(1, 4)

        Returns duration.
        '''
        return self.target_duration

    @property
    def multiplier(self):
        r'''Gets and sets multiplier of fixed-duration tuplet.

        ::

            >>> tuplet = scoretools.FixedDurationTuplet(
            ...     (1, 4), "c'8 d'8 e'8")
            >>> tuplet.multiplier
            Multiplier(2, 3)

        Returns multiplier.
        '''
        if 0 < len(self):
            return durationtools.Multiplier(
                self.target_duration / self._contents_duration)
        else:
            return None

    @multiplier.setter
    def multiplier(self, expr):
        pass

    @property
    def target_duration(self):
        r'''Gets and sets target duration of fixed-duration tuplet.

        ::

            >>> tuplet = scoretools.FixedDurationTuplet(
            ...     (1, 4), "c'8 d'8 e'8")
            >>> tuplet.target_duration
            Duration(1, 4)

        ..  doctest::

            >>> print(format(tuplet))
            \times 2/3 {
                c'8
                d'8
                e'8
            }

        ::

            >>> tuplet.target_duration = Duration(5, 8)
            >>> print(format(tuplet))
            \tweak text #tuplet-number::calc-fraction-text
            \times 5/3 {
                c'8
                d'8
                e'8
            }

        Returns duration.
        '''
        return self._target_duration

    @target_duration.setter
    def target_duration(self, expr):
        target_duration = durationtools.Duration(expr)
        assert 0 < target_duration
        self._target_duration = target_duration
