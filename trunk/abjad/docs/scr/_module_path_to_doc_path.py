import os


def _module_path_to_doc_path(module_path):
   '''Transform a module path like

      /Users/foo/abjad/trunk/abjad/tools/sequencetools/zip_cyclic.py

   to a doc path like

      tools/sequencetools/zip_cyclic

   for inclusion in the API TOC.
   '''

   module_parts = module_path.split(os.sep)
   doc_parts = [ ]
   for part in reversed(module_parts):
      if part == 'abjad':
         break
      else:
         doc_parts.insert(0, part)
   doc_path = os.path.join(*doc_parts)

   # remove '.py' extension
   doc_path = doc_path[:-3]

   return doc_path
