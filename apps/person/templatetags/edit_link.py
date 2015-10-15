from django import template

register = template.Library()


@register.simple_tag
def edit_link(object_from_context=None):
    if object_from_context:
        app = str(object_from_context.__class__).split(" ")[1].split(".")[-1][:-2]
        model = str(object_from_context.__class__).split(" ")[1].split(".")[-3]
        object_id = str(object_from_context.id)
        url = "/admin/" + app + "/" + model + "/" + object_id + "/"
        url = url.lower()
    else:
        url = "/admin/"
    return url
