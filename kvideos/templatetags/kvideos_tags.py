from django import template

register = template.Library()

class EmbedVideoNode(template.Node):
    def __init__(self, video_object, width, height):
        self.video_object = template.Variable(video_object)
        self.width = width
        self.height = height

    def render(self, context):
        video = self.video_object.resolve(context)
        video_template_context = {
            'code': video.code,
            'width': self.width,
            'height': self.height,
        }
        return template.loader.render_to_string("kvideos/%s.html" % video.typ, video_template_context)

def do_embed_video(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, video_object, size = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two argument" % token.contents.split()[0])

    if len(size.split("x")) != 2:
        raise template.TemplateSyntaxError("%r tag second argument should be in WIDTHxHEIGH format" % tag_name)

    try:
        width = int(size.split("x")[0])
        height = int(size.split("x")[1])
    except ValueError:
        raise template.TemplateSyntaxError("%r tag second argument should be in WIDTHxHEIGH format" % tag_name)

    return EmbedVideoNode(video_object, width, height)

register.tag('embed_video', do_embed_video)
