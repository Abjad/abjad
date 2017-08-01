LilyPond files
==============

..  abjad::

    import abjad

Making LilyPond files
---------------------

Make a basic LilyPond file with ``LilyPondFile.new()``:

..  abjad::

    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    lilypond_file = abjad.LilyPondFile.new(staff)

..  abjad::

    lilypond_file

..  abjad::

    print(format(lilypond_file))

..  abjad::

    show(lilypond_file)


Getting header, layout and paper blocks
---------------------------------------

Basic LilyPond files also come equipped with header, layout and paper blocks:

..  abjad::

    lilypond_file.header_block

..  abjad::

    lilypond_file.layout_block

..  abjad::

    lilypond_file.paper_block


Setting global staff size and default paper size
------------------------------------------------

A LilyPondFile's global staff size and default paper size are immutable.
Set them during instantiation, or by templating a new LilyPondFile via `new()`:

Via templating:

..  abjad::

    lilypond_file = abjad.new(
        lilypond_file,
        global_staff_size=14,
        default_paper_size=('A7', 'portrait'),
        )

When instantiating:

..  abjad::

    lilypond_file = abjad.LilyPondFile.new(
        staff,
        global_staff_size=14,
        default_paper_size=('A7', 'portrait'),
        )

..  abjad::

    print(format(lilypond_file))

..  abjad::

    show(lilypond_file)


Setting title, subtitle and composer information
------------------------------------------------

Use the LilyPond file header block to set title, subtitle and composer
information:

..  abjad::

    lilypond_file.header_block.title = abjad.Markup('Missa sexti tonus')
    lilypond_file.header_block.composer = abjad.Markup('Josquin')

..  abjad::

    print(format(lilypond_file))

..  abjad::

    show(lilypond_file)
