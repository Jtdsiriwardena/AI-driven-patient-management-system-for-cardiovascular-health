// Get the modals
var addAssistantModal = document.getElementById("addAssistantModal");

// open the modals
var addAssistantBtn = document.getElementById("addAssistantBtn");

// When the user clicks the "Add Assistant" button, open the add Assistant modal
addAssistantBtn.onclick = function() {
    addAssistantModal.style.display = "block";
}

// When the user clicks anywhere outside of a modal, close it
window.onclick = function(event) {
    if (event.target == addAssistantModal) {
        addAssistantModal.style.display = "none";
    }
}
