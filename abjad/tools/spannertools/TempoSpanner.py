# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import lilypondnametools
from abjad.tools import markuptools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import new


class TempoSpanner(Spanner):
    r'''Tempo spanner.

    ..  container:: example

        **Example 1.** With tempo indicators only:

        ::

            >>> staff = Staff("c'8. d' e'4. g'8. f' ef'4.")
            >>> attach(TimeSignature((3, 8)), staff)
            >>> score = Score([staff])

        ::

            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[0], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 90)
            >>> attach(tempo, staff[2], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 72)
            >>> attach(tempo, staff[3], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[5], is_annotation=True)

        ::

            >>> attach(spannertools.TempoSpanner(), staff[:])

        ::

            >>> override(score).text_script.staff_padding = 2.25

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript.staff-padding = #2.25
            } <<
                \new Staff {
                    \time 3/8
                    c'8. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        }
                    d'8.
                    e'4. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                90
                            }
                        }
                    g'8. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                72
                            }
                        }
                    f'8.
                    ef'4. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        }
                }
            >>

    ..  container:: example

        **Example 2.** With an accelerando:

        ::

            >>> staff = Staff("c'8. d' e'4. g'8. f' ef'4.")
            >>> attach(TimeSignature((3, 8)), staff)
            >>> score = Score([staff])

        ::

            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[0], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 90)
            >>> attach(tempo, staff[2], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 72)
            >>> attach(tempo, staff[3], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[5], is_annotation=True)

        ::

            >>> accelerando = indicatortools.Accelerando()
            >>> attach(accelerando, staff[0], is_annotation=True)

        ::

            >>> attach(spannertools.TempoSpanner(), staff[:])

        ::

            >>> override(score).text_script.staff_padding = 2.25
            >>> override(score).text_spanner.staff_padding = 3

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript.staff-padding = #2.25
                \override TextSpanner.staff-padding = #3
            } <<
                \new Staff {
                    \time 3/8
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        accel.
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        \hspace
                            #1.25
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 2
                    \once \override TextSpanner.bound-details.right.text = ##f
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    c'8. \startTextSpan
                    d'8.
                    e'4. \stopTextSpan ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                90
                            }
                        }
                    g'8. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                72
                            }
                        }
                    f'8.
                    ef'4. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        }
                }
            >>

    ..  container:: example

        **Example 3.** With a ritardando:

        ::

            >>> staff = Staff("c'8. d' e'4. g'8. f' ef'4.")
            >>> attach(TimeSignature((3, 8)), staff)
            >>> score = Score([staff])

        ::

            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[0], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 90)
            >>> attach(tempo, staff[2], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 72)
            >>> attach(tempo, staff[3], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[5], is_annotation=True)

        ::

            >>> ritardando = indicatortools.Ritardando()
            >>> attach(ritardando, staff[3], is_annotation=True)

        ::

            >>> attach(spannertools.TempoSpanner(), staff[:])

        ::

            >>> override(score).text_script.staff_padding = 2.25
            >>> override(score).text_spanner.staff_padding = 3

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript.staff-padding = #2.25
                \override TextSpanner.staff-padding = #3
            } <<
                \new Staff {
                    \time 3/8
                    c'8. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        }
                    d'8.
                    e'4. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                90
                            }
                        }
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        rit.
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                72
                            }
                        \hspace
                            #1.25
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 2
                    \once \override TextSpanner.bound-details.right.text = ##f
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    g'8. \startTextSpan
                    f'8.
                    ef'4. \stopTextSpan ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        }
                }
            >>

    ..  container:: example

        **Example 4.** With both an accelerando and a ritardando:

        ::

            >>> staff = Staff("c'8. d' e'4. g'8. f' ef'4.")
            >>> attach(TimeSignature((3, 8)), staff)
            >>> score = Score([staff])

        ::

            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[0], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 90)
            >>> attach(tempo, staff[2], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 72)
            >>> attach(tempo, staff[3], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[5], is_annotation=True)

        ::

            >>> accelerando = indicatortools.Accelerando()
            >>> attach(accelerando, staff[0], is_annotation=True)
            >>> ritardando = indicatortools.Ritardando()
            >>> attach(ritardando, staff[3], is_annotation=True)

        ::

            >>> attach(spannertools.TempoSpanner(), staff[:])

        ::

            >>> override(score).text_script.staff_padding = 2.25
            >>> override(score).text_spanner.staff_padding = 3

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript.staff-padding = #2.25
                \override TextSpanner.staff-padding = #3
            } <<
                \new Staff {
                    \time 3/8
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        accel.
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        \hspace
                            #1.25
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 2
                    \once \override TextSpanner.bound-details.right.text = ##f
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    c'8. \startTextSpan
                    d'8.
                    e'4. \stopTextSpan ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                90
                            }
                        }
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        rit.
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                72
                            }
                        \hspace
                            #1.25
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 2
                    \once \override TextSpanner.bound-details.right.text = ##f
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    g'8. \startTextSpan
                    f'8.
                    ef'4. \stopTextSpan ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        }
                }
            >>

    ..  container:: example

        **Example 5.** Implicit start to (music-initial) accelerando:

        ::

            >>> staff = Staff("c'8. d' e'4. g'8. f' ef'4.")
            >>> attach(TimeSignature((3, 8)), staff)
            >>> score = Score([staff])

        ::

            >>> tempo = Tempo(Duration(1, 4), 90)
            >>> attach(tempo, staff[2], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 72)
            >>> attach(tempo, staff[3], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[5], is_annotation=True)

        ::

            >>> accelerando = indicatortools.Accelerando()
            >>> attach(accelerando, staff[0], is_annotation=True)

        ::

            >>> attach(spannertools.TempoSpanner(), staff[:])

        ::

            >>> override(score).text_script.staff_padding = 2.25
            >>> override(score).text_spanner.staff_padding = 3

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript.staff-padding = #2.25
                \override TextSpanner.staff-padding = #3
            } <<
                \new Staff {
                    \time 3/8
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        accel.
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \large
                            \upright
                                accel.
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 2
                    \once \override TextSpanner.bound-details.right.text = ##f
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    c'8. \startTextSpan
                    d'8.
                    e'4. \stopTextSpan ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                90
                            }
                        }
                    g'8. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                72
                            }
                        }
                    f'8.
                    ef'4. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        }
                }
            >>

    ..  container:: example

        **Example 6.** Implicit start to (music-initial) ritardando:

        ::

            >>> staff = Staff("c'8. d' e'4. g'8. f' ef'4.")
            >>> attach(TimeSignature((3, 8)), staff)
            >>> score = Score([staff])

        ::

            >>> tempo = Tempo(Duration(1, 4), 90)
            >>> attach(tempo, staff[2], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 72)
            >>> attach(tempo, staff[3], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[5], is_annotation=True)

        ::

            >>> ritardando = indicatortools.Ritardando()
            >>> attach(ritardando, staff[0], is_annotation=True)

        ::

            >>> attach(spannertools.TempoSpanner(), staff[:])

        ::

            >>> override(score).text_script.staff_padding = 2.25
            >>> override(score).text_spanner.staff_padding = 3

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript.staff-padding = #2.25
                \override TextSpanner.staff-padding = #3
            } <<
                \new Staff {
                    \time 3/8
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        rit.
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \large
                            \upright
                                rit.
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 2
                    \once \override TextSpanner.bound-details.right.text = ##f
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    c'8. \startTextSpan
                    d'8.
                    e'4. \stopTextSpan ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                90
                            }
                        }
                    g'8. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                72
                            }
                        }
                    f'8.
                    ef'4. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        }
                }
            >>

    ..  container:: example

        **Example 7.** Implicit start to (midmusic) accelerando:

        ::

            >>> staff = Staff("c'8. d' e'4. g'8. f' ef'4.")
            >>> attach(TimeSignature((3, 8)), staff)
            >>> score = Score([staff])

        ::

            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[0], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 90)
            >>> attach(tempo, staff[2], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 120)
            >>> attach(tempo, staff[5], is_annotation=True)

        ::

            >>> accelerando = indicatortools.Accelerando()
            >>> attach(accelerando, staff[3], is_annotation=True)

        ::

            >>> tempo_spanner = spannertools.TempoSpanner(
            ...     start_with_parenthesized_tempo=True,
            ...     )
            >>> attach(tempo_spanner, staff[:])

        ::

            >>> override(score).text_script.staff_padding = 2.25
            >>> override(score).text_spanner.staff_padding = 3

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript.staff-padding = #2.25
                \override TextSpanner.staff-padding = #3
            } <<
                \new Staff {
                    \time 3/8
                    c'8. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        }
                    d'8.
                    e'4. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                90
                            }
                        }
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        accel.
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \line
                                    {
                                        \fontsize
                                            #-6
                                            \general-align
                                                #Y
                                                #DOWN
                                                \note-by-number
                                                    #2
                                                    #0
                                                    #1
                                        \upright
                                            {
                                                =
                                                90
                                            }
                                    }
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 2
                    \once \override TextSpanner.bound-details.right.text = ##f
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    g'8. \startTextSpan
                    f'8.
                    ef'4. \stopTextSpan ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                120
                            }
                        }
                }
            >>

    ..  container:: example

        **Example 8.** Implicit start to (midmusic) ritardando:

        ::

            >>> staff = Staff("c'8. d' e'4. g'8. f' ef'4.")
            >>> attach(TimeSignature((3, 8)), staff)
            >>> score = Score([staff])

        ::

            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[0], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 90)
            >>> attach(tempo, staff[2], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[5], is_annotation=True)

        ::

            >>> ritardando = indicatortools.Ritardando()
            >>> attach(ritardando, staff[3], is_annotation=True)

        ::

            >>> tempo_spanner = spannertools.TempoSpanner(
            ...     start_with_parenthesized_tempo=True,
            ...     )
            >>> attach(tempo_spanner, staff[:])

        ::

            >>> override(score).text_script.staff_padding = 2.25
            >>> override(score).text_spanner.staff_padding = 3

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript.staff-padding = #2.25
                \override TextSpanner.staff-padding = #3
            } <<
                \new Staff {
                    \time 3/8
                    c'8. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        }
                    d'8.
                    e'4. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                90
                            }
                        }
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        rit.
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \line
                                    {
                                        \fontsize
                                            #-6
                                            \general-align
                                                #Y
                                                #DOWN
                                                \note-by-number
                                                    #2
                                                    #0
                                                    #1
                                        \upright
                                            {
                                                =
                                                90
                                            }
                                    }
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 2
                    \once \override TextSpanner.bound-details.right.text = ##f
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    g'8. \startTextSpan
                    f'8.
                    ef'4. \stopTextSpan ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        }
                }
            >>

    ..  container:: example

        **Example 9.** With an accelerando over a line break:

        ::

            >>> staff = Staff("c'4. d' e' f' g' a' b' c''")
            >>> attach(TimeSignature((3, 8)), staff)
            >>> score = Score([staff])
            >>> command = indicatortools.LilyPondCommand('break', 'after')
            >>> attach(command, staff[3])

        ::

            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[2], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 90)
            >>> attach(tempo, staff[6], is_annotation=True)

        ::

            >>> accelerando = indicatortools.Accelerando()
            >>> attach(accelerando, staff[2], is_annotation=True)

        ::

            >>> attach(spannertools.TempoSpanner(), staff[:])

        ::

            >>> override(score).text_script.staff_padding = 2.25
            >>> override(score).text_spanner.staff_padding = 3

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript.staff-padding = #2.25
                \override TextSpanner.staff-padding = #3
            } <<
                \new Staff {
                    \time 3/8
                    c'4.
                    d'4.
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        accel.
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        \hspace
                            #1.25
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 2
                    \once \override TextSpanner.bound-details.right.text = ##f
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    e'4. \startTextSpan
                    f'4.
                    \break
                    g'4.
                    a'4.
                    b'4. \stopTextSpan ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                90
                            }
                        }
                    c''4.
                }
            >>

    ..  container:: example

        **Example 10.** With a ritardando over a line break:

        ::

            >>> staff = Staff("c'4. d' e' f' g' a' b' c''")
            >>> attach(TimeSignature((3, 8)), staff)
            >>> score = Score([staff])
            >>> command = indicatortools.LilyPondCommand('break', 'after')
            >>> attach(command, staff[3])

        ::

            >>> tempo = Tempo(Duration(1, 4), 90)
            >>> attach(tempo, staff[2], is_annotation=True)
            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> attach(tempo, staff[6], is_annotation=True)

        ::

            >>> ritardando = indicatortools.Ritardando()
            >>> attach(ritardando, staff[2], is_annotation=True)

        ::

            >>> attach(spannertools.TempoSpanner(), staff[:])

        ::

            >>> override(score).text_script.staff_padding = 2.25
            >>> override(score).text_spanner.staff_padding = 3

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript.staff-padding = #2.25
                \override TextSpanner.staff-padding = #3
            } <<
                \new Staff {
                    \time 3/8
                    c'4.
                    d'4.
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        rit.
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                90
                            }
                        \hspace
                            #1.25
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 2
                    \once \override TextSpanner.bound-details.right.text = ##f
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    e'4. \startTextSpan
                    f'4.
                    \break
                    g'4.
                    a'4.
                    b'4. \stopTextSpan ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        }
                    c''4.
                }
            >>

    ..  container:: example

        **Example 11.** With a metric modulation:

        ::

            >>> staff = Staff("c'8. d'8. e'4. g'8. f'8. ef'4.")
            >>> attach(TimeSignature((3, 8)), staff)
            >>> score = Score([staff])

        ::

            >>> tempo = Tempo(Duration(3, 4), 90)
            >>> attach(tempo, staff[0], is_annotation=True)
            >>> tempo = Tempo(Duration(3, 4), 60)
            >>> attach(tempo, staff[3], is_annotation=True)
            >>> metric_modulation = indicatortools.MetricModulation(
            ...     left_rhythm=Note('c4.'),
            ...     right_rhythm=Note('c4'),
            ...     )
            >>> attach(metric_modulation, staff[3], is_annotation=True)

        ::

            >>> attach(spannertools.TempoSpanner(), staff[:])

        ::

            >>> override(score).text_script.staff_padding = 2.25
            >>> override(score).text_spanner.staff_padding = 3

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript.staff-padding = #2.25
                \override TextSpanner.staff-padding = #3
            } <<
                \new Staff {
                    \time 3/8
                    c'8. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #1
                                    #1
                        \upright
                            {
                                =
                                90
                            }
                        }
                    d'8.
                    e'4.
                    g'8. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #1
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        \hspace
                            #0.5
                        \general-align
                            #Y
                            #DOWN
                            \override
                                #'(padding . 0.5)
                                \parenthesize
                                    \line
                                        {
                                            \scale
                                                #'(0.5 . 0.5)
                                                \score
                                                    {
                                                        \new Score \with {
                                                            \override SpacingSpanner.spacing-increment = #0.5
                                                            proportionalNotationDuration = ##f
                                                        } <<
                                                            \new RhythmicStaff \with {
                                                                \remove Time_signature_engraver
                                                                \remove Staff_symbol_engraver
                                                                \override Stem.direction = #up
                                                                \override Stem.length = #5
                                                                \override TupletBracket.bracket-visibility = ##t
                                                                \override TupletBracket.direction = #up
                                                                \override TupletBracket.padding = #1.25
                                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                                tupletFullLength = ##t
                                                            } {
                                                                c4.
                                                            }
                                                        >>
                                                        \layout {
                                                            indent = #0
                                                            ragged-right = ##t
                                                        }
                                                    }
                                            =
                                            \hspace
                                                #-0.5
                                            \scale
                                                #'(0.5 . 0.5)
                                                \score
                                                    {
                                                        \new Score \with {
                                                            \override SpacingSpanner.spacing-increment = #0.5
                                                            proportionalNotationDuration = ##f
                                                        } <<
                                                            \new RhythmicStaff \with {
                                                                \remove Time_signature_engraver
                                                                \remove Staff_symbol_engraver
                                                                \override Stem.direction = #up
                                                                \override Stem.length = #5
                                                                \override TupletBracket.bracket-visibility = ##t
                                                                \override TupletBracket.direction = #up
                                                                \override TupletBracket.padding = #1.25
                                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                                tupletFullLength = ##t
                                                            } {
                                                                c4
                                                            }
                                                        >>
                                                        \layout {
                                                            indent = #0
                                                            ragged-right = ##t
                                                        }
                                                    }
                                        }
                        }
                    f'8.
                    ef'4.
                }
            >>

    ..  container:: example

        **Example 12.** With a metric modulation and an accelerando:

        ::

            >>> staff = Staff("c'8. d'8. e'4. g'8. f'8. ef'4.")
            >>> attach(TimeSignature((3, 8)), staff)
            >>> score = Score([staff])

        ::

            >>> tempo = Tempo(Duration(3, 4), 90)
            >>> attach(tempo, staff[0], is_annotation=True)
            >>> tempo = Tempo(Duration(3, 4), 60)
            >>> attach(tempo, staff[3], is_annotation=True)
            >>> metric_modulation = indicatortools.MetricModulation(
            ...     left_rhythm=Note('c4.'),
            ...     right_rhythm=Note('c4'),
            ...     )
            >>> attach(metric_modulation, staff[3], is_annotation=True)
            >>> attach(Accelerando(), staff[3], is_annotation=True)
            >>> tempo = Tempo(Duration(3, 4), 90)
            >>> attach(tempo, staff[-1], is_annotation=True)

        ::

            >>> attach(spannertools.TempoSpanner(), staff[:])

        ::

            >>> override(score).text_script.staff_padding = 2.25
            >>> override(score).text_spanner.staff_padding = 3

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript.staff-padding = #2.25
                \override TextSpanner.staff-padding = #3
            } <<
                \new Staff {
                    \time 3/8
                    c'8. ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #1
                                    #1
                        \upright
                            {
                                =
                                90
                            }
                        }
                    d'8.
                    e'4.
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        accel.
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #1
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        \hspace
                            #0.5
                        \general-align
                            #Y
                            #DOWN
                            \override
                                #'(padding . 0.5)
                                \parenthesize
                                    \line
                                        {
                                            \scale
                                                #'(0.5 . 0.5)
                                                \score
                                                    {
                                                        \new Score \with {
                                                            \override SpacingSpanner.spacing-increment = #0.5
                                                            proportionalNotationDuration = ##f
                                                        } <<
                                                            \new RhythmicStaff \with {
                                                                \remove Time_signature_engraver
                                                                \remove Staff_symbol_engraver
                                                                \override Stem.direction = #up
                                                                \override Stem.length = #5
                                                                \override TupletBracket.bracket-visibility = ##t
                                                                \override TupletBracket.direction = #up
                                                                \override TupletBracket.padding = #1.25
                                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                                tupletFullLength = ##t
                                                            } {
                                                                c4.
                                                            }
                                                        >>
                                                        \layout {
                                                            indent = #0
                                                            ragged-right = ##t
                                                        }
                                                    }
                                            =
                                            \hspace
                                                #-0.5
                                            \scale
                                                #'(0.5 . 0.5)
                                                \score
                                                    {
                                                        \new Score \with {
                                                            \override SpacingSpanner.spacing-increment = #0.5
                                                            proportionalNotationDuration = ##f
                                                        } <<
                                                            \new RhythmicStaff \with {
                                                                \remove Time_signature_engraver
                                                                \remove Staff_symbol_engraver
                                                                \override Stem.direction = #up
                                                                \override Stem.length = #5
                                                                \override TupletBracket.bracket-visibility = ##t
                                                                \override TupletBracket.direction = #up
                                                                \override TupletBracket.padding = #1.25
                                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                                tupletFullLength = ##t
                                                            } {
                                                                c4
                                                            }
                                                        >>
                                                        \layout {
                                                            indent = #0
                                                            ragged-right = ##t
                                                        }
                                                    }
                                        }
                        \hspace
                            #1.25
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 2
                    \once \override TextSpanner.bound-details.right.text = ##f
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    g'8. \startTextSpan
                    f'8.
                    ef'4. \stopTextSpan ^ \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #1
                                    #1
                        \upright
                            {
                                =
                                90
                            }
                        }
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_left_broken_padding',
        '_left_broken_text',
        '_start_with_parenthesized_tempo',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        left_broken_padding=None,
        left_broken_text=None,
        start_with_parenthesized_tempo=False,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        assert isinstance(left_broken_padding, (int, float, type(None)))
        self._left_broken_padding = left_broken_padding
        prototype = (markuptools.Markup, type(None))
        assert isinstance(left_broken_text, prototype)
        self._left_broken_text = left_broken_text
        assert isinstance(start_with_parenthesized_tempo, (bool, type(None)))
        self._start_with_parenthesized_tempo = start_with_parenthesized_tempo

    ### PRIVATE METHODS ###

    def _combine_tempo_and_metric_modulation(
        self,
        tempo,
        metric_modulation,
        ):
        assert tempo is not None or metric_modulation is not None
        if tempo is None:
            return metric_modulation._get_markup(
                music_scale_pair=(0.5, 0.5),
                )
        if metric_modulation is None:
            return tempo._to_markup()
        tempo_markup = tempo._to_markup()
        tempo_markup = tempo_markup + tempo_markup.hspace(0.5)
        modulation_markup = metric_modulation._get_markup(
            music_scale_pair=(0.5, 0.5),
            )
        modulation_markup = modulation_markup.line()
        modulation_markup = modulation_markup.parenthesize()
        modulation_markup = modulation_markup.override(('padding', 0.5))
        modulation_markup = modulation_markup.general_align('Y', Down)
        markup = tempo_markup + modulation_markup
        return markup

    def _get_annotations(self, leaf):
        inspector = inspect_(leaf)
        tempo = None
        prototype = indicatortools.Tempo,
        if inspector.has_indicator(prototype):
            tempo = inspector.get_indicator(prototype)
        tempo_trend = None
        prototype = (
            indicatortools.Accelerando,
            indicatortools.Ritardando,
            )
        if inspector.has_indicator(prototype):
            tempo_trend = inspector.get_indicator(prototype)
        metric_modulation = None
        prototype = indicatortools.MetricModulation
        if inspector.has_indicator(prototype):
            metric_modulation = inspector.get_indicator(prototype)
        return (
            tempo,
            tempo_trend,
            metric_modulation,
            )

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        current_annotations = self._get_annotations(leaf)
        current_tempo = current_annotations[0]
        current_tempo_trend = current_annotations[1]
        current_metric_modulation = current_annotations[2]
        if current_tempo is None and current_tempo_trend is None:
            return lilypond_format_bundle
        previous_annotations = self._get_previous_annotations(leaf)
        previous_tempo = previous_annotations[0]
        previous_tempo_trend = previous_annotations[1]
        previous_metric_modulation = previous_annotations[2]
        # stop any previous tempo trend
        if previous_tempo_trend:
            spanner_stop = r'\stopTextSpan'
            lilypond_format_bundle.right.spanner_stops.append(spanner_stop)
        # use markup if no tempo trend starts now
        if current_tempo_trend is None:
            markup = self._combine_tempo_and_metric_modulation(
                current_tempo,
                current_metric_modulation,
                )
            markup = new(markup, direction=Up)
            string = format(markup, 'lilypond')
            lilypond_format_bundle.right.markup.append(string)
            return lilypond_format_bundle
        # use spanner if tempo trend starts now
        spanner_start = r'\startTextSpan'
        lilypond_format_bundle.right.spanner_starts.append(spanner_start)
        if current_tempo or current_metric_modulation:
            self._start_tempo_trend_spanner_with_explicit_start(
                leaf,
                lilypond_format_bundle,
                current_tempo,
                current_metric_modulation,
                )
        else:
            self._start_tempo_trend_spanner_with_implicit_start(
                leaf,
                lilypond_format_bundle,
                current_tempo_trend,
                previous_tempo,
                )
        #
        if self.left_broken_text is not None:
            markup = self.left_broken_text
        else:
            markup = current_tempo_trend._to_markup()
            markup = markup.parenthesize()
            markup = markup.override(('padding', 0.45))
            markup = markup + markup.hspace(0.75)
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'left-broken',
                'text',
                ),
            value=markup,
            )
        override_string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        self._make_other_text_spanner_overrides(lilypond_format_bundle)
        return lilypond_format_bundle

    def _get_previous_annotations(self, leaf):
        index = self._index(leaf)
        for index in reversed(range(index)):
            previous_leaf = self[index]
            annotations = self._get_annotations(previous_leaf)
            if any(_ is not None for _ in annotations):
                return annotations
        return None, None, None

    def _make_other_text_spanner_overrides(self, lilypond_format_bundle):
        r'''Alphabetically by property.
        '''
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'arrow-width',
                ),
            value=0.25,
            )
        override_string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'dash-fraction',
                ),
            value=0.25,
            )
        override_string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'dash-period',
                ),
            value=1.5,
            )
        override_string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'left',
                'stencil-align-dir-y',
                ),
            value=-0.5,
            )
        override_string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        if self.left_broken_padding is not None:
            padding = self.left_broken_padding
        else:
            padding = -2
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'left-broken',
                'padding',
                ),
            value=padding,
            )
        override_string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'right',
                'arrow',
                ),
            value=True,
            )
        override_string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'right',
                'padding',
                ),
            value=2,
            )
        override_string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'right',
                'text',
                ),
            value=False,
            )
        override_string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'right-broken',
                'arrow',
                ),
            value=False,
            )
        override_string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'right-broken',
                'padding',
                ),
            value=0,
            )
        override_string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'right-broken',
                'text',
                ),
            value=False,
            )
        override_string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(override_string)

    def _start_tempo_trend_spanner_with_explicit_start(
        self,
        leaf,
        lilypond_format_bundle,
        current_tempo,
        current_metric_modulation,
        ):
        #
        #markup = current_tempo._to_markup()
        markup = self._combine_tempo_and_metric_modulation(
            current_tempo,
            current_metric_modulation,
            )
        markup = markup + markup.hspace(1.25)
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'left',
                'text',
                ),
            value=markup,
            )
        override_string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(override_string)

    def _start_tempo_trend_spanner_with_implicit_start(
        self,
        leaf,
        lilypond_format_bundle,
        current_tempo_trend,
        previous_tempo,
        ):
        #
        if self.start_with_parenthesized_tempo and previous_tempo:
            markup = previous_tempo._to_markup()
            markup = markup.line()
            markup = markup.parenthesize()
            markup = markup.override(('padding', 0.45))
            markup = markup + markup.hspace(0.75)
        else:
            markup = current_tempo_trend._to_markup()
            markup = markup + markup.hspace(0.75)
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'left',
                'text',
                ),
            value=markup,
            )
        override_string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(override_string)

    ### PUBLIC PROPERTIES ###

    @property
    def left_broken_padding(self):
        r'''Gets left broken padding of tempo spanner.

        ..  container:: example

            **Example 1.** With left broken padding set to none:

            ::

                >>> staff = Staff("c'4. d' e' f' g' a' b' c''")
                >>> attach(TimeSignature((3, 8)), staff)
                >>> score = Score([staff])
                >>> command = indicatortools.LilyPondCommand('break', 'after')
                >>> attach(command, staff[3])

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> attach(tempo, staff[2], is_annotation=True)
                >>> tempo = Tempo(Duration(1, 4), 60)
                >>> attach(tempo, staff[6], is_annotation=True)

            ::

                >>> ritardando = indicatortools.Ritardando()
                >>> attach(ritardando, staff[2], is_annotation=True)

            ::

                >>> attach(spannertools.TempoSpanner(), staff[:])

            ::

                >>> override(score).text_script.staff_padding = 2.25
                >>> override(score).text_spanner.staff_padding = 3

            ::

                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> print(format(score))
                \new Score \with {
                    \override TextScript.staff-padding = #2.25
                    \override TextSpanner.staff-padding = #3
                } <<
                    \new Staff {
                        \time 3/8
                        c'4.
                        d'4.
                        \once \override TextSpanner.arrow-width = 0.25
                        \once \override TextSpanner.bound-details.left-broken.padding = -2
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \override
                                #'(padding . 0.45)
                                \parenthesize
                                    \large
                                        \upright
                                            rit.
                            \hspace
                                #0.75
                            }
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                        \once \override TextSpanner.bound-details.left.text = \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    90
                                }
                            \hspace
                                #1.25
                            }
                        \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 2
                        \once \override TextSpanner.bound-details.right.text = ##f
                        \once \override TextSpanner.dash-fraction = 0.25
                        \once \override TextSpanner.dash-period = 1.5
                        e'4. \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        b'4. \stopTextSpan ^ \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    60
                                }
                            }
                        c''4.
                    }
                >>

            Results in padding of ``-2``. (This is default behavior.)

        ..  container:: example

            **Example 2.** With left broken padding set explicitly:

            ::

                >>> staff = Staff("c'4. d' e' f' g' a' b' c''")
                >>> attach(TimeSignature((3, 8)), staff)
                >>> score = Score([staff])
                >>> command = indicatortools.LilyPondCommand('break', 'after')
                >>> attach(command, staff[3])

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> attach(tempo, staff[2], is_annotation=True)
                >>> tempo = Tempo(Duration(1, 4), 60)
                >>> attach(tempo, staff[6], is_annotation=True)

            ::

                >>> ritardando = indicatortools.Ritardando()
                >>> attach(ritardando, staff[2], is_annotation=True)

            ::

                >>> tempo_spanner = spannertools.TempoSpanner(
                ...     left_broken_padding=4,
                ...     )
                >>> attach(tempo_spanner, staff[:])

            ::

                >>> override(score).text_script.staff_padding = 2.25
                >>> override(score).text_spanner.staff_padding = 3

            ::

                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> print(format(score))
                \new Score \with {
                    \override TextScript.staff-padding = #2.25
                    \override TextSpanner.staff-padding = #3
                } <<
                    \new Staff {
                        \time 3/8
                        c'4.
                        d'4.
                        \once \override TextSpanner.arrow-width = 0.25
                        \once \override TextSpanner.bound-details.left-broken.padding = 4
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \override
                                #'(padding . 0.45)
                                \parenthesize
                                    \large
                                        \upright
                                            rit.
                            \hspace
                                #0.75
                            }
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                        \once \override TextSpanner.bound-details.left.text = \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    90
                                }
                            \hspace
                                #1.25
                            }
                        \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 2
                        \once \override TextSpanner.bound-details.right.text = ##f
                        \once \override TextSpanner.dash-fraction = 0.25
                        \once \override TextSpanner.dash-period = 1.5
                        e'4. \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        b'4. \stopTextSpan ^ \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    60
                                }
                            }
                        c''4.
                    }
                >>

        Returns number or none.
        '''
        return self._left_broken_padding

    @property
    def left_broken_text(self):
        r'''Gets left broken text of tempo spanner.

        ..  container:: example

            **Example 1.** With left broken text set to none:

            ::

                >>> staff = Staff("c'4. d' e' f' g' a' b' c''")
                >>> attach(TimeSignature((3, 8)), staff)
                >>> score = Score([staff])
                >>> command = indicatortools.LilyPondCommand('break', 'after')
                >>> attach(command, staff[3])

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> attach(tempo, staff[2], is_annotation=True)
                >>> tempo = Tempo(Duration(1, 4), 60)
                >>> attach(tempo, staff[6], is_annotation=True)

            ::

                >>> ritardando = indicatortools.Ritardando()
                >>> attach(ritardando, staff[2], is_annotation=True)

            ::

                >>> attach(spannertools.TempoSpanner(), staff[:])

            ::

                >>> override(score).text_script.staff_padding = 2.25
                >>> override(score).text_spanner.staff_padding = 3

            ::

                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> print(format(score))
                \new Score \with {
                    \override TextScript.staff-padding = #2.25
                    \override TextSpanner.staff-padding = #3
                } <<
                    \new Staff {
                        \time 3/8
                        c'4.
                        d'4.
                        \once \override TextSpanner.arrow-width = 0.25
                        \once \override TextSpanner.bound-details.left-broken.padding = -2
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \override
                                #'(padding . 0.45)
                                \parenthesize
                                    \large
                                        \upright
                                            rit.
                            \hspace
                                #0.75
                            }
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                        \once \override TextSpanner.bound-details.left.text = \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    90
                                }
                            \hspace
                                #1.25
                            }
                        \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 2
                        \once \override TextSpanner.bound-details.right.text = ##f
                        \once \override TextSpanner.dash-fraction = 0.25
                        \once \override TextSpanner.dash-period = 1.5
                        e'4. \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        b'4. \stopTextSpan ^ \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    60
                                }
                            }
                        c''4.
                    }
                >>

            Results in parenthesized abbreviation after line break.
            (This is default behavior.)

        ..  container:: example

            **Example 2.** With left broken text set explicitly:

            ::

                >>> staff = Staff("c'4. d' e' f' g' a' b' c''")
                >>> attach(TimeSignature((3, 8)), staff)
                >>> score = Score([staff])
                >>> command = indicatortools.LilyPondCommand('break', 'after')
                >>> attach(command, staff[3])

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> attach(tempo, staff[2], is_annotation=True)
                >>> tempo = Tempo(Duration(1, 4), 60)
                >>> attach(tempo, staff[6], is_annotation=True)

            ::

                >>> ritardando = indicatortools.Ritardando()
                >>> attach(ritardando, staff[2], is_annotation=True)

            ::

                >>> null_markup = Markup.null(direction=None)
                >>> tempo_spanner = spannertools.TempoSpanner(
                ...     left_broken_text=null_markup,
                ...     )
                >>> attach(tempo_spanner, staff[:])

            ::

                >>> override(score).text_script.staff_padding = 2.25
                >>> override(score).text_spanner.staff_padding = 3

            ::

                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> print(format(score))
                \new Score \with {
                    \override TextScript.staff-padding = #2.25
                    \override TextSpanner.staff-padding = #3
                } <<
                    \new Staff {
                        \time 3/8
                        c'4.
                        d'4.
                        \once \override TextSpanner.arrow-width = 0.25
                        \once \override TextSpanner.bound-details.left-broken.padding = -2
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \null
                            }
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                        \once \override TextSpanner.bound-details.left.text = \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    90
                                }
                            \hspace
                                #1.25
                            }
                        \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 2
                        \once \override TextSpanner.bound-details.right.text = ##f
                        \once \override TextSpanner.dash-fraction = 0.25
                        \once \override TextSpanner.dash-period = 1.5
                        e'4. \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        b'4. \stopTextSpan ^ \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    60
                                }
                            }
                        c''4.
                    }
                >>

            Results in null left broken text.

        Returns markup or none.
        '''
        return self._left_broken_text

    @property
    def start_with_parenthesized_tempo(self):
        r'''Is true when spanner should start with parenthesized tempo.

        ..  container:: example

            **Example 1.** Does not start with parenthesized tempo:

            ::

                >>> staff = Staff("c'8. d' e'4. g'8. f' ef'4.")
                >>> attach(TimeSignature((3, 8)), staff)
                >>> score = Score([staff])

            ::

                >>> tempo = Tempo(Duration(1, 4), 60)
                >>> attach(tempo, staff[0], is_annotation=True)
                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> attach(tempo, staff[2], is_annotation=True)
                >>> tempo = Tempo(Duration(1, 4), 120)
                >>> attach(tempo, staff[5], is_annotation=True)

            ::

                >>> accelerando = indicatortools.Accelerando()
                >>> attach(accelerando, staff[3], is_annotation=True)

            ::

                >>> tempo_spanner = spannertools.TempoSpanner(
                ...     start_with_parenthesized_tempo=False,
                ...     )
                >>> attach(tempo_spanner, staff[:])

            ::

                >>> override(score).text_script.staff_padding = 2.25
                >>> override(score).text_spanner.staff_padding = 3

            ::

                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> print(format(score))
                \new Score \with {
                    \override TextScript.staff-padding = #2.25
                    \override TextSpanner.staff-padding = #3
                } <<
                    \new Staff {
                        \time 3/8
                        c'8. ^ \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    60
                                }
                            }
                        d'8.
                        e'4. ^ \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    90
                                }
                            }
                        \once \override TextSpanner.arrow-width = 0.25
                        \once \override TextSpanner.bound-details.left-broken.padding = -2
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \override
                                #'(padding . 0.45)
                                \parenthesize
                                    \large
                                        \upright
                                            accel.
                            \hspace
                                #0.75
                            }
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                        \once \override TextSpanner.bound-details.left.text = \markup {
                            \large
                                \upright
                                    accel.
                            \hspace
                                #0.75
                            }
                        \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 2
                        \once \override TextSpanner.bound-details.right.text = ##f
                        \once \override TextSpanner.dash-fraction = 0.25
                        \once \override TextSpanner.dash-period = 1.5
                        g'8. \startTextSpan
                        f'8.
                        ef'4. \stopTextSpan ^ \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    120
                                }
                            }
                    }
                >>

        ..  container:: example

            **Example 2.** Starts with parenthesized tempo:

            ::

                >>> staff = Staff("c'8. d' e'4. g'8. f' ef'4.")
                >>> attach(TimeSignature((3, 8)), staff)
                >>> score = Score([staff])

            ::

                >>> tempo = Tempo(Duration(1, 4), 60)
                >>> attach(tempo, staff[0], is_annotation=True)
                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> attach(tempo, staff[2], is_annotation=True)
                >>> tempo = Tempo(Duration(1, 4), 120)
                >>> attach(tempo, staff[5], is_annotation=True)

            ::

                >>> accelerando = indicatortools.Accelerando()
                >>> attach(accelerando, staff[3], is_annotation=True)

            ::

                >>> tempo_spanner = spannertools.TempoSpanner(
                ...     start_with_parenthesized_tempo=True,
                ...     )
                >>> attach(tempo_spanner, staff[:])

            ::

                >>> override(score).text_script.staff_padding = 2.25
                >>> override(score).text_spanner.staff_padding = 3

            ::

                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> print(format(score))
                \new Score \with {
                    \override TextScript.staff-padding = #2.25
                    \override TextSpanner.staff-padding = #3
                } <<
                    \new Staff {
                        \time 3/8
                        c'8. ^ \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    60
                                }
                            }
                        d'8.
                        e'4. ^ \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    90
                                }
                            }
                        \once \override TextSpanner.arrow-width = 0.25
                        \once \override TextSpanner.bound-details.left-broken.padding = -2
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \override
                                #'(padding . 0.45)
                                \parenthesize
                                    \large
                                        \upright
                                            accel.
                            \hspace
                                #0.75
                            }
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                        \once \override TextSpanner.bound-details.left.text = \markup {
                            \override
                                #'(padding . 0.45)
                                \parenthesize
                                    \line
                                        {
                                            \fontsize
                                                #-6
                                                \general-align
                                                    #Y
                                                    #DOWN
                                                    \note-by-number
                                                        #2
                                                        #0
                                                        #1
                                            \upright
                                                {
                                                    =
                                                    90
                                                }
                                        }
                            \hspace
                                #0.75
                            }
                        \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 2
                        \once \override TextSpanner.bound-details.right.text = ##f
                        \once \override TextSpanner.dash-fraction = 0.25
                        \once \override TextSpanner.dash-period = 1.5
                        g'8. \startTextSpan
                        f'8.
                        ef'4. \stopTextSpan ^ \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    120
                                }
                            }
                    }
                >>

        Defaults to false.

        Set to true, false or none.
        '''
        return self._start_with_parenthesized_tempo
