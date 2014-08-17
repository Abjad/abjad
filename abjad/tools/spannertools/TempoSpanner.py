# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import lilypondnametools
from abjad.tools import markuptools
from abjad.tools import schemetools
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

            >>> override(score).text_script.staff_padding = 1.25

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript #'staff-padding = #1.25
            } <<
                \new Staff {
                    \time 3/8
                    c'8. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
                        }
                    d'8.
                    e'4. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 90"
                        }
                    g'8. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 72"
                        }
                    f'8.
                    ef'4. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
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

            >>> override(score).text_script.staff_padding = 1.25
            >>> override(score).text_spanner.staff_padding = 2

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript #'staff-padding = #1.25
                \override TextSpanner #'staff-padding = #2
            } <<
                \new Staff {
                    \time 3/8
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                {
                                    \large
                                        \upright
                                            accel.
                                }
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
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
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 90"
                        }
                    g'8. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 72"
                        }
                    f'8.
                    ef'4. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
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

            >>> override(score).text_script.staff_padding = 1.25
            >>> override(score).text_spanner.staff_padding = 2

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript #'staff-padding = #1.25
                \override TextSpanner #'staff-padding = #2
            } <<
                \new Staff {
                    \time 3/8
                    c'8. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
                        }
                    d'8.
                    e'4. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 90"
                        }
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                {
                                    \large
                                        \upright
                                            rit.
                                }
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 72"
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
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
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

            >>> override(score).text_script.staff_padding = 1.25
            >>> override(score).text_spanner.staff_padding = 2

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript #'staff-padding = #1.25
                \override TextSpanner #'staff-padding = #2
            } <<
                \new Staff {
                    \time 3/8
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                {
                                    \large
                                        \upright
                                            accel.
                                }
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
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
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 90"
                        }
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                {
                                    \large
                                        \upright
                                            rit.
                                }
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 72"
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
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
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

            >>> override(score).text_script.staff_padding = 1.25
            >>> override(score).text_spanner.staff_padding = 2

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript #'staff-padding = #1.25
                \override TextSpanner #'staff-padding = #2
            } <<
                \new Staff {
                    \time 3/8
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                {
                                    \large
                                        \upright
                                            accel.
                                }
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
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 90"
                        }
                    g'8. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 72"
                        }
                    f'8.
                    ef'4. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
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

            >>> override(score).text_script.staff_padding = 1.25
            >>> override(score).text_spanner.staff_padding = 2

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript #'staff-padding = #1.25
                \override TextSpanner #'staff-padding = #2
            } <<
                \new Staff {
                    \time 3/8
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                {
                                    \large
                                        \upright
                                            rit.
                                }
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
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 90"
                        }
                    g'8. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 72"
                        }
                    f'8.
                    ef'4. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
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

            >>> attach(spannertools.TempoSpanner(), staff[:])

        ::

            >>> override(score).text_script.staff_padding = 1.25
            >>> override(score).text_spanner.staff_padding = 2

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript #'staff-padding = #1.25
                \override TextSpanner #'staff-padding = #2
            } <<
                \new Staff {
                    \time 3/8
                    c'8. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
                        }
                    d'8.
                    e'4. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 90"
                        }
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                {
                                    \large
                                        \upright
                                            accel.
                                }
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
                                        \smaller
                                            \general-align
                                                #Y
                                                #DOWN
                                                \note-by-number
                                                    #2
                                                    #0
                                                    #1
                                        \upright
                                            " = 90"
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
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 120"
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

            >>> attach(spannertools.TempoSpanner(), staff[:])

        ::

            >>> override(score).text_script.staff_padding = 1.25
            >>> override(score).text_spanner.staff_padding = 2

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript #'staff-padding = #1.25
                \override TextSpanner #'staff-padding = #2
            } <<
                \new Staff {
                    \time 3/8
                    c'8. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
                        }
                    d'8.
                    e'4. ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 90"
                        }
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                {
                                    \large
                                        \upright
                                            rit.
                                }
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
                                        \smaller
                                            \general-align
                                                #Y
                                                #DOWN
                                                \note-by-number
                                                    #2
                                                    #0
                                                    #1
                                        \upright
                                            " = 90"
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
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
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

            >>> override(score).text_script.staff_padding = 1.25
            >>> override(score).text_spanner.staff_padding = 2

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript #'staff-padding = #1.25
                \override TextSpanner #'staff-padding = #2
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
                                {
                                    \large
                                        \upright
                                            accel.
                                }
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
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
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 90"
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

            >>> override(score).text_script.staff_padding = 1.25
            >>> override(score).text_spanner.staff_padding = 2

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                \override TextScript #'staff-padding = #1.25
                \override TextSpanner #'staff-padding = #2
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
                                {
                                    \large
                                        \upright
                                            rit.
                                }
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 90"
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
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
                        }
                    c''4.
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )

    ### PRIVATE METHODS ###

    def _append_hspace(self, markup, hspace):
        commands = list(markup.contents)
        commands.append(markuptools.MarkupCommand('hspace', hspace))
        markup = markuptools.Markup(contents=commands)
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

    def _get_previous_annotations(self, leaf):
        index = self._index(leaf)
        for index in reversed(range(index)):
            previous_leaf = self[index]
            annotations = self._get_annotations(previous_leaf)
            if any(_ is not None for _ in annotations):
                return annotations
        return None, None, None

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
            markup = current_tempo._to_markup()
            markup = new(markup, direction=Up)
            string = format(markup, 'lilypond')
            lilypond_format_bundle.right.markup.append(string)
            return lilypond_format_bundle
        # use spanner if tempo trend starts now
        spanner_start = r'\startTextSpan'
        lilypond_format_bundle.right.spanner_starts.append(spanner_start)
        if current_tempo:
            self._start_tempo_trend_spanner_with_explicit_start(
                leaf,
                lilypond_format_bundle,
                current_tempo,
                current_tempo_trend,
                )
        else:
            self._start_tempo_trend_spanner_with_implicit_start(
                leaf,
                lilypond_format_bundle,
                current_tempo_trend,
                previous_tempo,
                )
        #
        markup = current_tempo_trend._to_markup()
        markup = self._parenthesize_markup(markup, padding=0.45)
        markup = self._append_hspace(markup, 0.75)
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
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)
        self._make_other_text_spanner_overrides(lilypond_format_bundle)
        return lilypond_format_bundle

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
        override_string = '\n'.join(override_._override_format_pieces)
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
        override_string = '\n'.join(override_._override_format_pieces)
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
        override_string = '\n'.join(override_._override_format_pieces)
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
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'left-broken',
                'padding',
                ),
            value=-2,
            )
        override_string = '\n'.join(override_._override_format_pieces)
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
        override_string = '\n'.join(override_._override_format_pieces)
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
        override_string = '\n'.join(override_._override_format_pieces)
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
        override_string = '\n'.join(override_._override_format_pieces)
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
        override_string = '\n'.join(override_._override_format_pieces)
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
        override_string = '\n'.join(override_._override_format_pieces)
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
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)

    def _parenthesize_markup(self, markup, padding=None):
        commands = []
        if 1 < len(markup.contents):
            command = markuptools.MarkupCommand('line', markup.contents)
        else:
            command = markup.contents[:1]
        command = markuptools.MarkupCommand('parenthesize', command)
        pair = schemetools.SchemePair('padding', padding)
        command = markuptools.MarkupCommand('override', pair, command)
        commands.append(command)
        markup = markuptools.Markup(contents=commands)
        return markup

    def _start_tempo_trend_spanner_with_explicit_start(
        self,
        leaf,
        lilypond_format_bundle,
        current_tempo,
        current_tempo_trend,
        ):
        #
        markup = current_tempo._to_markup()
        markup = self._append_hspace(markup, 1.25)
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
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)

    def _start_tempo_trend_spanner_with_implicit_start(
        self,
        leaf,
        lilypond_format_bundle,
        current_tempo_trend,
        previous_tempo,
        ):
        #
        if previous_tempo:
            markup = previous_tempo._to_markup()
            markup = self._parenthesize_markup(markup, padding=0.45)
            markup = self._append_hspace(markup, 0.75)
        else:
            markup = current_tempo_trend._to_markup()
            markup = self._append_hspace(markup, 0.75)
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
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)