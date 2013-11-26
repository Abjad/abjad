LilyPond comments
=================

LilyPond comments begin with the ``%`` sign.  Abjad models LilyPond comments as
marks.


Creating LilyPond comments
--------------------------

Use ``indicatortools`` to create LilyPond comments:

::

   >>> message_1 = 'This is a LilyPond comment before a note.'
   >>> comment_1 = indicatortools.LilyPondComment(message_1, 'before')


::

   >>> comment_1
   LilyPondComment('This is a LilyPond comment before a note.')



Attaching LilyPond comments to leaves
-------------------------------------

Attach LilyPond comments to a note, rest or chord with ``attach()``:

::

   >>> note = Note("cs''4")


::

   >>> show(note)

.. image:: images/index-1.png


::

   >>> comment_1.attach(note)
   LilyPondComment('This is a LilyPond comment before a note.')(cs''4)


::

   >>> f(note)
   % This is a LilyPond comment before a note.
   cs''4


You can add LilyPond comments before, after or to the right of any leaf.


Attaching LilyPond comments to containers
-----------------------------------------

Use ``attach()`` to attach LilyPond comments to a container:

::

   >>> staff = Staff("c'8 d'8 e'8 f'8")


::

   >>> show(staff)

.. image:: images/index-2.png


::

   >>> message_1 = 'Here is a LilyPond comment before the staff.'
   >>> message_2 = 'Here is a LilyPond comment in the staff opening.'
   >>> message_3 = 'Here is another LilyPond comment in the staff opening.'
   >>> message_4 = 'LilyPond comment in the staff closing.'
   >>> message_5 = 'LilyPond comment after the staff.'


::

   >>> staff_comment_1 = indicatortools.LilyPondComment(message_1, 'before')
   >>> staff_comment_2 = indicatortools.LilyPondComment(message_2, 'opening')
   >>> staff_comment_3 = indicatortools.LilyPondComment(message_3, 'opening')
   >>> staff_comment_4 = indicatortools.LilyPondComment(message_4, 'closing')
   >>> staff_comment_5 = indicatortools.LilyPondComment(message_5, 'after')


::

   >>> staff_comment_1.attach(staff)
   LilyPondComment('Here is a LilyPond comment before the staff.')(Staff{4})
   >>> staff_comment_2.attach(staff)
   LilyPondComment('Here is a LilyPond comment in the staff opening.')(Staff{4})
   >>> staff_comment_3.attach(staff)
   LilyPondComment('Here is another LilyPond comment in the staff opening.')(Staff{4})
   >>> staff_comment_4.attach(staff)
   LilyPondComment('LilyPond comment in the staff closing.')(Staff{4})
   >>> staff_comment_5.attach(staff)
   LilyPondComment('LilyPond comment after the staff.')(Staff{4})


::

   >>> f(staff)
   % Here is a LilyPond comment before the staff.
   \new Staff {
       % Here is a LilyPond comment in the staff opening.
       % Here is another LilyPond comment in the staff opening.
       c'8
       d'8
       e'8
       f'8
       % LilyPond comment in the staff closing.
   }
   % LilyPond comment after the staff.


You can add LilyPond comments before, after, in the opening or in the closing
of any container.


Getting the LilyPond comments attached to a component
-----------------------------------------------------

Use the inspector to get the LilyPond comments attached to a component:

::

   >>> inspect(note).get_marks(indicatortools.LilyPondComment)
   (LilyPondComment('This is a LilyPond comment before a note.')(cs''4),)



Detaching LilyPond comments from a component
--------------------------------------------

Use ``detach()`` to detach LilyPond comments from a component:

::

   >>> comment_1 = inspect(note).get_marks(indicatortools.LilyPondComment)[0]


::

   >>> comment_1.detach()
   LilyPondComment('This is a LilyPond comment before a note.')


::

   >>> f(note)
   cs''4



Detaching all LilyPond comments attached to a component
-------------------------------------------------------

Write a loop to detach all LilyPond comments attached to a component:

::

   >>> comments = inspect(staff).get_marks(indicatortools.LilyPondComment)
   >>> for comment in comments:
   ...     print comment
   ... 
   LilyPondComment('Here is a LilyPond comment before the staff.')(Staff{4})
   LilyPondComment('Here is a LilyPond comment in the staff opening.')(Staff{4})
   LilyPondComment('Here is another LilyPond comment in the staff opening.')(Staff{4})
   LilyPondComment('LilyPond comment in the staff closing.')(Staff{4})
   LilyPondComment('LilyPond comment after the staff.')(Staff{4})


::

   >>> for comment in comments:
   ...     comment.detach()
   ... 
   LilyPondComment('Here is a LilyPond comment before the staff.')
   LilyPondComment('Here is a LilyPond comment in the staff opening.')
   LilyPondComment('Here is another LilyPond comment in the staff opening.')
   LilyPondComment('LilyPond comment in the staff closing.')
   LilyPondComment('LilyPond comment after the staff.')


::

   >>> f(staff)
   \new Staff {
       c'8
       d'8
       e'8
       f'8
   }



Inspecting the component to which a LilyPond comment is attached
----------------------------------------------------------------

Use ``start_component`` to inspect the component to which a LilyPond comment is
attached:

::

   >>> comment_1.attach(note)
   LilyPondComment('This is a LilyPond comment before a note.')(cs''4)


::

   >>> comment_1.start_component
   Note("cs''4")



Inspecting the contents string of a LilyPond comment
----------------------------------------------------

Use ``contents_string`` to inspect the written contents of a LiliyPond comment:

::

   >>> comment_1.contents_string
   'This is a LilyPond comment before a note.'
