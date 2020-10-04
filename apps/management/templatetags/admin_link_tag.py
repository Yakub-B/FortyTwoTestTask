from django import template
from django.urls import reverse

register = template.Library()


def get_url(instance):
    app = instance._meta.app_label
    model = instance._meta.model_name

    url = reverse(f'admin:{app}_{model}_change', args=[instance.id])
    return url


class AdminEditLinkNode(template.Node):
    def __init__(self, instance):
        self.instance = template.Variable(instance)

    def render(self, context):
        try:
            instance = self.instance.resolve(context)
            return get_url(instance)
        except template.VariableDoesNotExist:
            return ''


@register.tag(name='edit_link')
def admin_edit_link(parser, token):
    try:
        tag_name, instance = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            f"{token.contents.split()[0]} tag requires exactly two arguments"
        )
    return AdminEditLinkNode(instance)
