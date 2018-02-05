from .Spanner import Spanner


class MetronomeMarkSpanner(Spanner):
    r'''Metronome mark spanner.

    ..  container:: example

        With metronome marks only:

        >>> staff = abjad.Staff("c'8. d' e'4. g'8. f' ef'4.")
        >>> score = abjad.Score([staff])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
        >>> spanner = abjad.MetronomeMarkSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.override(staff).text_spanner.staff_padding = 3

        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[0])
        >>> mark = abjad.MetronomeMark((1, 4), 90)
        >>> spanner.attach(mark, spanner[2])
        >>> mark = abjad.MetronomeMark((1, 4), 72)
        >>> spanner.attach(mark, spanner[3])
        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[5])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    \time 3/8
                    c'8. \startTextSpan
                    d'8.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    e'4. \stopTextSpan \startTextSpan
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.right.text =
                    \markup {
                        \concat
                            {
                                \hspace
                                    #0.5
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
                                                60
                                            }
                                    }
                            }
                        }
                    \once \override TextSpanner.dash-period = 0
                    g'8. \stopTextSpan \startTextSpan
                    f'8.
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    ef'4. \stopTextSpan
                }
            >>

    ..  container:: example

        With an accelerando:

        >>> staff = abjad.Staff("c'8. d' e'4. g'8. f' ef'4.")
        >>> score = abjad.Score([staff])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
        >>> spanner = abjad.MetronomeMarkSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.override(staff).text_spanner.staff_padding = 3

        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[0])
        >>> accelerando = abjad.Accelerando()
        >>> spanner.attach(accelerando, spanner[0])
        >>> mark = abjad.MetronomeMark((1, 4), 90)
        >>> spanner.attach(mark, spanner[2])
        >>> mark = abjad.MetronomeMark((1, 4), 72)
        >>> spanner.attach(mark, spanner[3])
        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[5])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        accel.
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    \time 3/8
                    c'8. \startTextSpan
                    d'8.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    e'4. \stopTextSpan \startTextSpan
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.right.text =
                    \markup {
                        \concat
                            {
                                \hspace
                                    #0.5
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
                                                60
                                            }
                                    }
                            }
                        }
                    \once \override TextSpanner.dash-period = 0
                    g'8. \stopTextSpan \startTextSpan
                    f'8.
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    ef'4. \stopTextSpan
                }
            >>

    ..  container:: example

        With a ritardando:

        >>> staff = abjad.Staff("c'8. d' e'4. g'8. f' ef'4.")
        >>> score = abjad.Score([staff])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
        >>> spanner = abjad.MetronomeMarkSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.override(staff).text_spanner.staff_padding = 3

        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[0])
        >>> mark = abjad.MetronomeMark((1, 4), 90)
        >>> spanner.attach(mark, spanner[2])
        >>> mark = abjad.MetronomeMark((1, 4), 72)
        >>> spanner.attach(mark, spanner[3])
        >>> ritardando = abjad.Ritardando()
        >>> spanner.attach(ritardando, spanner[3])
        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[5])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    \time 3/8
                    c'8. \startTextSpan
                    d'8.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    e'4. \stopTextSpan \startTextSpan
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        rit.
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.right.text =
                    \markup {
                        \concat
                            {
                                \hspace
                                    #0.5
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
                                                60
                                            }
                                    }
                            }
                        }
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    g'8. \stopTextSpan \startTextSpan
                    f'8.
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    ef'4. \stopTextSpan
                }
            >>

    ..  container:: example

        With both an accelerando and a ritardando:

        >>> staff = abjad.Staff("c'8. d' e'4. g'8. f' ef'4.")
        >>> score = abjad.Score([staff])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
        >>> spanner = abjad.MetronomeMarkSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.override(staff).text_spanner.staff_padding = 3

        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[0])
        >>> mark = abjad.MetronomeMark((1, 4), 90)
        >>> spanner.attach(mark, spanner[2])
        >>> mark = abjad.MetronomeMark((1, 4), 72)
        >>> spanner.attach(mark, spanner[3])
        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[5])
        >>> accelerando = abjad.Accelerando()
        >>> spanner.attach(accelerando, spanner[0])
        >>> ritardando = abjad.Ritardando()
        >>> spanner.attach(ritardando, spanner[3])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        accel.
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    \time 3/8
                    c'8. \startTextSpan
                    d'8.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    e'4. \stopTextSpan \startTextSpan
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        rit.
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.right.text =
                    \markup {
                        \concat
                            {
                                \hspace
                                    #0.5
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
                                                60
                                            }
                                    }
                            }
                        }
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    g'8. \stopTextSpan \startTextSpan
                    f'8.
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    ef'4. \stopTextSpan
                }
            >>

    ..  container:: example

        Implicit start to (music-initial) accelerando:

        >>> staff = abjad.Staff("c'8. d' e'4. g'8. f' ef'4.")
        >>> score = abjad.Score([staff])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
        >>> spanner = abjad.MetronomeMarkSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.override(staff).text_spanner.staff_padding = 3

        >>> mark = abjad.MetronomeMark((1, 4), 90)
        >>> spanner.attach(mark, spanner[2])
        >>> mark = abjad.MetronomeMark((1, 4), 72)
        >>> spanner.attach(mark, spanner[3])
        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[5])
        >>> accelerando = abjad.Accelerando()
        >>> spanner.attach(accelerando, spanner[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        accel.
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \large
                            \upright
                                accel.
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    \time 3/8
                    c'8. \startTextSpan
                    d'8.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    e'4. \stopTextSpan \startTextSpan
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.right.text =
                    \markup {
                        \concat
                            {
                                \hspace
                                    #0.5
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
                                                60
                                            }
                                    }
                            }
                        }
                    \once \override TextSpanner.dash-period = 0
                    g'8. \stopTextSpan \startTextSpan
                    f'8.
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    ef'4. \stopTextSpan
                }
            >>

    ..  container:: example

        Implicit start to (music-initial) ritardando:

        >>> staff = abjad.Staff("c'8. d' e'4. g'8. f' ef'4.")
        >>> score = abjad.Score([staff])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
        >>> spanner = abjad.MetronomeMarkSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.override(staff).text_spanner.staff_padding = 3

        >>> mark = abjad.MetronomeMark((1, 4), 90)
        >>> spanner.attach(mark, spanner[2])
        >>> mark = abjad.MetronomeMark((1, 4), 72)
        >>> spanner.attach(mark, spanner[3])
        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[5])
        >>> ritardando = abjad.Ritardando()
        >>> spanner.attach(ritardando, spanner[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        rit.
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \large
                            \upright
                                rit.
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    \time 3/8
                    c'8. \startTextSpan
                    d'8.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    e'4. \stopTextSpan \startTextSpan
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.right.text =
                    \markup {
                        \concat
                            {
                                \hspace
                                    #0.5
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
                                                60
                                            }
                                    }
                            }
                        }
                    \once \override TextSpanner.dash-period = 0
                    g'8. \stopTextSpan \startTextSpan
                    f'8.
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    ef'4. \stopTextSpan
                }
            >>

    ..  container:: example

        Implicit start to (midmusic) accelerando:

        >>> staff = abjad.Staff("c'8. d' e'4. g'8. f' ef'4.")
        >>> score = abjad.Score([staff])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
        >>> spanner = abjad.MetronomeMarkSpanner(
        ...     parenthesize=True,
        ...     )
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.override(staff).text_spanner.staff_padding = 3

        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[0])
        >>> mark = abjad.MetronomeMark((1, 4), 90)
        >>> spanner.attach(mark, spanner[2])
        >>> mark = abjad.MetronomeMark((1, 4), 120)
        >>> spanner.attach(mark, spanner[5])
        >>> accelerando = abjad.Accelerando()
        >>> spanner.attach(accelerando, spanner[3])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    \time 3/8
                    c'8. \startTextSpan
                    d'8.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    e'4. \stopTextSpan \startTextSpan
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        accel.
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.right.text =
                    \markup {
                        \concat
                            {
                                \hspace
                                    #0.5
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
                                                120
                                            }
                                    }
                            }
                        }
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    g'8. \stopTextSpan \startTextSpan
                    f'8.
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    ef'4. \stopTextSpan
                }
            >>

    ..  container:: example

        Implicit start to (midmusic) ritardando:

        >>> staff = abjad.Staff("c'8. d' e'4. g'8. f' ef'4.")
        >>> score = abjad.Score([staff])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
        >>> spanner = abjad.MetronomeMarkSpanner(
        ...     parenthesize=True,
        ...     )
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.override(staff).text_spanner.staff_padding = 3

        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[0])
        >>> mark = abjad.MetronomeMark((1, 4), 90)
        >>> spanner.attach(mark, spanner[2])
        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[5])
        >>> ritardando = abjad.Ritardando()
        >>> spanner.attach(ritardando, spanner[3])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    \time 3/8
                    c'8. \startTextSpan
                    d'8.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    e'4. \stopTextSpan \startTextSpan
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        rit.
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.right.text =
                    \markup {
                        \concat
                            {
                                \hspace
                                    #0.5
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
                                                60
                                            }
                                    }
                            }
                        }
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    g'8. \stopTextSpan \startTextSpan
                    f'8.
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    ef'4. \stopTextSpan
                }
            >>

    ..  container:: example

        With an accelerando over a line break:

        >>> staff = abjad.Staff("c'4. d' e' f' g' a' b' c''")
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
        >>> spanner = abjad.MetronomeMarkSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> score = abjad.Score([staff])
        >>> command = abjad.LilyPondLiteral(r'\break', 'after')
        >>> abjad.attach(command, staff[3])
        >>> abjad.override(staff).text_spanner.staff_padding = 3

        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[2])
        >>> mark = abjad.MetronomeMark((1, 4), 90)
        >>> spanner.attach(mark, spanner[6])
        >>> accelerando = abjad.Accelerando()
        >>> spanner.attach(accelerando, spanner[2])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    \time 3/8
                    c'4. \startTextSpan
                    d'4.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        accel.
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    e'4. \stopTextSpan \startTextSpan
                    f'4.
                    \break
                    g'4.
                    a'4.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    b'4. \stopTextSpan \startTextSpan
                    c''4. \stopTextSpan
                }
            >>

    ..  container:: example

        With a ritardando over a line break:

        >>> staff = abjad.Staff("c'4. d' e' f' g' a' b' c''")
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
        >>> spanner = abjad.MetronomeMarkSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> score = abjad.Score([staff])
        >>> command = abjad.LilyPondLiteral(r'\break', 'after')
        >>> abjad.attach(command, staff[3])
        >>> abjad.override(staff).text_spanner.staff_padding = 3

        >>> mark = abjad.MetronomeMark((1, 4), 90)
        >>> spanner.attach(mark, spanner[2])
        >>> mark = abjad.MetronomeMark((1, 4), 60)
        >>> spanner.attach(mark, spanner[6])
        >>> ritardando = abjad.Ritardando()
        >>> spanner.attach(ritardando, spanner[2])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    \time 3/8
                    c'4. \startTextSpan
                    d'4.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        rit.
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    e'4. \stopTextSpan \startTextSpan
                    f'4.
                    \break
                    g'4.
                    a'4.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    b'4. \stopTextSpan \startTextSpan
                    c''4. \stopTextSpan
                }
            >>

    ..  container:: example

        With a metric modulation:

        >>> staff = abjad.Staff("c'8. d'8. e'4. g'8. f'8. ef'4.")
        >>> score = abjad.Score([staff])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
        >>> spanner = abjad.MetronomeMarkSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.override(staff).text_spanner.staff_padding = 3

        >>> mark = abjad.MetronomeMark((3, 4), 90)
        >>> spanner.attach(mark, spanner[0])
        >>> mark = abjad.MetronomeMark((3, 4), 60)
        >>> spanner.attach(mark, spanner[3])
        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note('c4.'),
        ...     right_rhythm=abjad.Note('c4'),
        ...     )
        >>> spanner.attach(metric_modulation, spanner[3])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    \time 3/8
                    c'8. \startTextSpan
                    d'8.
                    e'4.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                                                        \new Score
                                                        \with
                                                        {
                                                            \override SpacingSpanner.spacing-increment = #0.5
                                                            proportionalNotationDuration = ##f
                                                        }
                                                        <<
                                                            \new RhythmicStaff
                                                            \with
                                                            {
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
                                                            }
                                                            {
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
                                                        \new Score
                                                        \with
                                                        {
                                                            \override SpacingSpanner.spacing-increment = #0.5
                                                            proportionalNotationDuration = ##f
                                                        }
                                                        <<
                                                            \new RhythmicStaff
                                                            \with
                                                            {
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
                                                            }
                                                            {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    g'8. \stopTextSpan \startTextSpan
                    f'8.
                    ef'4. \stopTextSpan
                }
            >>

    ..  container:: example

        With a metric modulation and an accelerando:

        >>> staff = abjad.Staff("c'8. d'8. e'4. g'8. f'8. ef'4.")
        >>> score = abjad.Score([staff])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
        >>> spanner = abjad.MetronomeMarkSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.override(staff).text_spanner.staff_padding = 3

        >>> mark = abjad.MetronomeMark((3, 4), 90)
        >>> spanner.attach(mark, spanner[0])
        >>> mark = abjad.MetronomeMark((3, 4), 60)
        >>> spanner.attach(mark, spanner[3])
        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note('c4.'),
        ...     right_rhythm=abjad.Note('c4'),
        ...     )
        >>> spanner.attach(metric_modulation, spanner[3])
        >>> spanner.attach(abjad.Accelerando(), spanner[3])
        >>> mark = abjad.MetronomeMark((3, 4), 90)
        >>> spanner.attach(mark, spanner[-1])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    \time 3/8
                    c'8. \startTextSpan
                    d'8.
                    e'4.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \override
                            #'(padding . 0.45)
                            \parenthesize
                                \large
                                    \upright
                                        accel.
                        \hspace
                            #1
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                                                        \new Score
                                                        \with
                                                        {
                                                            \override SpacingSpanner.spacing-increment = #0.5
                                                            proportionalNotationDuration = ##f
                                                        }
                                                        <<
                                                            \new RhythmicStaff
                                                            \with
                                                            {
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
                                                            }
                                                            {
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
                                                        \new Score
                                                        \with
                                                        {
                                                            \override SpacingSpanner.spacing-increment = #0.5
                                                            proportionalNotationDuration = ##f
                                                        }
                                                        <<
                                                            \new RhythmicStaff
                                                            \with
                                                            {
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
                                                            }
                                                            {
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
                            #1
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.right.text =
                    \markup {
                        \concat
                            {
                                \hspace
                                    #0.5
                                \line
                                    {
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
                        }
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    g'8. \stopTextSpan \startTextSpan
                    f'8.
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    ef'4. \stopTextSpan
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_left_broken_padding',
        '_left_broken_text',
        '_left_hspace',
        '_parenthesize',
        '_right_padding',
        '_stem_height',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        left_broken_padding=None,
        left_broken_text=None,
        left_hspace=1,
        parenthesize=False,
        right_padding=1,
        stem_height=1,
        overrides=None,
        ):
        import abjad
        Spanner.__init__(self, overrides=overrides)
        assert isinstance(left_broken_padding, (int, float, type(None)))
        self._left_broken_padding = left_broken_padding
        prototype = (abjad.Markup, type(None))
        assert isinstance(left_broken_text, prototype)
        self._left_broken_text = left_broken_text
        self._left_hspace = left_hspace
        if parenthesize is not None:
            parenthesize = bool(parenthesize)
        self._parenthesize = parenthesize
        self._right_padding = right_padding
        self._stem_height = stem_height

    ### PRIVATE METHODS ###

    def _combine_metronome_mark_and_metric_modulation(
        self,
        metronome_mark,
        metric_modulation,
        ):
        import abjad
        assert metronome_mark is not None or metric_modulation is not None
        if metronome_mark is None:
            return metric_modulation._get_markup(
                music_scale_pair=(0.5, 0.5),
                )
        if metric_modulation is None:
            return metronome_mark._get_markup(
                stem_height=self.stem_height,
                )
        # HERE
        metronome_mark_markup = metronome_mark._get_markup(
            stem_height=self.stem_height,
            )
        metronome_mark_markup = \
            metronome_mark_markup + metronome_mark_markup.hspace(0.5)
        modulation_markup = metric_modulation._get_markup(
            music_scale_pair=(0.5, 0.5),
            )
        modulation_markup = modulation_markup.line([modulation_markup])
        modulation_markup = modulation_markup.parenthesize()
        modulation_markup = modulation_markup.override(('padding', 0.5))
        modulation_markup = modulation_markup.general_align('Y', abjad.Down)
        markup = metronome_mark_markup + modulation_markup
        return markup

    def _get_lilypond_format_bundle(self, leaf):
        import abjad
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if not 1 < len(self):
            return bundle
        if not self._wrappers:
            return bundle
        current_wrappers = self._get_piecewise_wrappers(leaf)
        #
        current_metronome_mark_wrapper = current_wrappers[0]
        if current_metronome_mark_wrapper is not None:
            current_metronome_mark = current_metronome_mark_wrapper.indicator
        else:
            current_metronome_mark = None
        #
        current_tempo_trend_wrapper = current_wrappers[1]
        if current_tempo_trend_wrapper is not None:
            current_tempo_trend = current_tempo_trend_wrapper.indicator
        else:
            current_tempo_trend = None
        #
        current_metric_modulation_wrapper = current_wrappers[2]
        if current_metric_modulation_wrapper is not None:
            current_metric_modulation = \
                current_metric_modulation_wrapper.indicator
        else:
            current_metric_modulation = None
        #
        if self._should_format_last_leaf_markup(leaf):
            last_leaf_metronome_mark = abjad.inspect(self[-1]).get_piecewise(
                abjad.MetronomeMark,
                )
        else:
            last_leaf_metronome_mark = None
        indicators = (
            current_metronome_mark,
            current_metric_modulation,
            current_tempo_trend,
            last_leaf_metronome_mark,
            )
        has_indicators = any(_ is not None for _ in indicators)
        #
        if not has_indicators:
            if leaf is self[0]:
                bundle.right.spanner_starts.append(r'\startTextSpan')
                string = r'\once \override TextSpanner.Y-extent = ##f'
                bundle.grob_overrides.append(string)
                line_segment = self._make_invisible_line_segment()
                line_segment = abjad.new(
                    line_segment,
                    right_padding=self.right_padding,
                    )
                overrides = line_segment._get_lilypond_grob_overrides()
                for override in overrides:
                    override_string = override.override_string
                    bundle.grob_overrides.append(override_string)
            if leaf is self[-1]:
                bundle.right.spanner_stops.append(r'\stopTextSpan')
            return bundle
        #
        previous_wrappers = self._get_previous_piecewise_wrappers(leaf)
        previous_metronome_mark_wrapper = previous_wrappers[0]
        if previous_metronome_mark_wrapper is not None:
            previous_metronome_mark = previous_metronome_mark_wrapper.indicator
        else:
            previous_metronome_mark = None
        previous_tempo_trend_wrapper = previous_wrappers[1]
        if previous_tempo_trend_wrapper is not None:
            previous_tempo_trend = previous_tempo_trend_wrapper.indicator
        else:
            previous_tempo_trend = None
        #
        if has_indicators and not leaf is self[0]:
            bundle.right.spanner_stops.append(r'\stopTextSpan')
        #
        if not leaf is self[-1]:
            bundle.right.spanner_starts.append(r'\startTextSpan')
            string = r'\once \override TextSpanner.Y-extent = ##f'
            bundle.grob_overrides.append(string)
            if current_metronome_mark or current_metric_modulation:
                self._start_tempo_trend_spanner_with_explicit_start(
                    leaf,
                    bundle,
                    current_metronome_mark_wrapper,
                    current_metric_modulation_wrapper,
                    )
            else:
                self._start_tempo_trend_spanner_with_implicit_start(
                    leaf,
                    bundle,
                    current_tempo_trend,
                    previous_metronome_mark,
                    )
            if current_tempo_trend is None:
                line_segment = self._make_invisible_line_segment()
            else:
                line_segment = self._make_dashed_arrow()
            line_segment = abjad.new(
                line_segment,
                right_padding=self.right_padding,
                )
            overrides = line_segment._get_lilypond_grob_overrides()
            for override in overrides:
                override_string = override.override_string
                bundle.grob_overrides.append(override_string)
        #
        if last_leaf_metronome_mark is not None:
            last_leaf_wrapper = abjad.inspect(self[-1]).wrapper(
                abjad.MetronomeMark
                )
            assert last_leaf_wrapper.indicator is last_leaf_metronome_mark
            last_leaf_markup = last_leaf_metronome_mark._get_markup(
                stem_height=self.stem_height,
                )
            right_hspace = line_segment.right_padding or 0
            # optical correction to draw last markup left:
            right_hspace -= 0.5
            right_hspace = abjad.Markup.hspace(right_hspace)
            last_leaf_markup = abjad.Markup.line([last_leaf_markup])
            last_leaf_markup = abjad.Markup.concat(
                [right_hspace, last_leaf_markup],
                )
            last_leaf_markup = abjad.new(last_leaf_markup, direction=None)
            pieces = last_leaf_markup._get_format_pieces()
            piece = r'\once \override TextSpanner.bound-details.right.text ='
            pieces.insert(0, piece)
            pieces = abjad.LilyPondFormatManager.tag(
                pieces,
                last_leaf_wrapper.tag,
                deactivate=last_leaf_wrapper.deactivate,
                site=last_leaf_wrapper.site,
                )
            string = '\n'.join(pieces)
            bundle.grob_overrides.append(string)
            alternate = last_leaf_wrapper.alternate
            if alternate is not None:
                deactivate = not last_leaf_wrapper.deactivate
                color, site, tag = alternate
                color = abjad.SchemeColor(color)
                last_leaf_markup = last_leaf_markup.with_color(color)
                pieces = last_leaf_markup._get_format_pieces()
                piece = r'\once \override'
                piece += ' TextSpanner.bound-details.right.text ='
                pieces.insert(0, piece)
                pieces = abjad.LilyPondFormatManager.tag(
                    pieces,
                    tag,
                    deactivate=deactivate,
                    site=site,
                    )
                string = '\n'.join(pieces)
                bundle.grob_overrides.append(string)
        #
        if self.left_broken_text is not None:
            markup = self.left_broken_text
        elif current_tempo_trend is not None:
            markup = current_tempo_trend._get_markup()
            markup = markup.parenthesize()
            markup = markup.override(('padding', 0.45))
            markup = markup + markup.hspace(self.left_hspace)
        else:
            markup = False
        override = abjad.LilyPondGrobOverride(
            grob_name='TextSpanner',
            once=True,
            property_path=(
                'bound-details',
                'left-broken',
                'text',
                ),
            value=markup,
            )
        override_string = override.override_string
        bundle.grob_overrides.append(override_string)
        return bundle

    def _get_piecewise_wrappers(self, leaf):
        import abjad
        metronome_mark = abjad.inspect(leaf).get_piecewise(
            abjad.MetronomeMark,
            default=None,
            unwrap=False,
            )
        tempo_trend = abjad.inspect(leaf).get_piecewise(
            (abjad.Accelerando, abjad.Ritardando),
            default=None,
            unwrap=False,
            )
        metric_modulation = abjad.inspect(leaf).get_piecewise(
            abjad.MetricModulation,
            default=None,
            unwrap=False,
            )
        return (
            metronome_mark,
            tempo_trend,
            metric_modulation,
            )

    def _get_previous_piecewise_wrappers(self, leaf):
        index = self._index(leaf)
        for index in reversed(range(index)):
            previous_leaf = self[index]
            wrappers = self._get_piecewise_wrappers(previous_leaf)
            indicators = [getattr(_, 'indicator', None) for _ in wrappers]
            if any(_ is not None for _ in indicators):
                return wrappers
        return None, None, None

    @staticmethod
    def _make_dashed_arrow():
        import abjad
        return abjad.ArrowLineSegment(
            dash_fraction=0.25,
            dash_period=1.5,
            left_broken_text=False,
            left_hspace=0.5,
            right_broken_arrow=False,
            right_broken_padding=0,
            right_broken_text=False,
            right_padding=0.5,
            )

    @staticmethod
    def _make_invisible_line_segment():
        import abjad
        return abjad.LineSegment(
            dash_period=0,
            left_broken_text=False,
            left_hspace=0.25,
            left_stencil_align_direction_y=abjad.Center,
            right_broken_padding=0,
            right_broken_text=False,
            right_padding=1.5,
            right_stencil_align_direction_y=abjad.Center,
            )

    def _should_format_last_leaf_markup(self, leaf):
        import abjad
        prototype = abjad.MetronomeMark
        if abjad.inspect(self[-1]).get_piecewise(prototype, None) is None:
            return False
        prototype = (
            abjad.Accelerando,
            abjad.MetricModulation,
            abjad.MetronomeMark,
            abjad.Ritardando,
            )
        leaf_ = None
        for leaf_ in reversed(self[:-1]):
            has_indicator = False
            for class_ in prototype:
                indicator = abjad.inspect(leaf_).get_piecewise(class_, None)
                if indicator is not None:
                    has_indicator = True
                    break
            if has_indicator:
                break
        return leaf_ is leaf

    def _start_tempo_trend_spanner_with_explicit_start(
        self,
        leaf,
        bundle,
        current_metronome_mark_wrapper,
        current_metric_modulation_wrapper,
        ):
        import abjad
        #
        markup = self._combine_metronome_mark_and_metric_modulation(
            getattr(current_metronome_mark_wrapper, 'indicator', None),
            getattr(current_metric_modulation_wrapper, 'indicator', None),
            )
        markup = markup + markup.hspace(self.left_hspace)
        #
        pieces = markup._get_format_pieces()
        piece = r'\once \override TextSpanner.bound-details.left.text ='
        pieces.insert(0, piece)
        pieces = abjad.LilyPondFormatManager.tag(
            pieces,
            current_metronome_mark_wrapper.tag,
            deactivate=current_metronome_mark_wrapper.deactivate,
            site=current_metronome_mark_wrapper.site,
            )
        string = '\n'.join(pieces)
        bundle.grob_overrides.append(string)
        alternate = current_metronome_mark_wrapper.alternate
        if alternate is not None:
            deactivate = not current_metronome_mark_wrapper.deactivate
            color, site, tag = alternate
            color = abjad.SchemeColor(color)
            markup = markup.with_color(color)
            pieces = markup._get_format_pieces()
            piece = r'\once \override TextSpanner.bound-details.left.text ='
            pieces.insert(0, piece)
            pieces = abjad.LilyPondFormatManager.tag(
                pieces,
                tag,
                deactivate=deactivate,
                site=site,
                )
            string = '\n'.join(pieces)
            bundle.grob_overrides.append(string)

    def _start_tempo_trend_spanner_with_implicit_start(
        self,
        leaf,
        bundle,
        current_tempo_trend,
        previous_metronome_mark,
        ):
        import abjad
        if (self.parenthesize and
            previous_metronome_mark):
            markup = previous_metronome_mark._get_markup(
                stem_height=self.stem_height,
                )
            markup = markup.line([markup])
            markup = markup.parenthesize()
            markup = markup.override(('padding', 0.45))
            markup = markup + markup.hspace(self.left_hspace)
        else:
            markup = current_tempo_trend._get_markup()
            markup = markup + markup.hspace(self.left_hspace)
        override = abjad.LilyPondGrobOverride(
            grob_name='TextSpanner',
            once=True,
            property_path=(
                'bound-details',
                'left',
                'text',
                ),
            value=markup,
            )
        override_string = override.override_string
        bundle.grob_overrides.append(override_string)

    ### PUBLIC PROPERTIES ###

    @property
    def left_broken_padding(self):
        r'''Gets left broken padding of metronome mark spanner.

        ..  container:: example

            With left broken padding set to none:

            >>> staff = abjad.Staff("c'4. d' e' f' g' a' b' c''")
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
            >>> score = abjad.Score([staff])
            >>> command = abjad.LilyPondLiteral(r'\break', 'after')
            >>> abjad.attach(command, staff[3])
            >>> spanner = abjad.MetronomeMarkSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.override(staff).text_spanner.staff_padding = 3

            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> spanner.attach(mark, spanner[2])
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> spanner.attach(mark, spanner[6])
            >>> ritardando = abjad.Ritardando()
            >>> spanner.attach(ritardando, spanner[2])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    \with
                    {
                        \override TextSpanner.staff-padding = #3
                    }
                    {
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-period = 0
                        \time 3/8
                        c'4. \startTextSpan
                        d'4.
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.arrow-width = 0.25
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \override
                                #'(padding . 0.45)
                                \parenthesize
                                    \large
                                        \upright
                                            rit.
                            \hspace
                                #1
                            }
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-fraction = 0.25
                        \once \override TextSpanner.dash-period = 1.5
                        e'4. \stopTextSpan \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-period = 0
                        b'4. \stopTextSpan \startTextSpan
                        c''4. \stopTextSpan
                    }
                >>

            Results in padding of ``-2``. (This is default behavior.)

        ..  container:: example

            With left broken padding set explicitly:

            >>> staff = abjad.Staff("c'4. d' e' f' g' a' b' c''")
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
            >>> score = abjad.Score([staff])
            >>> command = abjad.LilyPondLiteral(r'\break', 'after')
            >>> abjad.attach(command, staff[3])
            >>> spanner = abjad.MetronomeMarkSpanner(
            ...     left_broken_padding=4,
            ...     )
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.override(staff).text_spanner.staff_padding = 3

            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> spanner.attach(mark, spanner[2])
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> spanner.attach(mark, spanner[6])
            >>> ritardando = abjad.Ritardando()
            >>> spanner.attach(ritardando, spanner[2])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    \with
                    {
                        \override TextSpanner.staff-padding = #3
                    }
                    {
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-period = 0
                        \time 3/8
                        c'4. \startTextSpan
                        d'4.
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.arrow-width = 0.25
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \override
                                #'(padding . 0.45)
                                \parenthesize
                                    \large
                                        \upright
                                            rit.
                            \hspace
                                #1
                            }
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-fraction = 0.25
                        \once \override TextSpanner.dash-period = 1.5
                        e'4. \stopTextSpan \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-period = 0
                        b'4. \stopTextSpan \startTextSpan
                        c''4. \stopTextSpan
                    }
                >>

        Returns number or none.
        '''
        return self._left_broken_padding

    @property
    def left_broken_text(self):
        r'''Gets left broken text of metronome mark spanner.

        ..  container:: example

            With left broken text set to none:

            >>> staff = abjad.Staff("c'4. d' e' f' g' a' b' c''")
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
            >>> score = abjad.Score([staff])
            >>> command = abjad.LilyPondLiteral(r'\break', 'after')
            >>> abjad.attach(command, staff[3])
            >>> spanner = abjad.MetronomeMarkSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.override(staff).text_spanner.staff_padding = 3

            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> spanner.attach(mark, spanner[2])
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> spanner.attach(mark, spanner[6])
            >>> ritardando = abjad.Ritardando()
            >>> spanner.attach(ritardando, spanner[2])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    \with
                    {
                        \override TextSpanner.staff-padding = #3
                    }
                    {
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-period = 0
                        \time 3/8
                        c'4. \startTextSpan
                        d'4.
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.arrow-width = 0.25
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \override
                                #'(padding . 0.45)
                                \parenthesize
                                    \large
                                        \upright
                                            rit.
                            \hspace
                                #1
                            }
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-fraction = 0.25
                        \once \override TextSpanner.dash-period = 1.5
                        e'4. \stopTextSpan \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-period = 0
                        b'4. \stopTextSpan \startTextSpan
                        c''4. \stopTextSpan
                    }
                >>

            Results in parenthesized abbreviation after line break.
            (This is default behavior.)

        ..  container:: example

            With left broken text set explicitly:

            >>> staff = abjad.Staff("c'4. d' e' f' g' a' b' c''")
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
            >>> score = abjad.Score([staff])
            >>> command = abjad.LilyPondLiteral(r'\break', 'after')
            >>> abjad.attach(command, staff[3])
            >>> null_markup = abjad.Markup.null(direction=None)
            >>> spanner = abjad.MetronomeMarkSpanner(
            ...     left_broken_text=null_markup,
            ...     )
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.override(staff).text_spanner.staff_padding = 3

            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> spanner.attach(mark, spanner[2])
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> spanner.attach(mark, spanner[6])
            >>> ritardando = abjad.Ritardando()
            >>> spanner.attach(ritardando, spanner[2])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    \with
                    {
                        \override TextSpanner.staff-padding = #3
                    }
                    {
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-period = 0
                        \time 3/8
                        c'4. \startTextSpan
                        d'4.
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.arrow-width = 0.25
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \null
                            }
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-fraction = 0.25
                        \once \override TextSpanner.dash-period = 1.5
                        e'4. \stopTextSpan \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \null
                            }
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-period = 0
                        b'4. \stopTextSpan \startTextSpan
                        c''4. \stopTextSpan
                    }
                >>

            Results in null left broken text.

        Returns markup or none.
        '''
        return self._left_broken_text

    @property
    def left_hspace(self):
        r'''Gets left hspace.

        Set to a number or none.
        '''
        return self._left_hspace

    @property
    def parenthesize(self):
        r'''Is true when spanner should start with parenthesized metronome
        mark.

        ..  container:: example

            Does not start with parenthesized metronome mark:

            >>> staff = abjad.Staff("c'8. d' e'4. g'8. f' ef'4.")
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
            >>> score = abjad.Score([staff])
            >>> spanner = abjad.MetronomeMarkSpanner(
            ...     parenthesize=False,
            ...     )
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.override(staff).text_spanner.staff_padding = 3

            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> spanner.attach(mark, spanner[0])
            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> spanner.attach(mark, spanner[2])
            >>> mark = abjad.MetronomeMark((1, 4), 120)
            >>> spanner.attach(mark, spanner[5])
            >>> accelerando = abjad.Accelerando()
            >>> spanner.attach(accelerando, spanner[3])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    \with
                    {
                        \override TextSpanner.staff-padding = #3
                    }
                    {
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-period = 0
                        \time 3/8
                        c'8. \startTextSpan
                        d'8.
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-period = 0
                        e'4. \stopTextSpan \startTextSpan
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.arrow-width = 0.25
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \override
                                #'(padding . 0.45)
                                \parenthesize
                                    \large
                                        \upright
                                            accel.
                            \hspace
                                #1
                            }
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text = \markup {
                            \large
                                \upright
                                    accel.
                            \hspace
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.right.text =
                        \markup {
                            \concat
                                {
                                    \hspace
                                        #0.5
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
                                                    120
                                                }
                                        }
                                }
                            }
                        \once \override TextSpanner.dash-fraction = 0.25
                        \once \override TextSpanner.dash-period = 1.5
                        g'8. \stopTextSpan \startTextSpan
                        f'8.
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        ef'4. \stopTextSpan
                    }
                >>

        ..  container:: example

            Starts with parenthesized metronome mark:

            >>> staff = abjad.Staff("c'8. d' e'4. g'8. f' ef'4.")
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
            >>> score = abjad.Score([staff])
            >>> spanner = abjad.MetronomeMarkSpanner(
            ...     parenthesize=True,
            ...     )
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.override(staff).text_spanner.staff_padding = 3

            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> spanner.attach(mark, spanner[0])
            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> spanner.attach(mark, spanner[2])
            >>> mark = abjad.MetronomeMark((1, 4), 120)
            >>> spanner.attach(mark, spanner[5])
            >>> accelerando = abjad.Accelerando()
            >>> spanner.attach(accelerando, spanner[3])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    \with
                    {
                        \override TextSpanner.staff-padding = #3
                    }
                    {
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-period = 0
                        \time 3/8
                        c'8. \startTextSpan
                        d'8.
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-period = 0
                        e'4. \stopTextSpan \startTextSpan
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.arrow-width = 0.25
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \override
                                #'(padding . 0.45)
                                \parenthesize
                                    \large
                                        \upright
                                            accel.
                            \hspace
                                #1
                            }
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.right.text =
                        \markup {
                            \concat
                                {
                                    \hspace
                                        #0.5
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
                                                    120
                                                }
                                        }
                                }
                            }
                        \once \override TextSpanner.dash-fraction = 0.25
                        \once \override TextSpanner.dash-period = 1.5
                        g'8. \stopTextSpan \startTextSpan
                        f'8.
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        ef'4. \stopTextSpan
                    }
                >>

        Defaults to false.

        Set to true, false or none.
        '''
        return self._parenthesize

    @property
    def right_padding(self):
        r'''Gets right padding.

        Set to a number or none.
        '''
        return self._right_padding

    @property
    def stem_height(self):
        r'''Gets stem height.

        Set to a number.
        '''
        return self._stem_height

    ### PUBLIC METHODS ###

    def attach(
        self,
        indicator,
        leaf,
        alternate=None,
        deactivate=None,
        site=None,
        tag=None,
        ):
        r'''Attaches `indicator` to `leaf` in spanner.

        ..  container:: example

            REGRESSION. Inspection detects effective piecewise metronome marks
            correctly:

            >>> staff = abjad.Staff("c'8. d' e'4. g'8. f' ef'4.")
            >>> score = abjad.Score([staff])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
            >>> spanner = abjad.MetronomeMarkSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.override(staff).text_spanner.staff_padding = 3

            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> spanner.attach(mark, spanner[0])
            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> spanner.attach(mark, spanner[2])
            >>> mark = abjad.MetronomeMark((1, 4), 72)
            >>> spanner.attach(mark, spanner[3])
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> spanner.attach(mark, spanner[5])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    \with
                    {
                        \override TextSpanner.staff-padding = #3
                    }
                    {
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-period = 0
                        \time 3/8
                        c'8. \startTextSpan
                        d'8.
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-period = 0
                        e'4. \stopTextSpan \startTextSpan
                        \once \override TextSpanner.Y-extent = ##f
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.left.text =
                        \markup {
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
                                #1
                            }
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right-broken.text = ##f
                        \once \override TextSpanner.bound-details.right.padding = 1
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.bound-details.right.text =
                        \markup {
                            \concat
                                {
                                    \hspace
                                        #0.5
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
                                                    60
                                                }
                                        }
                                }
                            }
                        \once \override TextSpanner.dash-period = 0
                        g'8. \stopTextSpan \startTextSpan
                        f'8.
                        \once \override TextSpanner.bound-details.left-broken.text = ##f
                        ef'4. \stopTextSpan
                    }
                >>

            >>> prototype = abjad.MetronomeMark
            >>> abjad.inspect(staff[-1]).get_effective(prototype)
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=60)

        ..  container:: example

            Metronome marks can be tagged:

            >>> staff = abjad.Staff("c'8. d' e'4. g'8. f' ef'4.")
            >>> score = abjad.Score([staff])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
            >>> spanner = abjad.MetronomeMarkSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.override(staff).text_spanner.staff_padding = 3

            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> spanner.attach(mark, spanner[0], site='M1', tag='RED')
            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> spanner.attach(mark, spanner[2], tag='BLUE')
            >>> mark = abjad.MetronomeMark((1, 4), 72)
            >>> spanner.attach(mark, spanner[3], deactivate=True, tag='YELLOW')
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> spanner.attach(mark, spanner[5])
            >>> abjad.show(score) # doctest: +SKIP

            >>> abjad.f(score, strict=True)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text = %! RED:M1
                    \markup { %! RED:M1
                        \fontsize %! RED:M1
                            #-6 %! RED:M1
                            \general-align %! RED:M1
                                #Y %! RED:M1
                                #DOWN %! RED:M1
                                \note-by-number %! RED:M1
                                    #2 %! RED:M1
                                    #0 %! RED:M1
                                    #1 %! RED:M1
                        \upright %! RED:M1
                            { %! RED:M1
                                = %! RED:M1
                                60 %! RED:M1
                            } %! RED:M1
                        \hspace %! RED:M1
                            #1 %! RED:M1
                        } %! RED:M1
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    \time 3/8
                    c'8.
                    \startTextSpan
                    d'8.
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text = %! BLUE
                    \markup { %! BLUE
                        \fontsize %! BLUE
                            #-6 %! BLUE
                            \general-align %! BLUE
                                #Y %! BLUE
                                #DOWN %! BLUE
                                \note-by-number %! BLUE
                                    #2 %! BLUE
                                    #0 %! BLUE
                                    #1 %! BLUE
                        \upright %! BLUE
                            { %! BLUE
                                = %! BLUE
                                90 %! BLUE
                            } %! BLUE
                        \hspace %! BLUE
                            #1 %! BLUE
                        } %! BLUE
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    e'4.
                    \stopTextSpan
                    \startTextSpan
                %@% \once \override TextSpanner.bound-details.left.text = %! YELLOW
                %@% \markup { %! YELLOW
                %@%     \fontsize %! YELLOW
                %@%         #-6 %! YELLOW
                %@%         \general-align %! YELLOW
                %@%             #Y %! YELLOW
                %@%             #DOWN %! YELLOW
                %@%             \note-by-number %! YELLOW
                %@%                 #2 %! YELLOW
                %@%                 #0 %! YELLOW
                %@%                 #1 %! YELLOW
                %@%     \upright %! YELLOW
                %@%         { %! YELLOW
                %@%             = %! YELLOW
                %@%             72 %! YELLOW
                %@%         } %! YELLOW
                %@%     \hspace %! YELLOW
                %@%         #1 %! YELLOW
                %@%     } %! YELLOW
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.right.text =
                    \markup {
                        \concat
                            {
                                \hspace
                                    #0.5
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
                                                60
                                            }
                                    }
                            }
                        }
                    \once \override TextSpanner.dash-period = 0
                    g'8.
                    \stopTextSpan
                    \startTextSpan
                    f'8.
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    ef'4.
                    \stopTextSpan
                }
            >>

        >>> wrapper = abjad.inspect(staff[3]).wrapper(abjad.MetronomeMark)
        >>> abjad.f(wrapper)
        abjad.Wrapper(
            context='Score',
            deactivate=True,
            indicator=abjad.MetronomeMark(
                reference_duration=abjad.Duration(1, 4),
                units_per_minute=72,
                ),
            spanner=abjad.MetronomeMarkSpanner(
                left_hspace=1,
                parenthesize=False,
                right_padding=1,
                stem_height=1,
                ),
            tag='YELLOW',
            )

        Returns none.
        '''
        superclass = super(MetronomeMarkSpanner, self)
        superclass._attach_piecewise(
            indicator,
            leaf,
            alternate=alternate,
            deactivate=deactivate,
            site=site,
            tag=tag,
            )
