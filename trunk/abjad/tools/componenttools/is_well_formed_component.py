from abjad import checks as _checks


def is_well_formed_component(expr, allow_empty_containers = True):
   r'''True when `component` is well formed::

      abjad> staff = Staff(macros.scale(4))
      abjad> Beam(staff[:])
      abjad> componenttools.is_well_formed_component(staff)
      True

   Otherwise false::
      
      abjad> staff = Staff(macros.scale(4))
      abjad> staff[1].duration.written = Rational(1, 4)
      abjad> Beam(staff[:])
      abjad> componenttools.is_well_formed_component(staff)
      False
      
   Beam quarter notes are not well formed.
   '''
   
   results = [ ]
   for key, value in sorted(vars(_checks).items( )):
      checker = value( )
      if allow_empty_containers:
         if getattr(checker, 'runtime', False) == 'composition':
            continue
      results.append(checker.check(expr))
   return all(results) 
