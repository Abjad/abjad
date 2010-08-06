import cPickle


def load_pickle(file_name):
   '''Easy interface to Python cPickle persistence module.

   ::

      abjad> t = Note(0, (1, 4))
      abjad> f(t)
      c'4
      abjad> iotools.dump_pickle(t, 'temp.pkl')

   ::

      abjad> new = iotools.load_pickle('temp.pkl') 
      abjad> new
      Note(c', 4)

   .. versionchanged:: 1.1.2
      renamed ``persistencetools.pickle_load( )`` to
      ``iotools.load_pickle( )``.

   .. versionchanged:: 1.1.2
      renamed ``persistencetools.load_pickle( )`` to
      ``iotools.load_pickle( )``.
   '''

   f = open(file_name, 'r')
   data = cPickle.load(f)
   f.close( )
   return data
