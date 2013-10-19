from django.shortcuts import render
from tree.models import TextNode


def home(request):
    return render(request, 'home.html', {
        'root_nodes': TextNode.objects.filter(parent=None)
    })
