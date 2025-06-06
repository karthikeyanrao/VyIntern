const mainContainer = document.getElementById('main');
const inputGroup = document.getElementById('iG');
const taskInput = document.getElementById('tI');
const addButton = document.getElementById('aB');
const taskContainer = document.createElement('div');
taskContainer.className = 'task-container';
mainContainer.appendChild(taskContainer);
function addTask() {
    const taskText = taskInput.value.trim();
    if (taskText) {
       const taskElement = document.createElement('div');
        taskElement.className = 'task-item d-flex align-items-center justify-content-between p-3 mb-2 bg-white rounded shadow-sm';
        const taskSpan = document.createElement('span');
        taskSpan.className = 'task-text';
        taskSpan.textContent = taskText;
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn btn-danger btn-sm';
        deleteBtn.textContent = 'Delete';
        deleteBtn.onclick = function() {
            taskContainer.removeChild(taskElement);
        };
         taskElement.appendChild(taskSpan);
        taskElement.appendChild(deleteBtn);
        taskContainer.appendChild(taskElement);
        taskInput.value = '';
        taskInput.focus();
    }
}
