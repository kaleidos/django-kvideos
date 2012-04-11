from django import template
from ..models import Video
from ..settings import *

register = template.Library()

class EmbedVideoNode(template.Node):
    def __init__(self, video_object, width, height):
        self.video_object = template.Variable(video_object)
        self.width = width
        self.height = height

    def render(self, context):
        video = self.video_object.resolve(context)
    
        if not isinstance(video, Video):
            raise template.TemplateSyntaxError("embed_video tag first argument must be a Video object")

        video_template_context = {
            'code': video.code,
            'width': self.width,
            'height': self.height,
        }
        return template.loader.render_to_string("kvideos/%s.html" % video.typ, video_template_context)

def do_embed_video(parser, token):
    splited = token.split_contents()
    if len(splited) == 3:
        (tag_name, video_object, size) = splited
    elif len(splited) == 2:
        (tag_name, video_object) = splited
        size = KVIDEOS_DEFAULT_SIZE
    else:
        raise template.TemplateSyntaxError("embed_video tag requires two or three argument")

    if len(size.split("x")) != 2:
        raise template.TemplateSyntaxError("embed_video tag second argument should be in WIDTHxHEIGH format")

    try:
        width = int(size.split("x")[0])
        height = int(size.split("x")[1])
    except ValueError:
        raise template.TemplateSyntaxError("embed_video tag second argument should be in WIDTHxHEIGH format")

    return EmbedVideoNode(video_object, width, height)

register.tag('embed_video', do_embed_video)
