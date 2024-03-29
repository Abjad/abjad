:orphan:

LilyPond wellformedness
=======================

Recall that when typing LilyPond ``.ly`` files by hand, it is possible to enter input
that LilyPond considers not wellformed: starting a slur in one voice and trying to end it
in another voice, for example. The same situation can arise when working in Abjad, too.
Nothing prevents you from attaching slur indicators to mismatched voices in Abjad. But
LilyPond won't know how to render your score if you do.

These and other constraints fall under the category of LilyPond wellformedness. As of
Abjad 3.2 it's no longer clear whether these considerations need to be documented for
Abjad users: because spanners no longer exist in Abjad, users are free to attach any
indicator to any note, rest, chord. The remainder of this page documents previous
concerns about mismatched LilyPond voices. I'll leave the content mothballed until it's
clear whether we need it. (Bača.)

A logical voice is a structural relationship. Abjad uses the concept of the logical voice
to bind together all the notes, rests, chords and tuplets that comprise a single musical
voice.

It's important to understand what logical voices are and how they impact the way that you
may group notes, rests and chords together with beams, slurs and other spanners.

Logical voices and explicit voices are different things. The staff below contains an
explicit voice. You can slur these notes together because notes contained in an explicit
voice always belong to the same logical voice:

::

    >>> voice = abjad.Voice("c'8 d'8 e'8 f'8")
    >>> staff = abjad.Staff([voice])
    >>> notes = abjad.select.leaves(staff)
    >>> abjad.slur(notes)
    >>> abjad.show(staff)

Here is a staff without an explicit voice. You can slur these notes together because both
Abjad and LilyPond recognize that the notes belong to the same logical voice even though
no explicit voice is present:

::

    >>> staff = abjad.Staff("g'4 fs'8 e'8")
    >>> notes = abjad.select.leaves(staff)
    >>> abjad.slur(notes)
    >>> abjad.show(staff)

**Different voice names determine different logical voices.** Now let's consider a
slightly more complex example.  The staff below contains two short voices written one
after the other.  It's unusual to think of musical voices as following one after the
other on the same staff. But the example keeps things simple while we explore the way
that the names of explicit voices impact Abjad's determination of logical voices:

::

    >>> voice_1 = abjad.Voice("c'16 d'16 e'16 f'16", name='First Short Voice')
    >>> voice_2 = abjad.Voice("e'8 d'8", name='Second Short Voice')
    >>> staff = abjad.Staff([voice_1, voice_2])
    >>> abjad.show(staff)

You can't tell that the score above comprises two voices from the notation alone. But the
LilyPond input makes this clear:

::

    >>> string = abjad.lilypond(staff)
    >>> print(string)

You can slur together the notes in the first voice:

::

    >>> notes = abjad.select.leaves(voice_1)
    >>> abjad.slur(notes)
    >>> abjad.show(staff)

And you can slur together the notes in the second voice:

::

    >>> notes = abjad.select.leaves(voice_2)
    >>> abjad.slur(notes)
    >>> abjad.show(staff)

But you can not slur together all the notes in the staff.

Why? Because the six notes in the staff above belong to two different logical voices.
Abjad will raise an exception if you try to slur these notes together. And LilyPond would
refuse to render the resulting input code even if you could.

The important point here is that explicit voices carrying different names determine
different logical voices. The practical upshot of this is that voice naming constrains
which notes, rests and chords you can group together with slurs, beams and other
spanners.

**Identical voice names determine a single logical voice.** Now let's consider an example
in which both voices carry the same name:

::

    >>> voice_1 = abjad.Voice("c''16 b'16 a'16 g'16", name='Unified Voice')
    >>> voice_2 = abjad.Voice("fs'8 g'8", name='Unified Voice')
    >>> staff = abjad.Staff([voice_1, voice_2])
    >>> abjad.show(staff)

All six notes in the staff now belong to the same logical voice. We can see that this is
the case because it's now possible to slur all six notes together:

::

    >>> voice_1_notes = abjad.select.leaves(voice_1)
    >>> voice_2_notes = abjad.select.leaves(voice_2)
    >>> all_notes = voice_1_notes + voice_2_notes
    >>> abjad.slur(all_notes)
    >>> abjad.show(staff)

We can say that this example comprises two explicit voices but only a single logical
voice. The LilyPond input code also makes this clear:

::

    >>> string = abjad.lilypond(staff)
    >>> print(string)

**The importance of naming voices.** What happens if we choose not to name the explicit
voices we create?  It is clear that the staff below contains two explicit voices. But
because the explicit voices are unnamed it isn't clear how many logical voices the staff
defines.  Do the notes below belong to one logical voice or two?

::

    >>> voice_1 = abjad.Voice("c'8 e'16 fs'16")
    >>> voice_2 = abjad.Voice("g'16 gs'16 a'16 as'16")
    >>> staff = abjad.Staff([voice_1, voice_2])
    >>> abjad.show(staff)

Abjad defers to LilyPond in answering this question. LilyPond interprets successive
unnamed voices as constituting different voices; Abjad follows this convention. This
means that you can slur together the notes in the first voice. And you can slur together
the notes in the second voice. But you can't slur together all of the notes at once:

::

    >>> voice_1_notes = abjad.select.leaves(voice_1)
    >>> voice_2_notes = abjad.select.leaves(voice_2)
    >>> abjad.slur(voice_1_notes)
    >>> abjad.slur(voice_2_notes)
    >>> abjad.show(staff)

This point can be something of a gotcha. If you start working with increasingly fancy
ways of structuring your scores you can easily forget that notes in two successive (but
unnamed) voices can not be beamed or slurred together.

This leads to a best practice when working with Abjad: name the explicit voices you
create. The small score snippets we've created for the docs don't really require that
names for voices, staves and scores. But scores used to model serious music should
provide explicit names for every context from the beginning.
