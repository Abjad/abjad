import cPickle


def dump_pickle(data, file_name):
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
      renamed ``persistencetools.pickle_dump( )`` to
      ``iotools.dump_pickle( )``.

   .. versionchanged:: 1.1.2
      renamed ``persistencetools.dump_pickle( )`` to
      ``iotools.dump_pickle( )``.
   '''

   f = open(file_name, 'w')
   cPickle.dump(data, f)
   f.close( )
