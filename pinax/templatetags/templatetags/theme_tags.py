from django import template
from django.conf import settings

register = template.Library()


class SilkNode(template.Node):
    """Node class for silk tag """

    def __init__(self, name, attrs):
        self.name = template.Variable(name)
        self.attrs = [template.Variable(attr) for attr in attrs]

    def render(self, context):
        """Render the img tag with specified attributes"""

        joined_attrs = '' 

        try:
            name = self.name.resolve(context)
            joined_attrs = ' '.join([var.resolve(context) for var in self.attrs])
        except template.VariableDoesNotExist:
            print ""

        return """<img src="%spinax/images/silk/icons/%s.png" %s />""" % (settings.STATIC_URL,
                                                                          name,
                                                                          joined_attrs)

@register.tag
def silk(parser, token):
    """Templatetag to render silk icons
    
    Usage {{ silk "image_name" arg1="value1" arg2="value2" ... }}
     
    """
    try:
        split_token = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag has argument errors" % token.split_contents()[0]
    
    #send name and attributes to SilkNode
    return SilkNode(split_token[1], split_token[2:])