from django import template
from django.conf import settings

register = template.Library()

@register.tag
def silk(parser, token):
    """Templatetag to render silk icons
    
    Usage {{ silk "image_name" arg1="value1" arg2="value2" ... }}
     
    """
    try:
        split_token = token.split_contents()

        # get name and remove quotes
        name = split_token[1][1:-1]
    
        # get all arguments and join them.
        attrs = ' '.join(split_token[2:])
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag has argument errors" % token.split_contents()[0] 
    
    return SilkNode(name, attrs) 

class SilkNode(template.Node):

    def __init__(self, name, attrs):
        self.name = name
        self.attrs = attrs

    def render(self, context):
        """Render the img tag with specified attributes"""
        
        return """<img src="%spinax/images/silk/icons/%s.png" %s />""" % (settings.STATIC_URL, 
                                                                          self.name,
                                                                          self.attrs)
