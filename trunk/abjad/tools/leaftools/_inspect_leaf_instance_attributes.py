def _inspect_leaf_instance_attributes(instance):
    '''Inspect an instance of any class and return three lists.
    The three lists are vanilla instance attributes, read-only class properties
    and read-write class properties. The 'vanilla' attributes are nonpropertied
    attributes. The assumption here is that composer-set attributes will occur
    only on instances (never on classes) and that, conversely, properties
    will occur only on classes (never on instances). Composers would have to
    be doing very weird things to contradict either of these two assumptions.
    '''

    # inspect class attributes
    class_attribute_names = dir(instance.__class__)
    read_only_class_properties = []
    read_write_class_properties = []
    for class_attribute_name in class_attribute_names:
        # ignore private class attributes
        if class_attribute_name.startswith('_'):
            continue
        class_attribute = getattr(instance.__class__, class_attribute_name)
        # ignore class methods
        if callable(class_attribute):
            continue
        # remember read-only class properties
        elif isinstance(class_attribute, property) and class_attribute.fset is None:
            read_only_class_properties.append(class_attribute_name)
        # remember read / write class properties
        elif isinstance(class_attribute, property) and class_attribute.fset is not None:
            read_write_class_properties.append(class_attribute_name)
        # handle exception
        else:
            message = 'user property set on class rather than instance: "%s".'
            raise ValueError(message % instance.__class__.__name__)

    # inspect instance attributes
    vanilla_instance_attributes = []
    instance_attribute_names = dir(instance)
    for instance_attribute_name in instance_attribute_names:
        # ignore private instance attributes
        if instance_attribute_name.startswith('_'):
            continue
        # ignore class attributes
        if instance_attribute_name in class_attribute_names:
            continue
        instance_attribute = getattr(instance, instance_attribute_name)
        # ignore instance methods
        if callable(instance_attribute):
            continue
        # remember public instance attributes
        vanilla_instance_attributes.append(instance_attribute_name)

    # return instance attributes and class properties sorted by access type
    return vanilla_instance_attributes, read_only_class_properties, read_write_class_properties
