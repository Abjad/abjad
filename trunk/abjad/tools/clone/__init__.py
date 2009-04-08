from abjad.tools.imports.import_functions_in_package_to_namespace import \
   _import_functions_in_package_to_namespace

print 'debug in clone init!'
print __path__[0] # debug clone
_import_functions_in_package_to_namespace(__path__[0], globals( ))
