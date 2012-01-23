import os


# TODO: change name to '_get_public_function_names_in_module'
def _get_public_names_in_module(module_file):
    '''Collects and returns all public functions defined in module_file.'''
    result = []
    module_file = module_file.replace(os.sep, '.')
    mod = __import__(module_file, fromlist=['*'])
    for key, value in vars(mod).items():
        if not key.startswith('_'):
            #if getattr(value, '__module__', None) == module_file:
            #    result.append(value)
            # handle public function decorated with @require
            if getattr(value, 'func_closure', None):
                module_name = getattr(value.func_closure[1].cell_contents, '__module__', None)
            # handle plain old function
            else:
                module_name = getattr(value, '__module__', None)
            if module_name == module_file:
                result.append(value)
    return result
