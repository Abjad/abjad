from abjad import *


def test_UserDirectives_contributions_01( ):
   '''Container user directives contributions.'''

   t = Container(macros.scale(4))
   beam = BeamSpanner(t[:])
   beam.thickness = 3
   t.directives.before.append(r"\override BeforeFoo #'bar = #'blah")
   t.directives.opening.append(r"#(set-opening-foo 'bar)")
   #t.directives.left.append(r'\foo-left')
   t.directives.right.append(r'\foo-right')
   t.directives.closing.append(r"#(set-closing-foo 'bar)")
   t.directives.after.append(r"\revert AfterFoo #'bar")

   r'''
   \override BeforeFoo #'bar = #'blah
   {
           #(set-opening-foo 'bar)
           \override Beam #'thickness = #3
           c'8 [
           d'8
           e'8
           f'8 ]
           \revert Beam #'thickness
           #(set-closing-foo 'bar)
   }
   \revert AfterFoo #'bar
   '''

   result = t.directives.contributions

   (('before', ("\\override BeforeFoo #'bar = #'blah",)),
    ('opening', ("#(set-opening-foo 'bar)",)),
    ('right', ('\\foo-right',)),
    ('closing', ("#(set-closing-foo 'bar)",)),
    ('after', ("\\revert AfterFoo #'bar",)))

   assert result == (('before', ("\\override BeforeFoo #'bar = #'blah",)), ('opening', ("#(set-opening-foo 'bar)",)), ('right', ('\\foo-right',)), ('closing', ("#(set-closing-foo 'bar)",)), ('after', ("\\revert AfterFoo #'bar",)))


def test_UserDirectives_contributions_02( ):
   '''Context user directives contributions.'''

   t = Voice(macros.scale(4))
   beam = BeamSpanner(t[:])
   beam.thickness = 3
   t.directives.before.append(r"\override BeforeFoo #'bar = #'blah")
   t.directives.opening.append(r"#(set-opening-foo 'bar)")
   #t.directives.left.append(r'\foo-left')
   t.directives.right.append(r'\foo-right')
   t.directives.closing.append(r"#(set-closing-foo 'bar)")
   t.directives.after.append(r"\revert AfterFoo #'bar")

   r'''
   \override BeforeFoo #'bar = #'blah
   \new Voice {
           #(set-opening-foo 'bar)
           \override Beam #'thickness = #3
           c'8 [
           d'8
           e'8
           f'8 ]
           \revert Beam #'thickness
           #(set-closing-foo 'bar)
   }
   \revert AfterFoo #'bar
   '''

   result = t.directives.contributions

   (('before', ("\\override BeforeFoo #'bar = #'blah",)),
    ('opening', ("#(set-opening-foo 'bar)",)),
    ('right', ('\\foo-right',)),
    ('closing', ("#(set-closing-foo 'bar)",)),
    ('after', ("\\revert AfterFoo #'bar",)))

   assert result == (('before', ("\\override BeforeFoo #'bar = #'blah",)), ('opening', ("#(set-opening-foo 'bar)",)), ('right', ('\\foo-right',)), ('closing', ("#(set-closing-foo 'bar)",)), ('after', ("\\revert AfterFoo #'bar",)))


