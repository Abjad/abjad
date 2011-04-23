from abjad import checks as _checks


def tabulate_well_formedness_violations_in_expr(expr, allow_empty_containers = True):
   r'''.. versionadded:: 1.1.1

   Tabulate well-formedness violations in `expr`::

      abjad> staff = Staff(macros.scale(4))
      abjad> staff[1].duration.written = Fraction(1, 4)
      abjad> spannertools.BeamSpanner(staff[:])
      abjad> f(staff)
      \new Staff {
              c'8 [
              d'4
              e'8
              f'8 ]
      }

   ::

      abjad> componenttools.tabulate_well_formedness_violations_in_expr(staff)
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

   Beamed quarter notes are not well formed.
   '''
   
   for key, value in sorted(vars(_checks).items( )):
      checker = value( )
      checker.report(expr)
