Literature examples
===================

..  abjad::

    import abjad

..  abjad::
    :hide:

    import random
    random.seed(0)

..  rubric:: Bartók: *Mikrokosmos*

Build up a score fragment manually, piece-by-piece, in this implementation of a
few measure from Bartók's *Mikrokosmos*. 

..  abjad::
    :hide:
    :stylesheet: non-proportional.ly

    from abjad.demos import bartok
    score = bartok.make_bartok_score()
    show(score)

..  toctree::

    bartok

..  rubric:: Ferneyhough: *Unsichtbare Farben*

Use functions to create an array of nested tuplets in this implementation of
Ferneyhough's pre-compositional process.

..  abjad::
    :hide:

    from abjad.demos.ferneyhough import FerneyhoughDemo
    ferneyhough = FerneyhoughDemo()
    lilypond_file = ferneyhough.make_lilypond_file(Duration(1, 4), 6, 6)
    show(lilypond_file)

..  toctree::

    ferneyhough

..  rubric:: Ligeti: *Désordre*

Create a polymetric score by aggregating musical cells in this implementation
of Ligeti's *Désordre*.

..  abjad::
    :hide:
    :stylesheet: non-proportional.ly

    from abjad.demos import ligeti
    top = [
        [[-1, 4, 5], [-1, 4, 5, 7, 9]], 
        [[0, 7, 9], [-1, 4, 5, 7, 9]], 
        [[2, 4, 5, 7, 9], [0, 5, 7]], 
        [[-3, -1, 0, 2, 4, 5, 7]], 
        [[-3, 2, 4], [-3, 2, 4, 5, 7]], 
        [[2, 5, 7], [-3, 9, 11, 12, 14]], 
        [[4, 5, 7, 9, 11], [2, 4, 5]], 
        [[-5, 4, 5, 7, 9, 11, 12]], 
        [[2, 9, 11], [2, 9, 11, 12, 14]],
        ]
    bottom = [
        [[-9, -4, -2], [-9, -4, -2, 1, 3]], 
        [[-6, -2, 1], [-9, -4, -2, 1, 3]], 
        [[-4, -2, 1, 3, 6], [-4, -2, 1]], 
        [[-9, -6, -4, -2, 1, 3, 6, 1]], 
        [[-6, -2, 1], [-6, -2, 1, 3, -2]], 
        [[-4, 1, 3], [-6, 3, 6, -6, -4]], 
        [[-14, -11, -9, -6, -4], [-14, -11, -9]], 
        [[-11, -2, 1, -6, -4, -2, 1, 3]], 
        [[-6, 1, 3], [-6, -4, -2, 1, 3]],
        ]
    score = ligeti.make_desordre_score([top, bottom])
    lilypond_file = abjad.documentationtools.make_ligeti_example_lilypond_file(score)
    show(lilypond_file)

..  toctree::

    ligeti

..  rubric:: Mozart: *Musikalisches Würfelspiel*

Create randomly-generated scores from a corpus of LilyPond syntax strings in
this implementation of Mozart's dice game.

..  abjad::
    :hide:
    :no-stylesheet:
    :no-trim:
    :with-columns: 1

    from abjad.demos import mozart
    lilypond_file = mozart.make_mozart_lilypond_file()
    show(lilypond_file)

..  toctree::

    mozart

..  rubric:: Pärt: *Cantus in Memory of Benjamin Britten*

Build up a full-fledged score in this implementation of Pärt's *Cantus in
Memory of Benhamin Britten*.

..  abjad::
    :hide:
    :no-stylesheet:
    :no-trim:
    :pages: 1-2
    :with-columns: 2

    from abjad.demos import part
    lilypond_file = part.make_part_lilypond_file()
    show(lilypond_file)

..  toctree::

    part
