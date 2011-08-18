import types


def _remove_modules_from_namespace(namespace):
    for key, value in namespace.items():
        if isinstance(value, types.ModuleType) and not key.startswith('_'):
            del(namespace[key])
