# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mutationtools
from abjad.tools.scoretools.Tuplet import Tuplet


class FixedDurationTuplet(Tuplet):
    r'''A tuplet with fixed duration and variable multiplier.

    ..  container:: example

            >>> tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), [])
            >>> tuplet.extend("c'8 d'8 e'8")
            >>> show(tuplet) # doctest: +SKIP

        ..  doctest::

            >>> f(tuplet)
            \times 2/3 {
                c'8
                d'8
                e'8
            }

        ::

            >>> tuplet.append("fs'4")
            >>> show(tuplet) # doctest: +SKIP

        ..  doctest::

            >>> f(tuplet)
            \times 2/5 {
                c'8
                d'8
                e'8
                fs'4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_target_duration',
        )

    _default_positional_input_arguments = (
        (1, 4),
        repr("c'8 d'8 e'8"),
        )

    ### INITIALIZER ###

    def __init__(self, duration, music=None):
        dummy_multiplier = durationtools.Multiplier(1)
        Tuplet.__init__(self, dummy_multiplier, music)
        self._signifier = '@'
        self.target_duration = duration

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        '''Gets new arguments.

        Returns tuple.
        '''
        return (self.target_duration, )

    def __repr__(self):
        '''Interpreter representation of fixd-duration tuplet.

        Returns string.
        '''
        return '%s(%s, [%s])' % (
            self._class_name, self.target_duration, self._summary)

    def __str__(self):
        '''String representation of fixed-duration tuplet.

        Returns string.
        '''
        if 0 < len(self):
            return '{%s %s %s %s}' % (
                self._signifier,
                self._ratio_string,
                self._summary,
                self._signifier,
                )
        else:
            return '{%s %s %s}' % (
                self._signifier,
                self.target_duration,
                self._signifier,
                )

    ### PRIVATE METHODS ###

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

    ### PUBLIC PROPERTIES ###

    @property
    def multiplied_duration(self):
        r'''Multiplied duration of tuplet:

        ::

            >>> tuplet = scoretools.FixedDurationTuplet((1, 4), "c'8 d'8 e'8")
            >>> tuplet.multiplied_duration
            Duration(1, 4)

        Returns duration.
        '''
        return self.target_duration

    @apply
    def multiplier():
        def fget(self):
            r'''Multiplier of tuplet:

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
        def fset(self, expr):
            pass
        return property(**locals())

    @apply
    def target_duration():
        def fget(self):
            r'''Read / write target duration of fixed-duration tuplet:

            ::

                >>> tuplet = scoretools.FixedDurationTuplet(
                ...     (1, 4), "c'8 d'8 e'8")
                >>> tuplet.target_duration
                Duration(1, 4)

            ..  doctest::

                >>> f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

            ::

                >>> tuplet.target_duration = Duration(5, 8)
                >>> f(tuplet)
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 5/3 {
                    c'8
                    d'8
                    e'8
                }

            Returns duration.
            '''
            return self._target_duration
        def fset(self, expr):
            target_duration = durationtools.Duration(expr)
            assert 0 < target_duration
            self._target_duration = target_duration
        return property(**locals())

    ### PUBLIC METHODS ###

    def to_fixed_multiplier(self):
        r'''Change fixed-duration tuplet to (unqualified) tuplet.

        ..  container:: example

            **Example:**

            ::

                >>> tuplet = scoretools.FixedDurationTuplet((2, 8), [])
                >>> tuplet.extend("c'8 d'8 e'8")
                >>> show(tuplet) # doctest: +SKIP

            ::

                >>> tuplet
                FixedDurationTuplet(1/4, [c'8, d'8, e'8])

            ::

                >>> new_tuplet = tuplet.to_fixed_multiplier()
                >>> show(new_tuplet) # doctest: +SKIP

            ::

                >>> new_tuplet
                Tuplet(2/3, [c'8, d'8, e'8])

        Returns new tuplet.
        '''
        from abjad.tools import scoretools
        new_tuplet = scoretools.Tuplet(self.multiplier, [])
        mutationtools.mutate(self).swap(new_tuplet)
        return new_tuplet

    def toggle_prolation(self):
        if self.is_diminution:
            while self.is_diminution:
                for leaf in self.select_leaves():
                    leaf.written_duration /= 2
        elif not self.is_diminution:
            while not self.is_diminution:
                for leaf in self.select_leaves():
                    leaf.written_duration *= 2

    def trim(self, start, stop='unused'):
        r'''Trim fixed-duration tuplet elements from `start` to `stop`:

        ::

            >>> tuplet = scoretools.FixedDurationTuplet(
            ...     Duration(2, 8), "c'8 d'8 e'8")
            >>> tuplet
            FixedDurationTuplet(1/4, [c'8, d'8, e'8])

        ::

            >>> tuplet.trim(2)
            >>> tuplet
            FixedDurationTuplet(1/6, [c'8, d'8])

        Preserve fixed-duration tuplet multiplier.

        Adjust fixed-duration tuplet duration.

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
