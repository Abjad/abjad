Formatting LilyPond files
=========================

Abjad's LilyPond file class accepts a list of items. Many LilyPond files comprise just a
score:

::

    >>> voice = abjad.Voice("c'4 d'4 e'4 f'4", name="Violin_Voice")
    >>> staff = abjad.Staff([voice], name="Violin_Staff")
    >>> score = abjad.Score([staff], name="Score")
    >>> lilypond_file = abjad.LilyPondFile(items=[score])

LilyPond version and language commands are inserted automatically:

::

    >>> string = abjad.lilypond(lilypond_file)
    >>> print(string)

You can type all other LilyPond settings directly into a string:

::

    >>> preamble = r"""#(set-global-staff-size 14)
    ...
    ... \header {
    ...     composer = \markup { Josquin }
    ...     subtitle = \markup { Agnus dei }
    ...     title = \markup { Missa sexti toni }
    ... }
    ...
    ... \layout {
    ...     indent = 0
    ... }"""

Bundle the preamble and score like this:

::

    >>> lilypond_file = abjad.LilyPondFile(items=[preamble, score])

Then everything appears together:

::

    >>> string = abjad.lilypond(lilypond_file)
    >>> print(string)

Click on the image below. Abjad generates this same LilyPond input behind the scenes when
you call show:

..  book::
    :lilypond/no-stylesheet:

    >>> abjad.show(lilypond_file)
