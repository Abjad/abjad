Literature examples
===================

..  abjad::
    :hide:

    import random
    random.seed(0)

..  rubric:: Bartók: *Mikrokosmos*

..  import:: abjad.demos.bartok:make_bartok_score
    :hide:

..  abjad::
    :hide:
    :stylesheet: non-proportional.ly

    score = make_bartok_score()
    show(score)

..  toctree::

    bartok

..  rubric:: Ferneyhough: *Unsichtbare Farben*

..  import:: abjad.demos.ferneyhough.make_lilypond_file:make_lilypond_file
    :hide:

..  abjad::
    :hide:

    lilypond_file = make_lilypond_file(Duration(1, 4), 6, 6)
    show(lilypond_file)

..  toctree::

    ferneyhough

..  rubric:: Ligeti: *Désordre*

..  import:: abjad.demos.desordre.make_desordre_score:make_desordre_score
    :hide:

..  abjad::
    :hide:
    :stylesheet: non-proportional.ly

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
    score = make_desordre_score([top, bottom])
    lilypond_file = documentationtools.make_ligeti_example_lilypond_file(score)
    show(lilypond_file)

..  toctree::

    ligeti

Mozart: *Musikalisches Würfelspiel*
-----------------------------------

..  import:: abjad.demos.mozart.make_mozart_lilypond_file:make_mozart_lilypond_file
    :hide:

..  abjad::
    :hide:
    :stylesheet: non-proportional.ly

    lilypond_file = make_mozart_lilypond_file()
    show(lilypond_file)

..  toctree::

    mozart

Pärt: *Cantus in Memory of Benjamin Britten*
--------------------------------------------

..  import:: abjad.demos.part:make_part_lilypond_file
    :hide:

..  abjad::
    :hide:
    :pages: 1
    :stylesheet: non-proportional.ly

    lilypond_file = make_part_lilypond_file()
    show(lilypond_file)

..  toctree::

    part