from django import template

register = template.Library()


@register.filter
def media_path(image_path):
    if image_path:
        return image_path.url
    return '/media/blog/net.png'
