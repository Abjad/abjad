'''Set MenuSection.return_value_attribute to one of 'body', 'key' or 'number'.
The behavior of the setting interacts with string tokens and tuple tokens as follows.
Behaviors marked (NB) are cases of forgiveness implemented such that the
system will always supply a return value, even where the return value
has to be selected from the next most likely available attribute.

When section has string tokens ...

    With numbering turned off ...

        * return body/key when return_value_attribute set to 'number' (NB)
        * return body/key when return_value_attribute set to 'key'
        * return body/key when return_value_attribute set to 'body'

    With numbering turned on ...

        * return number when return_value_attribute set to 'number'
        * return body/key when return_value_attribute set to 'key'
        * return body/key when return_value_attribute set to 'body'

When section has tuple tokens ...

    With numbering turned off ...

        * return key when return_value_attribute set to 'number' (NB)
        * return key when return_value_attribute set to 'key'
        * return body when return_value_attribute set to 'body'

    With numbering turned on ...

        * return number when return_value_attribute set to 'number'
        * return key when return_value_attribute set to 'key'
        * return body when return_value_attribute set to 'body'
'''

from MenuSection import MenuSection
