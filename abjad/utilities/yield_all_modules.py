import collections
import importlib
import types
import uqbar.apis


def yield_all_modules(paths=None):
    '''
    Yields all modules encountered in `path`.

    Returns generator.
    '''
    import abjad
    _paths = []
    if not paths:
        _paths = abjad.__path__
    elif isinstance(paths, str):
        module = importlib.import_module(paths)
        _paths.extend(module.__path__)
    elif isinstance(paths, types.ModuleType):
        _paths.extend(paths.__path__)
    elif isinstance(paths, collections.Iterable):
        for path in paths:
            if isinstance(path, types.ModuleType):
                _paths.extend(path.__path__)
            elif isinstance(path, str):
                module = importlib.import_module(path)
                _paths.extend(module.__path__)
            else:
                raise ValueError(module)
    for path in _paths:
        for source_path in uqbar.apis.collect_source_paths([path]):
            package_path = uqbar.apis.source_path_to_package_path(source_path)
            yield importlib.import_module(package_path)
