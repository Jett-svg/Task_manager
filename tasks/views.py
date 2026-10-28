from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

from .models import Task
from .forms import TaskForm


def task_list(request):
    """Список всех задач"""
    tasks = Task.objects.all()

    # Фильтрация
    status = request.GET.get('status', 'all')
    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'active':
        tasks = tasks.filter(completed=False)

    # Поиск
    search = request.GET.get('search', '')
    if search:
        tasks = tasks.filter(title__icontains=search)

    # Для AJAX запросов возвращаем только HTML
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'html': render(request, 'tasks/partials/task_list.html', {
                'tasks': tasks
            }).content.decode()
        })

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'current_status': status,
        'search_query': search
    })


def task_create(request):
    """Создание новой задачи"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Новая задача'
    })


def task_toggle(request, task_id):
    """Переключение статуса задачи (AJAX)"""
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        data = json.loads(request.body)
        task.completed = data.get('completed', not task.completed)
        task.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def task_delete(request, task_id):
    """Удаление задачи (AJAX)"""
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def task_stats(request):
    """Статистика по задачам"""
    total = Task.objects.count()
    completed = Task.objects.filter(completed=True).count()
    active = total - completed

    by_priority = {
        'high': Task.objects.filter(priority='high').count(),
        'medium': Task.objects.filter(priority='medium').count(),
        'low': Task.objects.filter(priority='low').count(),
    }

    return render(request, 'tasks/task_stats.html', {
        'total': total,
        'completed': completed,
        'active': active,
        'by_priority': by_priority
    })