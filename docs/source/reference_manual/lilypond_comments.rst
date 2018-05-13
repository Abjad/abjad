LilyPond comments
=================

..  abjad::

    import abjad

LilyPond comments begin with the ``%`` sign.

You can include comments in the LilyPond output of the scores you create with
Abjad.


Creating LilyPond comments
--------------------------

Use ``abjad.LilyPondComment`` to create a LilyPond comment:

..  abjad::

    string = 'This is a LilyPond comment before a note.'
    comment_1 = abjad.LilyPondComment(string, 'before')


Understanding the interpreter representation of a LilyPond comment
------------------------------------------------------------------

..  abjad::

    comment_1

``LilyPondComment`` tells you the comment's class.

``'This is a LilyPond comments before a note.'`` tells you the contents string
of the comment.

``'before'`` tells you the slot in which the comment will be formatted.


Attaching LilyPond comments to leaves
-------------------------------------

Use ``abjad.attach()`` to attach LilyPond comments to any note, rest or chord.

You can add LilyPond comments before, after or to the right of any leaf:

..  abjad::

    note = abjad.Note("cs''4")

..  abjad::

    abjad.show(note)

..  abjad::

    abjad.attach(comment_1, note)

..  abjad::

    abjad.f(note)


Attaching LilyPond comments to containers
-----------------------------------------

Use ``abjad.attach()`` to attach LilyPond comments to a container.

You can add LilyPond comments before, after, in the opening or in the closing
of any container:

..  abjad::

    staff = abjad.Staff("c'8 d'8 e'8 f'8")

..  abjad::

    abjad.show(staff)

..  abjad::

    contents_string_1 = 'Here is a LilyPond comment before the staff.'
    contents_string_2 = 'Here is a LilyPond comment in the staff opening.'
    contents_string_3 = 'Here is another LilyPond comment in the staff opening.'
    contents_string_4 = 'LilyPond comment in the staff closing.'
    contents_string_5 = 'LilyPond comment after the staff.'

..  abjad::

    staff_comment_1 = abjad.LilyPondComment(contents_string_1, 'before')
    staff_comment_2 = abjad.LilyPondComment(contents_string_2, 'opening')
    staff_comment_3 = abjad.LilyPondComment(contents_string_3, 'opening')
    staff_comment_4 = abjad.LilyPondComment(contents_string_4, 'closing')
    staff_comment_5 = abjad.LilyPondComment(contents_string_5, 'after')

..  abjad::

    abjad.attach(staff_comment_1, staff)
    abjad.attach(staff_comment_2, staff)
    abjad.attach(staff_comment_3, staff)
    abjad.attach(staff_comment_4, staff)
    abjad.attach(staff_comment_5, staff)

..  abjad::

    abjad.f(staff)


Getting the LilyPond comments attached to a component
-----------------------------------------------------

Use ``abjad.inspect()`` to get the LilyPond comments attached to any component:

..  abjad::

    abjad.inspect(note).get_indicators(abjad.LilyPondComment)


Detaching LilyPond comments
---------------------------

Use ``abjad.detach()`` to detach LilyPond comments:

..  abjad::

    abjad.detach(comment_1, note)

..  abjad::

    abjad.f(note)

..  abjad::

    detached_comments = abjad.detach(abjad.LilyPondComment, staff)
    for comment in detached_comments: comment

..  abjad::

    abjad.f(staff)


Getting the contents string of a LilyPond comment
----------------------------------------------------

Use ``string`` to get the string contents of a LilyPond comment:

..  abjad::

    comment_1.string
