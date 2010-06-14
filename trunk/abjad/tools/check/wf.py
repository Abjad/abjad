from abjad import checks as _checks


def wf(expr, delivery = 'boolean', runtime = 'composition'):
   r'''Check `expr` for well-formedness.

   Set the `delivery` keyword parameter to ``'boolean'``, ``'violators'`` 
   or ``'report'``.

   Set the `runtime` keyword parameter to ``'composition'`` or ``'format'``.

   Examples refer to the following score. 
   The score is not well-formed because the score contains
   a beamed quarter note. ::

      abjad> staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> staff[1].duration.written = Rational(1, 4)
      abjad> Beam(staff[:])
      abjad> f(staff)
      \new Staff {
              c'8 [
              d'4
              e'8
              f'8 ]
      }

   When ``delivery = 'report'`` print complete test results. ::

      abjad> check.wf(staff, delivery = 'report')
         0 /    1 beams overlapping
         0 /    1 containers empty
         0 /    4 flags misrepresented
         0 /    0 glissandi overlapping
         0 /    0 hairpins intermarked
         0 /    0 hairpins short
         0 /    5 ids duplicated
         0 /    0 measures improperly filled
         0 /    0 measures misdurated
         0 /    0 measures nested
         0 /    0 octavations overlapping
         0 /    5 parents missing
         1 /    4 quarters beamed
         0 /    1 spanners discontiguous
         0 /    0 tempo spanners overlapping
         0 /    4 ties mispitched

   When ``delivery = 'boolean'`` return true or false. ::

      abjad> check.wf(staff)
      False

   When ``delivery = 'violators'`` return a Python list of 
   components that are not well-formed. ::

      abjad> check.wf(staff, delivery = 'violators')
      [Note(d', 4)]

   When ``runtime = 'composition'`` allow empty containers. ::

      abjad> check.wf(Voice([ ]), runtime = 'composition')
      True

   When ``runtime = 'format'`` do not allow empty containers. ::

      abjad> check.wf(Voice([ ]), runtime = 'format')
      False

   The `runtime` parameter should be renamed `allow_empty_containers`.

   .. todo:: break into a family of related functions with longer names.
   '''
   
   results = [ ]

   if delivery == 'report':
      return _report(expr)
   if delivery == 'violators':
      return _violators(expr)

   for key, value in sorted(vars(_checks).items( )):
      checker = value( )
      if runtime == 'composition':
         if getattr(checker, 'runtime', False) == 'composition':
            continue
      results.append(checker.check(expr))
   return all(results) 


def _report(expr):
   '''Print list of badly formed components to screen.'''
   for key, value in sorted(vars(_checks).items( )):
      checker = value( )
      checker.report(expr)


def _violators(expr):
   '''Deliver list of badly formed components as list.'''
   violators = [ ]
   for key, value in sorted(vars(_checks).items( )):
      checker = value( )
      violators.extend(checker.violators(expr))
   return violators