def test_UserDirectives_contributions_03( ):
   '''Tuplet user directives contributions.'''

   t = FixedDurationTuplet((2, 8), macros.scale(3))
   beam = BeamSpanner(t[:])
   beam.thickness = 3
   t.directives.before.append(r"\override BeforeFoo #'bar = #'blah")
   t.directives.opening.append(r"#(set-opening-foo 'bar)")
   #t.directives.left.append(r'\foo-left')
   t.directives.right.append(r'\foo-right')
   t.directives.closing.append(r"#(set-closing-foo 'bar)")
   t.directives.after.append(r"\revert AfterFoo #'bar")

   r'''
   \override BeforeFoo #'bar = #'blah
   \times 2/3 {
           #(set-opening-foo 'bar)
           \override Beam #'thickness = #3
           c'8 [
           d'8
           e'8 ]
           \revert Beam #'thickness
           #(set-closing-foo 'bar)
   }
   \revert AfterFoo #'bar
   '''

   result = t.directives.contributions

   (('before', ("\\override BeforeFoo #'bar = #'blah",)),
    ('opening', ("#(set-opening-foo 'bar)",)),
    ('right', ('\\foo-right',)),
    ('closing', ("#(set-closing-foo 'bar)",)),
    ('after', ("\\revert AfterFoo #'bar",)))

   assert result == (('before', ("\\override BeforeFoo #'bar = #'blah",)), ('opening', ("#(set-opening-foo 'bar)",)), ('right', ('\\foo-right',)), ('closing', ("#(set-closing-foo 'bar)",)), ('after', ("\\revert AfterFoo #'bar",)))


def test_UserDirectives_contributions_04( ):
   '''Measure user directives contributions.'''

   t = RigidMeasure((3, 8), macros.scale(3))
   beam = BeamSpanner(t[:])
   beam.thickness = 3
   t.directives.before.append(r"\override BeforeFoo #'bar = #'blah")
   t.directives.opening.append(r"#(set-opening-foo 'bar)")
   #t.directives.left.append(r'\foo-left')
   t.directives.right.append(r'\foo-right')
   t.directives.closing.append(r"#(set-closing-foo 'bar)")
   t.directives.after.append(r"\revert AfterFoo #'bar")

   r'''
   \override BeforeFoo #'bar = #'blah
           #(set-opening-foo 'bar)
           \time 3/8
           \override Beam #'thickness = #3
           c'8 [
           d'8
           e'8 ]
           \revert Beam #'thickness
           #(set-closing-foo 'bar)
   \revert AfterFoo #'bar
   '''

   result = t.directives.contributions

   (('before', ("\\override BeforeFoo #'bar = #'blah",)),
    ('opening', ("#(set-opening-foo 'bar)",)),
    ('right', ('\\foo-right',)),
    ('closing', ("#(set-closing-foo 'bar)",)),
    ('after', ("\\revert AfterFoo #'bar",)))

   assert result == (('before', ("\\override BeforeFoo #'bar = #'blah",)), ('opening', ("#(set-opening-foo 'bar)",)), ('right', ('\\foo-right',)), ('closing', ("#(set-closing-foo 'bar)",)), ('after', ("\\revert AfterFoo #'bar",)))


def test_UserDirectives_contributions_05( ):
   '''Leaf user directives contributions.'''

   t = Note(0, (1, 8))
   t.beam.thickness = 3
   t.directives.before.append(r"\override BeforeFoo #'bar = #'blah")
   t.directives.opening.append(r"#(set-opening-foo 'bar)")
   #t.directives.left.append(r'\foo-left')
   t.directives.right.append(r'\foo-right')
   t.directives.closing.append(r"#(set-closing-foo 'bar)")
   t.directives.after.append(r"\revert AfterFoo #'bar")

   r'''
   \override BeforeFoo #'bar = #'blah
   \once \override Beam #'thickness = #3
   #(set-opening-foo 'bar)
   c'8 \foo-right
   #(set-closing-foo 'bar)
   \revert AfterFoo #'bar'''

   result = t.directives.contributions

   (('before', ("\\override BeforeFoo #'bar = #'blah",)),
    ('opening', ("#(set-opening-foo 'bar)",)),
    ('right', ('\\foo-right',)),
    ('closing', ("#(set-closing-foo 'bar)",)),
    ('after', ("\\revert AfterFoo #'bar",)))

   assert result == (('before', ("\\override BeforeFoo #'bar = #'blah",)), ('opening', ("#(set-opening-foo 'bar)",)), ('right', ('\\foo-right',)), ('closing', ("#(set-closing-foo 'bar)",)), ('after', ("\\revert AfterFoo #'bar",)))
