Fake Docs
=========

This will show the cropped version of the staff:

::

    >>> staff = abjad.Staff("c' d' e' f'")
    >>> abjad.show(staff)

This will show the uncropped version of the staff:

..  book::
    :lilypond/no-trim:

    >>> abjad.show(staff)

This will show the single-SVG cropped version of the 4-page staff:

::

    >>> multipage_staff = abjad.Staff("c'1 d'1 e'1 f'1")
    >>> for note in multipage_staff:
    ...     page_break = abjad.LilyPondLiteral(r"\pageBreak", format_slot="after")
    ...     abjad.attach(page_break, note)
    ...
    >>> abjad.show(multipage_staff)

This will show four individual pages, because there is no single SVG for
uncropped output for the 4-page staff:

..  book::
    :lilypond/no-trim:

    >>> abjad.show(multipage_staff)

This will show pages 2, 3 and 1 of the 4-page staff:

..  book::
    :lilypond/pages: 2-3,1

    >>> abjad.show(multipage_staff)

This will show all four pages, in a 2x2 grid:

..  book::
    :lilypond/with-columns: 2
    :lilypond/pages: 1-4

    >>> abjad.show(multipage_staff)
