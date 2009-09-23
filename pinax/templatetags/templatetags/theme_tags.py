from django import template
from django.conf import settings

register = template.Library()


class SilkNode(template.Node):
    """Node class for silk tag """

    def __init__(self, name, attrs):
        self.name = template.Variable(name)
        self.attrs = {}
        for attr in attrs:
            key, value = attr.split("=")
            self.attrs[key] = template.Variable(value)
                

    def render(self, context):
        """Render the img tag with specified attributes"""

        joined_attrs = ''

        try:
            name = self.name.resolve(context)
            joined_attrs = self._join_attrs(context)
        except template.VariableDoesNotExist:
            print ""

        return """<img src="%spinax/images/silk/icons/%s.png" %s />""" % (settings.STATIC_URL,
                                                                          name,
                                                                          joined_attrs)

    def _join_attrs(self, context):
        attrs = ['%s="%s"' % (k, v.resolve(context)) for k, v in self.attrs.items()]
        return ' '.join(attrs)


@register.tag
def silk(parser, token):
    """Templatetag to render silk icons
    
    Usage {{ silk "image_name" arg1="value1" arg2="value2" ... }}
     
    """

    split_token = token.split_contents()

    #send name and attributes to SilkNode
    return SilkNode(split_token[1], split_token[2:])