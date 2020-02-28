from django import template

register = template.Library()


@register.filter(name='img_100to500')
def change_image_dimension_in_filename(image_url):
    return image_url.replace('100x100', '500x500')
