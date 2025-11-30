from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from .models import Todo

# Form for Todo model
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date', 'resolved']

# List all TODOs
def todo_list(request):
    todos = Todo.objects.all().order_by('-created_at')
    return render(request, 'todo_app/todo_list.html', {'todos': todos})

# Create a new TODO
def todo_create(request):
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_app:todo_list')
    return render(request, 'todo_app/todo_form.html', {'form': form, 'form_title': 'Create New Todo'})

# View a single TODO
def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    return render(request, 'todo_app/todo_detail.html', {'todo': todo})

# Edit an existing TODO
def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    form = TodoForm(instance=todo)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_app:todo_list')
    return render(request, 'todo_app/todo_form.html', {'form': form, 'form_title': 'Edit Todo', 'todo': todo})

# Delete a TODO
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_app:todo_list')
    return render(request, 'todo_app/todo_confirm_delete.html', {'todo': todo})

# Toggle the 'resolved' status of a TODO
def todo_toggle_resolved(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.resolved = not todo.resolved
        todo.save()
    return redirect('todo_app:todo_list')