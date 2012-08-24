LilyPond comments
=================

LilyPond comments begin with the ``%`` sign.
Abjad models LilyPond comments as marks.


Creating LilyPond comments
--------------------------

Use ``marktools`` to create LilyPond comments:

::

	>>> comment_1 = marktools.LilyPondComment('This is a LilyPond comment before a note.', 'before')


::

	>>> comment_1
	LilyPondComment('This is a LilyPond comment before a note.')



Attaching LilyPond comments to leaves
-------------------------------------

Attach LilyPond comments to a note, rest or chord with ``attach()``:

::

	>>> note = Note("cs''4")


::

	>>> show(note, docs=True)

.. image:: images/lilypond-comments-1.png

::

	>>> comment_1.attach(note)


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

	>>> show(staff, docs=True)

.. image:: images/lilypond-comments-2.png

::

	>>> staff_comment_1 = marktools.LilyPondComment('Here is a LilyPond comment before the staff.', 'before')
	>>> staff_comment_2 = marktools.LilyPondComment('Here is a LilyPond comment in the staff opening.', 'opening')
	>>> staff_comment_3 = marktools.LilyPondComment('Here is another LilyPond comment in the staff opening.', 'opening')
	>>> staff_comment_4 = marktools.LilyPondComment('LilyPond comment in the staff closing.', 'closing')
	>>> staff_comment_5 = marktools.LilyPondComment('LilyPond comment after the staff.', 'after')


::

	>>> staff_comment_1.attach(staff)
	>>> staff_comment_2.attach(staff)
	>>> staff_comment_3.attach(staff)
	>>> staff_comment_4.attach(staff)
	>>> staff_comment_5.attach(staff)


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


You can add LilyPond comments before, after, in the opening or in the closing of any container.


Getting the LilyPond comments attached to a component
-----------------------------------------------------

Use ``marktools`` to get all the LilyPond comments attached to a component:

::

	>>> marktools.get_lilypond_comments_attached_to_component(note)
	(LilyPondComment('This is a LilyPond comment before a note.')(cs''4),)


Abjad returns a tuple of zero or more LilyPond comments.


Detaching LilyPond comments from a component one at a time
----------------------------------------------------------

Use ``detach()`` to detach LilyPond comments from a component one at a time:

::

	>>> comment_1 = marktools.get_lilypond_comments_attached_to_component(note)[0]


::

	>>> comment_1.detach()
	LilyPondComment('This is a LilyPond comment before a note.')


::

	>>> f(note)
	cs''4



Detaching all LilyPond comments attached to a component at once
---------------------------------------------------------------

Or use ``marktools`` to detach all LilyPond comments attached to a component at once:

::

	>>> for comment in marktools.get_lilypond_comments_attached_to_component(staff): print comment
	LilyPondComment('Here is a LilyPond comment before the staff.')(Staff{4})
	LilyPondComment('Here is a LilyPond comment in the staff opening.')(Staff{4})
	LilyPondComment('Here is another LilyPond comment in the staff opening.')(Staff{4})
	LilyPondComment('LilyPond comment in the staff closing.')(Staff{4})
	LilyPondComment('LilyPond comment after the staff.')(Staff{4})


::

	>>> marktools.detach_lilypond_comments_attached_to_component(staff)


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

Use ``start_component`` to inspect the component to which a LilyPond comment is attached:

::

	>>> comment_1.attach(note)


::

	>>> comment_1.start_component
	Note("cs''4")



Inspecting contents string of a LilyPond comment
------------------------------------------------

Use ``contents_string`` to inspect the written contents of a LiliyPond comment:

::

	>>> comment_1.contents_string
	'This is a LilyPond comment before a note.'

