from django.template import TemplateSyntaxError
from nose.tools import eq_, assert_false, raises, assert_not_equal
from . import imagegenerators  # noqa
from .utils import render_tag, get_html_attrs, clear_imagekit_cache


def test_img_tag():
    ttag = r"""{% generateimage 'testspec' source=img %}"""
    clear_imagekit_cache()
    attrs = get_html_attrs(ttag)
    expected_attrs = set(['src', 'width', 'height'])
    eq_(set(attrs.keys()), expected_attrs)
    for k in expected_attrs:
        assert_not_equal(attrs[k].strip(), '')


def test_img_tag_attrs():
    ttag = r"""{% generateimage 'testspec' source=img -- alt="Hello" %}"""
    clear_imagekit_cache()
    attrs = get_html_attrs(ttag)
    eq_(attrs.get('alt'), 'Hello')


@raises(TemplateSyntaxError)
def test_dangling_html_attrs_delimiter():
    ttag = r"""{% generateimage 'testspec' source=img -- %}"""
    render_tag(ttag)


@raises(TemplateSyntaxError)
def test_html_attrs_assignment():
    """
    You can either use generateimage as an assignment tag or specify html attrs,
    but not both.

    """
    ttag = r"""{% generateimage 'testspec' source=img -- alt="Hello" as th %}"""
    render_tag(ttag)


def test_single_dimension_attr():
    """
    If you only provide one of width or height, the other should not be added.

    """
    ttag = r"""{% generateimage 'testspec' source=img -- width="50" %}"""
    clear_imagekit_cache()
    attrs = get_html_attrs(ttag)
    assert_false('height' in attrs)


def test_assignment_tag():
    ttag = r"""{% generateimage 'testspec' source=img as th %}{{ th.url }}{{ th.height }}{{ th.width }}"""
    clear_imagekit_cache()
    html = render_tag(ttag)
    assert_not_equal(html.strip(), '')
