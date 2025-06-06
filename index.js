const tC = document.getElementById('tc');
function Addtask() {
    const tI = document.getElementById("ti");
    const taskText = tI.value.trim();
    if (taskText === '') {
        return;
    }  
    const taskElement = document.createElement("h3");
    taskElement.textContent = taskText;
    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.className = "delete-btn";
    deleteButton.onclick = function() {
        taskElement.remove();
    };
    taskElement.appendChild(deleteButton);
    tC.appendChild(taskElement);
    tI.value = "";
}

