from django.shortcuts import render, redirect
from tree.models import TextNode


def editor(request):
    if request.method == 'POST':
        action = request.GET.get('action')
        if action not in ['edit', 'create']:
            raise Exception('Invalid action!')

        if action == 'create':
            TextNode.objects.create(
                title=request.POST.get('title'),
                parent_id=request.GET.get('node', None)
            )

        elif action == 'edit':
            node = TextNode.objects.get(id=request.GET.get('node'))
            node.title = request.POST.get('title')
            node.body = request.POST.get('body')
            node.save()

        return redirect('editor.views.editor')


    return render(request, 'editor.html', {
        'root_nodes': TextNode.objects.filter(parent=None)
    })
