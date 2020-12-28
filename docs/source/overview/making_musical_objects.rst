Making musical objects
======================

Newcomers to Abjad usually find it easiest to make musical objects with LilyPond input.
This works because Abjad knows how to parse a basic form of LilyPond's input language:

::

    >>> string = "d'8 f' a' d'' f'' gs'4 r8 e' gs' b' e'' gs'' a'4"
    >>> voice = abjad.Voice(string)
    >>> staff = abjad.Staff([voice])
    >>> score = abjad.Score([staff])
    >>> abjad.show(score)

Abjad displays pitch information in English. But LilyPond's other input languages are
available, too:

::

    >>> string = "re'8 fa' la' re'' fa'' sold'4 r8 mi' sold' si' mi'' sold'' la'4"
    >>> voice = abjad.Voice(string, language="français")
    >>> staff = abjad.Staff([voice])
    >>> score = abjad.Score([staff])
    >>> abjad.show(score)

Consider that only a small number of musical objects carry a duration: notes, rests,
chords and the tuplets, voices, staves that contain them. All the other symbols used to
notate music are dependent on notes, rests, chords for their moment of performance (and
their location on the page). These include articulations, fingerings, pedal markings,
slurs, phrase groupings, clefs, key signatures, and many others. Abjad formalizes this
idea of a non-durated object as an indicator. You attach indicators to notes, rests,
chords as you compose:

::

    >>> key_signature = abjad.KeySignature("g", "major")
    >>> abjad.attach(key_signature, voice[0])
    >>> time_signature = abjad.TimeSignature((2, 4), partial=(1, 8))
    >>> abjad.attach(time_signature, voice[0])
    >>> articulation = abjad.Articulation("turn")
    >>> abjad.attach(articulation, voice[5])
    >>> abjad.show(score)

"Can I type indicators into LilyPond input, too?" Yes. But over time you'll probably
migrate to the make-then-attach pattern show above. The reasons for this have to do with
the way you're likely to incrementally build up musical expressions, with experience.
Important, too, is the Abjad parses only a basic subset of LilyPond's input language;
parsing all of LilyPond's input language would too tightly couple the two systems. The
time signature must still be created explicitly in the example below because Abjad
doesn't parse LilyPond's partial measure command:

::

    >>> string = r"""\key g "major" d'8 f' a' d'' f'' gs'4 - \turn r8 e' gs' b' e'' gs'' a'4"""
    >>> voice = abjad.Voice(string)
    >>> staff = abjad.Staff([voice])
    >>> score = abjad.Score([staff])
    >>> abjad.show(score)

::

    >>> time_signature = abjad.TimeSignature((2, 4), partial=(1, 8))
    >>> abjad.attach(time_signature, voice[0])
    >>> abjad.show(score)
