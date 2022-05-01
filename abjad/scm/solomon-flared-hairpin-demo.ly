\version "2.19"
\include "solomon-flared-hairpin.ily"


\layout {
  ragged-right = ##t
  indent = 0
}

\markup "ordinary cresc"

{
  g1~\<
  %\break
  g4 ~ g4 ~ g8\f
}

\markup "ordinary Ferneyhough cresc"

{
  \override Hairpin.stencil = #flared-hairpin
  g1~\<
  %\break
  g4 ~ g4 ~ g8\f
}

\markup "ordinary niente cresc"

{
  \override Hairpin.circled-tip = ##t
  g1~\<
  %\break
  g4 ~ g4 ~ g8\f
}

{
  \override Hairpin.circled-tip = ##t
  r2 r4 r8 r16 g16~\<
  \break
  g4 ~ g4 ~ g8\sfz
}

\markup "Ferneyhough niente cresc"

{
  \override Hairpin.circled-tip = ##t
  \override Hairpin.stencil = #flared-hairpin
  r2 r4 r8 r16 g16~\<
  \break
  g4 ~ g4 ~ g8\f
}


\markup "Ferneyhough constante"

{
  %\override Hairpin.stencil = #normal-hairpin
  \override Hairpin.stencil = #constante-hairpin
  %\override Hairpin.stencil = #flared-hairpin
  %\override Hairpin.stencil = #bizarre-hairpin
  %\override Hairpin.circled-tip = ##t
  g1\p ~\<
  \break
  g1~
  %\break
  %\override DynamicText.extra-offset = #'(-1.5 . 0)
  g4 ~ g4 ~ g8\sfz
}

{
  %\override Hairpin.stencil = #normal-hairpin
  \override Hairpin.stencil = #constante-hairpin
  %\override Hairpin.stencil = #flared-hairpin
  %\override Hairpin.stencil = #bizarre-hairpin
  \override Hairpin.circled-tip = ##t
  g1~\<
  %\break
  g1~
  %\break
  %\override DynamicText.extra-offset = #'(-1.5 . 0)
  g4 ~ g4 ~ g8\sfz
}

\markup "ordinary decresc al niente"

{
  \override Hairpin.circled-tip = ##t
  g1~\f\>
  \break
  g4 ~ g4 ~ g8\!
}

\markup "Ferneyhough decresc al niente"
{
  \override Hairpin.stencil = #flared-hairpin
  \override Hairpin.circled-tip = ##t
  g1~\sfz\>
  \break
  g1~
  %\break
  g4 ~ g4 ~ g8\!
}


\markup "Your example"

{
  \override Hairpin.stencil = #flared-hairpin
  \override Hairpin #'circled-tip = ##t

  c'4 \< c'2 c'4 \!
  |
  \revert Hairpin.stencil
  c'4 \< c'2 c'4 \!
  |

}
