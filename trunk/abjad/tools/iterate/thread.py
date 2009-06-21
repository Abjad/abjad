def thread(expr, klass, thread_signature):
   '''Iterates all instances of class `klass` that have the given 
   `thread_signature`.

   Returns a generator.

   Example::
      
      abjad> v1 = Voice(construct.scale(4))
      abjad> v2 = Voice(construct.run(2))
      abjad> v1.name = 'piccolo'
      abjad> v2.name = 'piccolo'
      abjad> s = Staff([v1, v2])
      abjad> iterate.thread(s, Note, v1.thread.signature)
      <generator object at 0x8366d8c>
      abjad> list(_)
      [Note(c', 8), Note(d', 8), Note(e', 8), Note(f', 8), Note(c', 8), Note(c', 8)]
   '''

   if isinstance(expr, klass) and expr.thread.signature == thread_signature:
      yield expr
   if isinstance(expr, (list, tuple)):
      for m in expr:
         for x in thread(m, klass, thread_signature):
            yield x
   if hasattr(expr, '_music'):
      for m in expr._music:
         for x in thread(m, klass, thread_signature):
            yield x
