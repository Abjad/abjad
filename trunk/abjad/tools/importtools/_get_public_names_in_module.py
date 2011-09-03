import os


def _get_public_names_in_module(module_file):
    '''Collects and returns all functions defined in module_file.'''

    result = []
    module_file = module_file.replace(os.sep, '.')
    mod = __import__(module_file, fromlist=['*'])
    for key, value in vars(mod).items():
        # if not a private function
        if not key.startswith('_'):
            if getattr(value, '__module__', None) == module_file:
                result.append(value)
    return result
