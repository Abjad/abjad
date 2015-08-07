Spacing music proportionally
============================

..  note::

    Abjad's proportional-by-default stylesheets have been disabled for this
    cookbook article.

..  abjad::
    :no-stylesheet:

    voice = Voice(r"c'4.. g'16 \times 2/3 { e'4 a'4 c''4 }")
    staff = Staff([voice])
    score = Score([staff])
    show(score)

Uniform stretching
------------------

..  abjad::

    override(score).spacing_spanner.uniform_stretching = True
    show(score)

Proportional notation duration
------------------------------

..  abjad::

    set_(score).proportional_notation_duration = schemetools.SchemeMoment(1, 24)
    show(score)

..  abjad::

    set_(score).proportional_notation_duration = schemetools.SchemeMoment(1, 32)
    show(score)

..  abjad::

    set_(score).proportional_notation_duration = schemetools.SchemeMoment(1, 48)
    show(score)

Strict note spacing
-------------------

..  abjad::

    override(score).spacing_spanner.strict_note_spacing = True
    show(score)

Strict grace spacing
--------------------

Handling collisions
-------------------

Base shortest duration
----------------------