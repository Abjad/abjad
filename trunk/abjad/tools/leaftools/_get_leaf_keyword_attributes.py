from abjad.tools.componenttools._Component import _Component
from abjad.exceptions import MissingSpannerError
from abjad.exceptions import MissingTempoError
from abjad.interfaces._Interface import _Interface
from abjad.tools.leaftools._inspect_leaf_instance_attributes import _inspect_leaf_instance_attributes
from abjad.tools import durationtools


_types_forbidden_to_write_as_keyword_values = (_Component, _Interface)

def _get_leaf_keyword_attributes(leaf):
    result = []
    attributes = _inspect_leaf_instance_attributes(leaf)
    vanilla_attributes, read_only_properties, read_write_properties = attributes
    #print vanilla_attributes
    #print read_only_properties
    #print read_write_properties
    #print ''
    for vanilla_attribute in vanilla_attributes:
        result.extend(_handle_vanilla_attribute(None, leaf, vanilla_attribute))
    for read_only_property in read_only_properties:
        if read_only_property in ('grace', 'spanners'):
            pass
        else:
            #print ''
            #print 'handling read-only leaf.%s ...' % read_only_property
            result.extend(_handle_read_only_property(None, leaf, read_only_property))
    #print 'PROCESSING READ / WRITE PROPERTIES NOW ...'
    for read_write_property in read_write_properties:
        #print ''
        #print 'handling read / write leaf.%s ...' % read_write_property
        result.extend(_handle_read_write_property(None, leaf, read_write_property))
    result.extend(leaf.override._get_skeleton_strings())
    result.extend(leaf.set._get_skeleton_strings())
    result.sort()
    return result


def _handle_vanilla_attribute(attribute_host_name, attribute_host, attribute_name):
    result = []
    attribute = getattr(attribute_host, attribute_name)
    if isinstance(attribute, _types_forbidden_to_write_as_keyword_values):
        return result
    if attribute_host_name is not None:
        lhs = attribute_host_name + '__' + attribute_name
    else:
        lhs = attribute_name
    rhs = repr(attribute)
    output_string = '%s = %s' % (lhs, rhs)
    result.append(output_string)
    return result


def _handle_read_only_property(property_host_name, property_host, property_name):
    result = []
    #print 'handling read-only %s.%s ...' % (property_host_name, property_name)
    try:
        attribute = getattr(property_host, property_name)
        if isinstance(attribute, _Interface):
            if property_host_name is not None:
                interface_name = property_host_name + '__' + property_name
                interface = attribute
            else:
                interface_name, interface = property_name, attribute
            result.extend(_handle_interface(interface_name, interface))
    except (MissingSpannerError, MissingTempoError):
        pass
    return result


def _handle_interface(interface_name, interface):
    result = []
    #print 'handling interface %s ...' % interface_name
    attributes = _inspect_leaf_instance_attributes(interface)
    vanilla_attributes, read_only_properties, read_write_properties = attributes
    #print ''
    #print vanilla_attributes
    #print read_only_properties
    #print read_write_properties
    #print ''
    for vanilla_attribute in vanilla_attributes:
        result.extend(_handle_vanilla_attribute(interface_name, interface, vanilla_attribute))
    for read_only_property in read_only_properties:
        result.extend(_handle_read_only_property(interface_name, interface, read_only_property))
    for read_write_property in read_write_properties:
        result.extend(_handle_read_write_property(interface_name, interface, read_write_property))
    return result


def _handle_read_write_property(property_host_name, property_host, property_name):
    result = []
    #print 'handling read-write %s.%s ...' % (property_host_name, property_name)
    # ignore _Leaf.written_duration
    if property_name == 'written':
        return result
    # ignore Note.pitch and Note.note_head.written_pitch
    if property_host_name is None and property_name == 'pitch':
        return result
    if property_host_name == 'note_head' and property_name == 'written_pitch':
        return result
    if property_host_name == 'duration' and property_name == 'target':
        return result
    attribute = getattr(property_host, property_name)
    if attribute is None:
        pass
    elif attribute == []:
        pass
    elif isinstance(attribute, _Interface):
        interface_name, interface = property_name, attribute
        result.extend(_handle_interface(interface_name, interface))
    elif not isinstance(attribute, _types_forbidden_to_write_as_keyword_values):
        if property_host_name is not None:
            lhs = property_host_name + '__' + property_name
        else:
            lhs = property_name
        rhs = repr(attribute)
        output_string = '%s = %s' % (lhs, rhs)
        result.append(output_string)
    else:
        raise ValueError('unknonwn: "%s.%r".' % (property_host_name, attribute))
    return result
