def safe_import(target_namespace, source_module_short_name, source_attribute_name,
    source_parent_package_path=None):

    #print repr(target_namespace.keys())
    #print repr(source_module_short_name)
    #print repr(source_attribute_name)
    #print repr(source_parent_package_path)

    if source_parent_package_path is None:
        try:
            source_parent_package_path = target_namespace['__name__']
        except KeyError:
            pass

    if source_parent_package_path:
        source_module_path = '{}.{}'.format(
            source_parent_package_path, source_module_short_name)
    else:
        source_module_path = source_module_short_name

    try:
        source_module = __import__(source_module_path, fromlist=['*'])
    except:
        message = 'Error importing {!r}.'.format(source_module_path)
        print message
        return

    try:
        source_attribute_value = source_module.__dict__[source_attribute_name]
    except:
        message = 'Can not import {!r} from {!r}.'.format(source_attribute_name, source_module_path)
        print message
        return

    target_namespace[source_attribute_name] = source_attribute_value
    return source_attribute_value
