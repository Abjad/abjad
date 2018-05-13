LilyPond commands
=================

..  abjad::

    import abjad

LilyPond commands allow you to attach arbitrary LilyPond commands
to Abjad score components.


Creating LilyPond commands
--------------------------

Use ``LilyPondCommand`` to create a LilyPond command:

..  abjad::

    command = abjad.LilyPondCommand('bar "||"', 'after')


Understanding the interpreter representation of LilyPond commands
-----------------------------------------------------------------

..  abjad::

    command

``LilyPondCommand`` tells you the command's class.

``'bar "||"'`` tells you the LilyPond command to be formatted.

``'after'`` tells you where the command will be formatted relative to the leaf
to which it is attached.


Attaching LilyPond command to Abjad components
----------------------------------------------

Use ``attach()`` to attach a LilyPond command to any Abjad component:

..  abjad::

    staff = abjad.Staff()
    staff.extend("{ d''16 ( c''16 fs''16 g''16 ) }")
    staff.extend("{ f''16 ( e''16 d''16 c''16 ) }")
    staff.extend("{ cs''16 ( d''16 f''16 d''16 ) }")
    staff.extend("{ a'8 b'8 }")
    staff.extend("{ d''16 ( c''16 fs''16 g''16 )} ")
    staff.extend("{ f''16 ( e''16 d''16 c''16 ) }")
    staff.extend("{ cs''16 ( d''16 f''16 d''16 ) }")
    staff.extend("{ a'8 b'8 c''2 }")
    key_signature = abjad.KeySignature('f', 'major')
    leaf = abjad.inspect(staff).get_leaf(0)
    abjad.attach(key_signature, leaf)

..  abjad::

    abjad.attach(command, staff[-2])

..  abjad::

    show(staff)


Inspecting the LilyPond commands attached to a leaf
---------------------------------------------------

Use the inspector to get the LilyPond commands attached to a leaf:

..  abjad::

    abjad.inspect(staff[-2]).get_indicators(abjad.LilyPondCommand)


Detaching LilyPond commands
---------------------------

Use ``detach()`` to detach LilyPond commands:

..  abjad::

    abjad.detach(command, staff[-2])

..  abjad::

    show(staff)


Getting the name of a LilyPond command
--------------------------------------

Use ``name`` to get the name of a LilyPond command:

..  abjad::

    command.name


Comparing LilyPond commands
---------------------------

LilyPond commands compare equal with equal names. Otherwise LilyPond commands
do not compare equal:

..  abjad::

    command_1 = abjad.LilyPondCommand('bar "||"', 'after')
    command_2 = abjad.LilyPondCommand('bar "||"', 'before')
    command_3 = abjad.LilyPondCommand('slurUp')

..  abjad::

    command_1 == command_1
    command_1 == command_2
    command_1 == command_3

..  abjad::

    command_2 == command_1
    command_2 == command_2
    command_2 == command_3

..  abjad::

    command_3 == command_1
    command_3 == command_2
    command_3 == command_3
