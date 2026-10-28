// Сохранение состояния интерфейса
let currentFilter = localStorage.getItem('taskFilter') || 'all';
let currentTheme = localStorage.getItem('taskTheme') || 'light';

// Применяем тему при загрузке
if (currentTheme === 'dark') {
    document.body.classList.add('dark-theme');
}

// Функция для обновления задач без перезагрузки
function updateTaskStatus(taskId, completed) {
    fetch(`/task/${taskId}/toggle/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ completed: completed })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Обновляем визуально
            const taskElement = document.querySelector(`#task-${taskId}`);
            if (taskElement) {
                taskElement.classList.toggle('completed', completed);
            }
            showAlert('Задача обновлена!', 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Ошибка при обновлении', 'error');
    });
}

// Удаление задачи без перезагрузки
function deleteTask(taskId) {
    if (confirm('Удалить эту задачу?')) {
        fetch(`/task/${taskId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const taskElement = document.querySelector(`#task-${taskId}`);
                if (taskElement) {
                    taskElement.remove();
                }
                showAlert('Задача удалена', 'success');
            }
        });
    }
}

// Получение CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Показ уведомлений
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible`;
    alertDiv.innerHTML = `
        ${message}
        <a href="#" class="btn-close" onclick="this.parentElement.remove()"></a>
    `;

    const container = document.querySelector('.container-fluid');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        setTimeout(() => alertDiv.remove(), 3000);
    }
}

// Фильтрация задач
function filterTasks(filter) {
    currentFilter = filter;
    localStorage.setItem('taskFilter', filter);

    fetch(`/tasks/filter/?status=${filter}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('task-list');
        if (container) {
            container.innerHTML = data.html;
        }
    });
}