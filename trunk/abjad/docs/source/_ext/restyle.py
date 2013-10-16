# -*- encoding: utf-8 -*-
import importlib
import inspect
import sphinx
import types
from docutils import nodes
from sphinx import addnodes


class AbjadDoctestDirective(sphinx.util.compat.Directive):

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    def run(self):
        self.assert_has_content()
        return []


def doctree_read(app, doctree):

    classes_to_attributes = {}

    def get_unique_parts(parts):
        unique_parts = [parts[0]]
        for part in parts[1:]:
            if part != unique_parts[-1]:
                unique_parts.append(part)
            else:
                break
        return unique_parts

    for desc_node in doctree.traverse(addnodes.desc):
        if desc_node.get('domain') != 'py':
            continue

        signature_node = desc_node.traverse(addnodes.desc_signature)[0]
        module_name = signature_node.get('module')
        object_name = signature_node.get('fullname')
        object_type = desc_node.get('objtype')
        module = importlib.import_module(module_name)

        # Strip 'abjad.tools.' or 'experimental.tools.' from signature.
        # Also strip duplicate class names.
        if object_type in ('function', 'class'):
            addname_node = signature_node.traverse(addnodes.desc_addname)[0]
            text = addname_node[0].astext()
            parts = [x for x in text.split('.') if x]
            parts = get_unique_parts(parts)
            if parts[0] in ('abjad', 'experimental'):
                parts = parts[2:-1]
            text = '{}.'.format('.'.join(parts))
            addname_node[0] = nodes.Text(text)

        if object_type == 'class':
            cls = getattr(module, object_name, None)
            if cls is None:
                continue
            if cls not in classes_to_attributes:
                classes_to_attributes[cls] = {}
                attributes = inspect.classify_class_attrs(cls)
                for attribute in attributes:
                    classes_to_attributes[cls][attribute.name] = attribute
            if inspect.isabstract(cls):
                labelnode = addnodes.only(expr='html')
                labelnode.append(nodes.literal(
                    '',
                    ' abstract ',
                    classes=['attribute', 'abstract'],
                    ))
                signature_node.insert(0, labelnode)

        elif object_type in ('method', 'attribute', 'staticmethod', 'classmethod'):
            object_parts = object_name.split('.')
            cls_name, attr_name = object_name.split('.') 
            cls = getattr(module, cls_name, None)
            if cls is None:
                continue
            attr = getattr(cls, attr_name)
            inspected_attr = classes_to_attributes[cls][attr_name]
            label_node = addnodes.only(expr='html')
            defining_class = inspected_attr.defining_class
            if defining_class != cls:
                addname_node = signature_node.traverse(
                    addnodes.desc_addname)[0]
                xref_node = addnodes.pending_xref(
                    '',
                    refdomain='py',
                    refexplicit=True,
                    reftype='class',
                    reftarget='{}.{}'.format(
                        defining_class.__module__,
                        defining_class.__name__,
                        ))
                xref_node.append(nodes.literal(
                    '',
                    '{}'.format(defining_class.__name__),
                    ))
                html_only_class_name_node = addnodes.only(expr='html')
                html_only_class_name_node.append(nodes.Text('('))
                html_only_class_name_node.append(xref_node)
                html_only_class_name_node.append(nodes.Text(').'))
                latex_only_class_name_node = addnodes.only(expr='latex')
                latex_only_class_name_node.append(nodes.Text(
                    '({}).'.format(defining_class.__name__),
                    ))
                addname_node.clear()
                addname_node.append(html_only_class_name_node)
                addname_node.append(latex_only_class_name_node)
                label_node.append(nodes.literal(
                    '',
                    ' inherited ',
                    classes=['attribute', 'inherited'],
                    ))
            if getattr(attr, '__isabstractmethod__', False):
                label_node.append(nodes.literal(
                    '',
                    ' abstract ',
                    classes=['attribute', 'abstract'],
                    ))
            if isinstance(attr, types.FunctionType):
                # remove Sphinx's annotation, so we can use our own.
                signature_node.pop(0)
                label_node.append(nodes.literal(
                    '',
                    ' staticmethod ',
                    classes=['attribute', 'staticmethod'],
                    ))
            elif hasattr(attr, 'im_self') and attr.im_self is not None:
                signature_node.pop(0)
                label_node.append(nodes.literal(
                    '',
                    ' classmethod ',
                    classes=['attribute', 'classmethod'],
                    ))
            signature_node.insert(0, label_node)

def setup(app):
    app.add_directive('doctest', AbjadDoctestDirective)
    app.connect('doctree-read', doctree_read)
