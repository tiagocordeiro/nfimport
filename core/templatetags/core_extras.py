from django import template

register = template.Library()


@register.filter(name='original_image')
def get_original_image(image_url):
    if '-100x100' in image_url:
        image_url = image_url.replace('-100x100', '')
        return image_url.replace('image/cache/catalog', 'image/catalog')
    return image_url
