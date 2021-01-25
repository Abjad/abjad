Indicators
==========

..

----

..  rubric:: What's an indicator?

Only a small number of musical objects carry a duration: notes, rests, chords and the
tuplets, voices, staves that contain them. All the other symbols used to notate music are
dependent on notes, rests, chords for their moment of performance (and their location on
the page). These include articulations, fingerings, pedal markings, slurs, phrase
groupings, clefs, key signatures, and many others. Abjad formalizes this idea of a
non-durated object as an indicator. You attach indicators to notes, rests, chords as you
compose:

::

    >>> string = "d'8 f' a' d'' f'' gs'4 r8 e' gs' b' e'' gs'' a'4"
    >>> voice = abjad.Voice(string, name="RH_Voice")
    >>> staff = abjad.Staff([voice], name="RH_Staff")
    >>> score = abjad.Score([staff], name="Score")
    >>> abjad.show(score)

::

    >>> key_signature = abjad.KeySignature("g", "major")
    >>> abjad.attach(key_signature, voice[0])
    >>> time_signature = abjad.TimeSignature((2, 4), partial=(1, 8))
    >>> abjad.attach(time_signature, voice[0])
    >>> articulation = abjad.Articulation("turn")
    >>> abjad.attach(articulation, voice[5])
    >>> abjad.show(score)

----

..  rubric:: Attach? Or write by hand?

You can type indicators into LilyPond input, too. But over time you'll probably
migrate to the make-then-attach pattern show above. The reasons for this have to do with
the way you're likely to incrementally build up musical expressions, with experience.
Important, too, is the Abjad parses only a basic subset of LilyPond's input language;
parsing all of LilyPond's input language would too tightly couple the two systems. (The
time signature must still be created explicitly in the example above because Abjad
doesn't parse LilyPond's partial measure command.) Attaching becomes powerful when
coupled with a loop:

::

    >>> for leaf in voice[:6]:
    ...     staccato = abjad.Articulation("staccato")
    ...     abjad.attach(staccato, leaf)
    ...

    >>> abjad.show(score)

----

..  rubric:: Getting indicators

Get all the indicators attached to a note, rest, chord like this:

::

    >>> indicators = abjad.get.indicators(voice[0])
    >>> for indicator in indicators:
    ...     indicator


Filter by type and get just the articulations attached to a note, rest, chord like this:

::

    >>> abjad.get.indicators(voice[0], abjad.Articulation)

----

..  rubric:: Detaching indicators


Detach the articulations from a note, rest, chord like this:


::

    >>> indicators = abjad.detach(abjad.Articulation, voice[0])
    >>> abjad.show(score)

The function returns a tuple of the indicators detached:

::

    >>> indicators

:author:`[Ex. Joseph Haydn, Piano sonata 42, Hob. XVI/27.]`
