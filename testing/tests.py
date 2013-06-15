from django.test import TestCase
from kvideos.models import Video
from .models import TestModel
from django.core.exceptions import ValidationError
from django.template import TemplateSyntaxError, Template, Context

YOUTUBE_VALID_CODE = "dR14UepDQqk"
VIMEO_VALID_CODE = "45402998"

class KVideosModelTest(TestCase):
    def setUp(self):
        self.test = TestModel()
        self.test.save()
        self.valid_youtube_code = YOUTUBE_VALID_CODE
        self.invalid_youtube_code = "invalid"
        self.valid_vimeo_code = VIMEO_VALID_CODE
        self.invalid_vimeo_code = "invalid"

    def test_clean(self):
        self.assertEqual(None, Video(content_object=self.test, typ="youtube", code=self.valid_youtube_code).clean())
        with self.assertRaises(ValidationError):
            Video(content_object=self.test, typ="youtube", code=self.invalid_youtube_code).clean()

        self.assertEqual(None, Video(content_object=self.test, typ="vimeo", code=self.valid_vimeo_code).clean())
        with self.assertRaises(ValidationError):
            Video(content_object=self.test, typ="vimeo", code=self.invalid_vimeo_code).clean()

class KVideosTemplateTagTest(TestCase):
    def setUp(self):
        self.test = TestModel()
        self.test.save()
        self.youtube_video = Video(content_object=self.test, typ="youtube", code=YOUTUBE_VALID_CODE)
        self.youtube_video.save()
        self.vimeo_video = Video(content_object=self.test, typ="vimeo", code=VIMEO_VALID_CODE)
        self.vimeo_video.save()

    def test_embed_video(self):
        with_size_template = Template('{% load kvideos %}{% embed_video video 320x240 %}')
        no_size_template = Template('{% load kvideos %}{% embed_video video %}')

        rendered = with_size_template.render(Context({ 'video': self.youtube_video }))
        expected_result = '<iframe width="320" height="240" '
        expected_result += 'src="http://www.youtube.com/embed/dR14UepDQqk" '
        expected_result += 'frameborder="0" allowfullscreen>\n</iframe>\n'
        self.assertEqual(rendered,expected_result)

        rendered = with_size_template.render(Context({ 'video': self.vimeo_video }))
        expected_result = '<iframe src="http://player.vimeo.com/video/45402998?title=0&amp;byline=0&amp;portrait=0" '
        expected_result += 'width="320" height="240" frameborder="0" webkitAllowFullScreen '
        expected_result += 'mozallowfullscreen allowFullScreen>\n</iframe>\n'

        self.assertEqual(rendered,expected_result)

        rendered = no_size_template.render(Context({ 'video': self.youtube_video }))
        expected_result = '<iframe width="640" height="480" '
        expected_result += 'src="http://www.youtube.com/embed/dR14UepDQqk" '
        expected_result += 'frameborder="0" allowfullscreen>\n</iframe>\n'
        self.assertEqual(rendered,expected_result)

        rendered = no_size_template.render(Context({ 'video': self.vimeo_video }))
        expected_result = '<iframe src="http://player.vimeo.com/video/45402998?title=0&amp;byline=0&amp;portrait=0" '
        expected_result += 'width="640" height="480" frameborder="0" webkitAllowFullScreen '
        expected_result += 'mozallowfullscreen allowFullScreen>\n</iframe>\n'
        self.assertEqual(rendered,expected_result)

        with self.assertRaises(TemplateSyntaxError):
            # Bad object type test
            rendered = no_size_template.render(Context({ 'video': self.test }))

        with self.assertRaises(TemplateSyntaxError):
            bad_size_template = Template('{% load kvideos %}{% embed_video video 320x %}')

        with self.assertRaises(TemplateSyntaxError):
            bad_num_args_template = Template('{% load kvideos %}{% embed_video video 320x240 other %}')
