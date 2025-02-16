
var addDoctorModal = document.getElementById("addDoctorModal");


var addDoctorBtn = document.getElementById("addDoctorBtn");


addDoctorBtn.onclick = function() {
    addDoctorModal.style.display = "block";
}


window.onclick = function(event) {
    if (event.target == addDoctorModal) {
        addDoctorModal.style.display = "none";
    }
}
