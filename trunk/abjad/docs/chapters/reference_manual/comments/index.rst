Comments
========

LilyPond comments begin with the ``%`` sign.
Abjad models LilyPond comments as marks.


Creating comments
-----------------

Use mark tools to create comments:

::

	abjad> comment_1 = marktools.Comment('This is a comment before a note.', 'before')


::

	abjad> comment_1
	Comment('This is a comment before a note.')



Attaching comments to leaves
----------------------------

Attach comments to a note, rest or chord with ``attach_mark()``:

::

	abjad> note = Note("cs''4")
	abjad> show(note)

.. image:: images/comments-1.png

::

	abjad> comment_1.attach_mark(note)


::

	abjad> f(note)
	% This is a comment before a note.
	cs''4


You can add comments before, after or to the right of any leaf.


Attaching comments to containers
--------------------------------

Use ``attach_mark()`` to attach comments to any container:

::

	abjad> staff = Staff("c'8 d'8 e'8 f'8")
	abjad> show(staff)

.. image:: images/comments-2.png

::

	abjad> staff_comment_1 = marktools.Comment('Here is a comment before the staff.', 'before')
	abjad> staff_comment_2 = marktools.Comment('Here is a comment in the staff opening.', 'opening')
	abjad> staff_comment_3 = marktools.Comment('Here is another comment in the staff opening.', 'opening')
	abjad> staff_comment_4 = marktools.Comment('Comment in the staff closing.', 'closing')
	abjad> staff_comment_5 = marktools.Comment('Comment after the staff.', 'after')


::

	abjad> staff_comment_1.attach_mark(staff)
	abjad> staff_comment_2.attach_mark(staff)
	abjad> staff_comment_3.attach_mark(staff)
	abjad> staff_comment_4.attach_mark(staff)
	abjad> staff_comment_5.attach_mark(staff)


::

	abjad> f(staff)
	% Here is a comment before the staff.
	\new Staff {
		% Here is a comment in the staff opening.
		% Here is another comment in the staff opening.
		c'8
		d'8
		e'8
		f'8
		% Comment in the staff closing.
	}
	% Comment after the staff.


You can add comments before, after, in the opening or in the closing of any container.


Getting the comments attached to a component
--------------------------------------------

Use mark tools to get all the comments attached to a component:

::

	abjad> marktools.get_comments_attached_to_component(note)
	(Comment('This is a comment before a note.')(cs''4),)


Abjad returns a tuple of zero or more comments.


Detaching comments from a component one at a time
-------------------------------------------------

Use ``detach_mark()`` to detach comments from a component one at a time:

::

	abjad> comment_1 = marktools.get_comments_attached_to_component(note)[0]


::

	abjad> comment_1.detach_mark( )
	Comment('This is a comment before a note.')


::

	abjad> f(note)
	cs''4



Detaching all comments attached to a component at once
------------------------------------------------------

Or use mark tools to detach all comments attached to a component at once:

::

	abjad> for comment in marktools.get_comments_attached_to_component(staff): print comment
	Comment('Here is a comment before the staff.')(Staff{4})
	Comment('Here is a comment in the staff opening.')(Staff{4})
	Comment('Here is another comment in the staff opening.')(Staff{4})
	Comment('Comment in the staff closing.')(Staff{4})
	Comment('Comment after the staff.')(Staff{4})


::

	abjad> marktools.detach_comments_attached_to_component(staff)


::

	abjad> f(staff)
	\new Staff {
		c'8
		d'8
		e'8
		f'8
	}



Inspecting the component to which a comment is attached
-------------------------------------------------------

Use ``start_component`` to inspect the component to which a comment is attached:

::

	abjad> comment_1.attach_mark(note)


::

	abjad> comment_1.start_component
	Note("cs''4")



Inspecting comments contents string
-----------------------------------

Use ``contents_string`` to inspect the written contents of a comment:

::

	abjad> comment_1.contents_string
	'This is a comment before a note.'

