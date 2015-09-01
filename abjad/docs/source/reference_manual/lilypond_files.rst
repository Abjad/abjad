LilyPond files
==============


Making LilyPond files
---------------------

Make a basic LilyPond file with the ``lilypondfiletools`` package:

..  abjad::

    staff = Staff("c'4 d'4 e'4 f'4")
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(staff)

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

Set default LilyPond global staff size and paper size like this:

..  abjad::

    lilypond_file.global_staff_size = 14
    lilypond_file.default_paper_size = 'A7', 'portrait'

..  abjad::

    print(format(lilypond_file))

..  abjad::

    show(lilypond_file)


Setting title, subtitle and composer information
------------------------------------------------

Use the LilyPond file header block to set title, subtitle and composer
information:

..  abjad::

    lilypond_file.header_block.title = markuptools.Markup('Missa sexti tonus')
    lilypond_file.header_block.composer = markuptools.Markup('Josquin')

..  abjad::

    print(format(lilypond_file))

..  abjad::

    show(lilypond_file)
