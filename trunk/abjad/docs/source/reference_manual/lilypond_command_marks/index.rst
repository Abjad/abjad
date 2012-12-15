LilyPond command marks
======================

LilyPond command marks allow you to attach arbitrary LilyPond commands
to Abjad score components.


Creating LilyPond command marks
-------------------------------

Use ``marktools`` to create LilyPond command marks:

::

   >>> lilypond_command_mark = marktools.LilyPondCommandMark('bar "||"', 'after')


::

   >>> lilypond_command_mark
   LilyPondCommandMark('bar "||"')



Attaching LilyPond command marks to Abjad components
----------------------------------------------------

Use ``attach()`` to attach a LilyPond command mark to any Abjad component:

::

   >>> import copy
   >>> staff = Staff([])
   >>> key_signature = contexttools.KeySignatureMark('f', 'major')
   >>> key_signature.attach(staff)
   KeySignatureMark(NamedChromaticPitchClass('f'), Mode('major'))(Staff{})
   >>> staff.extend(p("{ d''16 ( c''16 fs''16 g''16 ) }"))
   >>> staff.extend(p("{ f''16 ( e''16 d''16 c''16 ) }"))
   >>> staff.extend(p("{ cs''16 ( d''16 f''16 d''16 ) }"))
   >>> staff.extend(p("{ a'8 b'8 }"))
   >>> staff.extend(p("{ d''16 ( c''16 fs''16 g''16 )} "))
   >>> staff.extend(p("{ f''16 ( e''16 d''16 c''16 ) }"))
   >>> staff.extend(p("{ cs''16 ( d''16 f''16 d''16 ) }"))
   >>> staff.extend(p("{ a'8 b'8 c''2 }"))


::

   >>> lilypond_command_mark.attach(staff[-2])
   LilyPondCommandMark('bar "||"')(b'8)


::

   >>> show(staff)

.. image:: images/index-1.png



Getting the LilyPond command marks attached to an Abjad component
-----------------------------------------------------------------

Use ``marktools`` to get the lilypond_command_marks attached to a leaf:

::

   >>> marktools.get_lilypond_command_marks_attached_to_component(staff[-2])
   (LilyPondCommandMark('bar "||"')(b'8),)



Detaching LilyPond command marks from components one at a time
--------------------------------------------------------------

Use ``detach()`` to detach LilyPond command marks one at a time:

::

   >>> lilypond_command_mark.detach()
   LilyPondCommandMark('bar "||"')


::

   >>> lilypond_command_mark
   LilyPondCommandMark('bar "||"')


::

   >>> show(staff)

.. image:: images/index-2.png



Detaching all LilyPond command marks attached to a component at once
--------------------------------------------------------------------

Use ``marktools`` to detach all LilyPond command marks attached to a component at once:

::

   >>> lilypond_command_mark_1 = marktools.LilyPondCommandMark('bar "||"', 'closing')
   >>> lilypond_command_mark_1.attach(staff[-2])
   LilyPondCommandMark('bar "||"')(b'8)


::

   >>> lilypond_command_mark_2 = marktools.LilyPondCommandMark('bar "||"', 'closing')
   >>> lilypond_command_mark_2.attach(staff[-16])
   LilyPondCommandMark('bar "||"')(b'8)


::

   >>> show(staff)

.. image:: images/index-3.png


::

   >>> marktools.detach_lilypond_command_marks_attached_to_component(staff[-16])
   (LilyPondCommandMark('bar "||"'),)


::

   >>> show(staff)

.. image:: images/index-4.png



Inspecting the component to which a LilyPond command mark is attached
---------------------------------------------------------------------

Use ``start_component`` to inspect the component to which a LilyPond command mark is attached:

::

   >>> lilypond_command_mark = marktools.LilyPondCommandMark('bar "||"', 'closing')
   >>> lilypond_command_mark.attach(staff[-2])
   LilyPondCommandMark('bar "||"')(b'8)


::

   >>> show(staff)

.. image:: images/index-5.png


::

   >>> lilypond_command_mark.start_component
   Note("b'8")



Getting and setting the command name of a LilyPond command mark
---------------------------------------------------------------

Set the ``command_name`` of a LilyPond command mark to change the 
LilyPond command a LilyPond command mark prints:

::

   >>> lilypond_command_mark.command_name = 'bar "|."'


::

   >>> show(staff)

.. image:: images/index-6.png



Copying LilyPond commands
-------------------------

Use ``copy.copy()`` to copy a LilyPond command mark:

::

   >>> import copy


::

   >>> lilypond_command_mark_copy_1 = copy.copy(lilypond_command_mark)


::

   >>> lilypond_command_mark_copy_1
   LilyPondCommandMark('bar "|."')


::

   >>> lilypond_command_mark_copy_1.attach(staff[-1])
   LilyPondCommandMark('bar "|."')(c''2)


::

   >>> show(staff)

.. image:: images/index-7.png


Or use ``copy.deepcopy()`` to do the same thing.


Comparing LilyPond command marks
--------------------------------

LilyPond command marks compare equal with equal command names:

::

   >>> lilypond_command_mark.command_name
   'bar "|."'


::

   >>> lilypond_command_mark_copy_1.command_name
   'bar "|."'


::

   >>> lilypond_command_mark == lilypond_command_mark_copy_1
   True


Otherwise LilyPond command marks do not compare equal.
