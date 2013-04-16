import inspect


def safe_import(target_namespace, source_module_short_name, source_attribute_name,
    source_parent_package_importable_name=None):

    #print repr(target_namespace.keys())
    #print repr(source_module_short_name)
    #print repr(source_attribute_name)
    #print repr(source_parent_package_importable_name)

    if source_parent_package_importable_name is None:
        try:
            source_parent_package_importable_name = target_namespace['__name__']
        except KeyError:
            pass

    if source_parent_package_importable_name:
        source_module_importable_name = '{}.{}'.format(
            source_parent_package_importable_name, source_module_short_name)
    else:
        source_module_importable_name = source_module_short_name

    try:
        source_module = __import__(source_module_importable_name, fromlist=['*'])
    except:
        message = 'Error importing {!r}.'.format(source_module_importable_name)
        print message
        return

    try:
        source_attribute_value = source_module.__dict__[source_attribute_name]
    except:
        message = 'Can not import {!r} from {!r}.'.format(source_attribute_name, source_module_importable_name)
        print message
        return

    target_namespace[source_attribute_name] = source_attribute_value
    return source_attribute_value
