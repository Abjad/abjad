# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class LabelExpression(AbjadObject):
    r'''A label expression.

    ..  container:: example

        **Example 1.** Colors leaves:

        ::

            >>> expression = expressiontools.LabelExpression()
            >>> expression = expression.color_leaves()

        ::

            >>> staff = Staff("<c' bf'>8 <g' a'>4 af'8 ~ af'8 gf'8 ~ gf'4") 
            >>> expression(staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \once \override Accidental #'color = #red
                \once \override Beam #'color = #red
                \once \override Dots #'color = #red
                \once \override NoteHead #'color = #red
                \once \override Stem #'color = #red
                <c' bf'>8
                \once \override Accidental #'color = #red
                \once \override Beam #'color = #red
                \once \override Dots #'color = #red
                \once \override NoteHead #'color = #red
                \once \override Stem #'color = #red
                <g' a'>4
                \once \override Accidental #'color = #red
                \once \override Beam #'color = #red
                \once \override Dots #'color = #red
                \once \override NoteHead #'color = #red
                \once \override Stem #'color = #red
                af'8 ~
                \once \override Accidental #'color = #red
                \once \override Beam #'color = #red
                \once \override Dots #'color = #red
                \once \override NoteHead #'color = #red
                \once \override Stem #'color = #red
                af'8
                \once \override Accidental #'color = #red
                \once \override Beam #'color = #red
                \once \override Dots #'color = #red
                \once \override NoteHead #'color = #red
                \once \override Stem #'color = #red
                gf'8 ~
                \once \override Accidental #'color = #red
                \once \override Beam #'color = #red
                \once \override Dots #'color = #red
                \once \override NoteHead #'color = #red
                \once \override Stem #'color = #red
                gf'4
            }

    ..  container:: example

        **Example 2.** Colors note note heads:

        ::

            >>> expression = expressiontools.LabelExpression()
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
                \once \override NoteHead #'color = #(x11-color 'DarkOrange)
                af'8 ~
                \once \override NoteHead #'color = #(x11-color 'DarkOrange)
                af'8
                \once \override NoteHead #'color = #(x11-color 'firebrick)
                gf'8 ~
                \once \override NoteHead #'color = #(x11-color 'firebrick)
                gf'4
            }

    ..  container:: example

        **Example 3.** Labels logical ties with durations:

        ::

            >>> expression = expressiontools.LabelExpression()
            >>> expression = expression.with_durations()

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
                            1/4
                        }
                af'8 ~
                    ^ \markup {
                        \small
                            1/4
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

        **Example 4.** Labels logical ties with indices:

        ::

            >>> expression = expressiontools.LabelExpression()
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

        **Example 5.** Labels consecutive notes with named intervals:

        ::

            >>> expression = expressiontools.LabelExpression()
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

        **Example 6.** Labels logical ties with start offsets:

        ::

            >>> expression = expressiontools.LabelExpression()
            >>> expression = expression.with_start_offsets()

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
                            1/8
                        }
                af'8 ~
                    ^ \markup {
                        \small
                            3/8
                        }
                af'8
                gf'8 ~
                    ^ \markup {
                        \small
                            5/8
                        }
                gf'4
            }

    ..  container:: example

        **Example 7.** Labels logical ties with pitch names:

        ::

            >>> expression = expressiontools.LabelExpression()
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

    __documentation_section__ = 'Expressions'

    __slots__ = (
        '_callbacks',
        )

    ### INITIALIZER ###

    def __init__(self, callbacks=None):
        if callbacks is not None:
            callbacks = tuple(callbacks)
        self._callbacks = callbacks

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

    ### PRIVATE METHODS ###

    def _append_callback(self, callback):
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def _make_callback(self, name, keywords=None):
        from abjad.tools import expressiontools
        callback = expressiontools.Callback(
            name=name,
            keywords=keywords,
            )
        return self._append_callback(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        r'''Gets callbacks.

        Returns tuple or none.
        '''
        return self._callbacks

    ### PUBLIC METHODS ###

    def color_container(self, color='red'):
        r'''Colors contents of container.
        '''
        keywords = {
            'color': color,
            }
        return self._make_callback(
            'agenttools.LabelAgent.color_container', 
            keywords,
            )

    def color_leaves(self, color='red'):
        r'''Colors leaves.
        '''
        keywords = {
            'color': color,
            }
        return self._make_callback(
            'agenttools.LabelAgent.color_leaves', 
            keywords,
            )

    def color_note_heads(self, color_map=None):
        r'''Colors note note heads by `color_map`.
        '''
        keywords = {
            'color_map': color_map,
            }
        return self._make_callback(
            'agenttools.LabelAgent.color_note_heads', 
            keywords,
            )

    def remove_markup(self):
        r'''Removes markup from leaves.
        '''
        return self._make_callback('agenttools.LabelAgent.remove_markup')

    def vertical_moments(self, direction=Up, prototype=None):
        r'''Labels vertical moments.
        '''
        keywords = {
            'direction': direction,
            'prototype': prototype,
            }
        return self._make_callback(
            'agenttools.LabelAgent.vertical_moments', 
            keywords,
            )

    def with_durations(self, direction=Up):
        r'''Labels durations.
        '''
        keywords = {
            'direction': direction,
            }
        return self._make_callback(
            'agenttools.LabelAgent.with_durations', 
            keywords,
            )

    def with_indices(self, direction=Up, prototype=None):
        r'''Labels indices.
        '''
        keywords = {
            'direction': direction,
            'prototype': prototype,
            }
        return self._make_callback(
            'agenttools.LabelAgent.with_indices', 
            keywords,
            )

    def with_intervals(self, direction=Up, prototype=None):
        r'''Labels intervals.
        '''
        keywords = {
            'direction': direction,
            'prototype': prototype,
            }
        return self._make_callback(
            'agenttools.LabelAgent.with_intervals', 
            keywords,
            )

    def with_pitches(self, direction=Up, prototype=None):
        r'''Labels pitches.
        '''
        keywords = {
            'direction': direction,
            'prototype': prototype,
            }
        return self._make_callback(
            'agenttools.LabelAgent.with_pitches', 
            keywords,
            )

    def with_start_offsets(self, direction=Up):
        r'''Labels offsets.
        '''
        keywords = {
            'direction': direction,
            }
        return self._make_callback(
            'agenttools.LabelAgent.with_start_offsets', 
            keywords,
            )