Here are the contents for the file `/advanced_features_and_security/advanced_features_and_security/bookshelf/views.py`:

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import YourModel  # Replace with your actual model
from .forms import YourForm  # Replace with your actual form

@login_required
def your_view(request):
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with your success URL
    else:
        form = YourForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

@permission_required('app_name.can_view', raise_exception=True)
def list_view(request):
    items = YourModel.objects.all()  # Replace with your actual query
    return render(request, 'bookshelf/book_list.html', {'items': items})

@permission_required('app_name.can_edit', raise_exception=True)
def edit_view(request, pk):
    item = YourModel.objects.get(pk=pk)  # Replace with your actual query
    if request.method == 'POST':
        form = YourForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with your success URL
    else:
        form = YourForm(instance=item)
    return render(request, 'bookshelf/form_example.html', {'form': form})