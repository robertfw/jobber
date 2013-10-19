from django.db import models


class TextNode(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    see_also = models.ManyToManyField('self', null=True, blank=True)

    @property
    def breadcrumb_title(self):
        if self.parent:
            return '{} -> {}'.format(self.parent.title, self.title)
        else:
            return self.title

    def __unicode__(self):
        return self.breadcrumb_title

    @property
    def is_leaf(self):
        return self.children.all().count() == 0
