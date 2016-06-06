# -*- coding: utf-8 -*-
from abjad.tools.expressiontools.Expression import Expression


class LabelExpression(Expression):
    r'''Label expression.

    ..  container:: example

        **Example 1.** Makes expression to color leaves:

        ::

            >>> expression = label()
            >>> expression = expression.color_leaves()

        ::

            >>> staff = Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
            >>> expression(staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                <c' bf'>8
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                <g' a'>4
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                af'8 ~
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                af'8
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                gf'8 ~
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                gf'4
            }

    ..  container:: example

        **Example 2.** Makes expression to color note note heads:

        ::

            >>> expression = label()
            >>> expression = expression.color_note_heads()

        ::

            >>> staff = Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
            >>> expression(staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                <c' bf'>8
                <g' a'>4
                \once \override NoteHead.color = #(x11-color 'DarkOrange)
                af'8 ~
                \once \override NoteHead.color = #(x11-color 'DarkOrange)
                af'8
                \once \override NoteHead.color = #(x11-color 'firebrick)
                gf'8 ~
                \once \override NoteHead.color = #(x11-color 'firebrick)
                gf'4
            }

    ..  container:: example

        **Example 3.** Makes expression to label logical ties with durations:

        ::

            >>> expression = label()
            >>> expression = expression.with_durations(preferred_denominator=8)

        ::

            >>> staff = Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
            >>> expression(staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                <c' bf'>8
                    ^ \markup {
                        \small
                            1/8
                        }
                <g' a'>4
                    ^ \markup {
                        \small
                            2/8
                        }
                af'8 ~
                    ^ \markup {
                        \small
                            2/8
                        }
                af'8
                gf'8 ~
                    ^ \markup {
                        \small
                            3/8
                        }
                gf'4
            }

    ..  container:: example

        **Example 4.** Makes expression to label logical ties with indices:

        ::

            >>> expression = label()
            >>> expression = expression.with_indices()

        ::

            >>> staff = Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
            >>> expression(staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                <c' bf'>8
                    ^ \markup {
                        \small
                            0
                        }
                <g' a'>4
                    ^ \markup {
                        \small
                            1
                        }
                af'8 ~
                    ^ \markup {
                        \small
                            2
                        }
                af'8
                gf'8 ~
                    ^ \markup {
                        \small
                            3
                        }
                gf'4
            }

    ..  container:: example

        **Example 5.** Makes expression to label leaves with indices:

        ::

            >>> expression = label()
            >>> expression = expression.with_indices(prototype=scoretools.Leaf)

        ::

            >>> staff = Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
            >>> expression(staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                <c' bf'>8
                    ^ \markup {
                        \small
                            0
                        }
                <g' a'>4
                    ^ \markup {
                        \small
                            1
                        }
                af'8 ~
                    ^ \markup {
                        \small
                            2
                        }
                af'8
                    ^ \markup {
                        \small
                            3
                        }
                gf'8 ~
                    ^ \markup {
                        \small
                            4
                        }
                gf'4
                    ^ \markup {
                        \small
                            5
                        }
            }

    ..  container:: example

        **Example 6.** Makes expression to label consecutive notes with named
        intervals:

        ::

            >>> expression = label()
            >>> expression = expression.with_intervals()

        ::

            >>> staff = Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
            >>> expression(staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                <c' bf'>8
                <g' a'>4
                af'8 ~ ^ \markup { P1 }
                af'8 ^ \markup { -M2 }
                gf'8 ~ ^ \markup { P1 }
                gf'4
            }

    ..  container:: example

        **Example 7.** Makes expression to label logical ties with start
        offsets:

        ::

            >>> expression = label()
            >>> expression = expression.with_start_offsets()

        ::

            >>> staff = Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
            >>> expression(staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                <c' bf'>8 ^ \markup { 0 }
                <g' a'>4 ^ \markup { 1/8 }
                af'8 ~ ^ \markup { 3/8 }
                af'8
                gf'8 ~ ^ \markup { 5/8 }
                gf'4
            }

    ..  container:: example

        **Example 8.** Makes expression to label logical ties with pitch names:

        ::

            >>> expression = label()
            >>> expression = expression.with_pitches()

        ::

            >>> staff = Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4")
            >>> expression(staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                <c' bf'>8
                    ^ \markup {
                        \small
                            \column
                                {
                                    bf'
                                    c'
                                }
                        }
                <g' a'>4
                    ^ \markup {
                        \small
                            \column
                                {
                                    a'
                                    g'
                                }
                        }
                af'8 ~
                    ^ \markup {
                        \small
                            af'
                        }
                af'8
                gf'8 ~
                    ^ \markup {
                        \small
                            gf'
                        }
                gf'4
            }

    ..  note:: Add usage examples to this docstring. Do not add
        usage examples to property and method docstrings. Properties
        and methods will all be derived automatically from the LabeAgent class
        at some point in future.

    Initializer returns expression.

    Expression returns none.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __call__(self, expr=None):
        r'''Calls label expression on `expr`.

        Makes label agent with `expr` as client.

        Applies callbacks to label agent client.

        Operates in place on label agent client.

        Returns none.
        '''
        from abjad.tools import agenttools
        if expr is None:
            return
        agent = agenttools.LabelAgent(expr)
        callbacks = self.callbacks or ()
        for callback in callbacks:
            callback(agent)

    ### PUBLIC METHODS ###

    def color_container(self, color='red'):
        r'''Make color-container callback.

        Returns callback.
        '''
        arguments = {
            'color': color,
            }
        return self._make_callback(
            'agenttools.LabelAgent.color_container',
            arguments,
            )

    def color_leaves(self, color='red'):
        r'''Makes color-leaves callback.

        Returns callback.
        '''
        arguments = {
            'color': color,
            }
        return self._make_callback(
            'agenttools.LabelAgent.color_leaves',
            arguments,
            )

    def color_note_heads(self, color_map=None):
        r'''Makes color-note-heads callback.

        Returns callback.
        '''
        arguments = {
            'color_map': color_map,
            }
        return self._make_callback(
            'agenttools.LabelAgent.color_note_heads',
            arguments,
            )

    def remove_markup(self):
        r'''Makes remove-markup callback.

        Returns callback.
        '''
        return self._make_callback('agenttools.LabelAgent.remove_markup')

    def vertical_moments(self, direction=Up, prototype=None):
        r'''Makes vertical-moments callback.

        Returns callback.
        '''
        arguments = {
            'direction': direction,
            'prototype': prototype,
            }
        return self._make_callback(
            'agenttools.LabelAgent.vertical_moments',
            arguments,
            )

    def with_durations(self, direction=Up, preferred_denominator=None):
        r'''Makes with-durations callback.

        Returns callback.
        '''
        arguments = {
            'direction': direction,
            'preferred_denominator': preferred_denominator,
            }
        return self._make_callback(
            'agenttools.LabelAgent.with_durations',
            arguments,
            )

    def with_indices(self, direction=Up, prototype=None):
        r'''Makes with-indices callback.

        Returns callback.
        '''
        arguments = {
            'direction': direction,
            'prototype': prototype,
            }
        return self._make_callback(
            'agenttools.LabelAgent.with_indices',
            arguments,
            )

    def with_intervals(self, direction=Up, prototype=None):
        r'''Makes with-intervals callback.

        Returns callback.
        '''
        arguments = {
            'direction': direction,
            'prototype': prototype,
            }
        return self._make_callback(
            'agenttools.LabelAgent.with_intervals',
            arguments,
            )

    def with_pitches(self, direction=Up, prototype=None):
        r'''Makes with-pitches callback.

        Returns callback.
        '''
        arguments = {
            'direction': direction,
            'prototype': prototype,
            }
        return self._make_callback(
            'agenttools.LabelAgent.with_pitches',
            arguments,
            )

    def with_start_offsets(
        self,
        clock_time=False,
        direction=Up,
        font_size=None,
        ):
        r'''Makes with-start-offsets callback.

        Returns callback.
        '''
        arguments = {
            'clock_time': clock_time,
            'direction': direction,
            'font_size': font_size,
            }
        return self._make_callback(
            'agenttools.LabelAgent.with_start_offsets',
            arguments,
            )
