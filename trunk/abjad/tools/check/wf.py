from abjad import checks as _checks


def wf(expr, delivery = 'boolean', runtime = 'composition'):
   '''Run every check in the 'check' module against expr.

      Set the 'runtime' keyword to 'composition' to run
      only those checks appropriate at composition-time.
      Abjad allow empty containers at composition-time.
      Empty container checks will NOT run.

      abjad> check.wf(Voice([ ]), runtime = 'composition')
      True

      Set the 'runtime' keyword to 'format' to run the 
      complete set of checks appropriate at format-time.
      LilyPond does NOT allow empty containers at format-time.
      Empty container check WILL run.

      abjad> check.wf(Voice([ ]), runtime = 'format')
      False'''

   results = [ ]

   if delivery == 'report':
      return _report(expr)
   if delivery == 'violators':
      return _violators(expr)

   ## TODO: Redo _checks dict iteration with proper package init. ##

   for key, value in sorted(_checks.__dict__.items( )):
      checker = value( )
      if runtime == 'composition':
         if getattr(checker, 'runtime', False) == 'composition':
            continue
      results.append(checker.check(expr))
   return all(results) 


def _report(expr):
   '''Print list of badly formed components to screen.'''
   for key, value in sorted(_checks.__dict__.items( )):
      checker = value( )
      checker.report(expr)


def _violators(expr):
   '''Deliver list of badly formed components as list.'''
   violators = [ ]
   for key, value in sorted(_checks.__dict__.items( )):
      checker = value( )
      violators.extend(checker.violators(expr))
   return violators
