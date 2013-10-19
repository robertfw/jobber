from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# plucked from MPTT with minor modifications for this use case
# https://github.com/django-mptt/django-mptt/blob/master/mptt/templatetags/mptt_tags.py
# thanks and credit goes to them!
class RecurseTreeNode(template.Node):
    def __init__(self, template_nodes, queryset_var):
        self.template_nodes = template_nodes
        self.queryset_var = queryset_var

    def _render_node(self, context, node):
        bits = []
        context.push()
        for child in node.children.all():
            bits.append(self._render_node(context, child))

        context['node'] = node
        context['children'] = mark_safe(''.join(bits))
        rendered = self.template_nodes.render(context)
        context.pop()
        return rendered

    def render(self, context):
        queryset = self.queryset_var.resolve(context)
        bits = [self._render_node(context, node) for node in queryset.all()]
        return ''.join(bits)


@register.tag
def recursetree(parser, token):
    """
Iterates over the nodes in the tree, and renders the contained block for each node.
This tag will recursively render children into the template variable {{ children }}.
Only one database query is required (children are cached for the whole tree)

Usage:
<ul>
{% recursetree nodes %}
<li>
{{ node.name }}
{% if not node.is_leaf_node %}
<ul>
{{ children }}
</ul>
{% endif %}
</li>
{% endrecursetree %}
</ul>
"""
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(_('%s tag requires a queryset') % bits[0])

    queryset_var = template.Variable(bits[1])

    template_nodes = parser.parse(('endrecursetree',))
    parser.delete_first_token()

    return RecurseTreeNode(template_nodes, queryset_var)