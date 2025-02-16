
//Display 3 blogs------------------------------------------------

// Function to show modal for blogs using modal ID
function showModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = "block";
    
    // Add event listener to close modal when clicking outside of it
    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            hideModal(modalId);
        }
    });
}

// Function to hide modal for blogs using modal ID
function hideModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = "none";
    
    // Remove event listener when modal is closed
    window.removeEventListener('click', function(event) {
        if (event.target == modal) {
            hideModal(modalId);
        }
    });
}




//FAQ section----------------------------------------

        const items = document.querySelectorAll(".accordion button");

function toggleAccordion() {
  const itemToggle = this.getAttribute('aria-expanded');
  
  for (i = 0; i < items.length; i++) {
    items[i].setAttribute('aria-expanded', 'false');
  }
  
  if (itemToggle == 'false') {
    this.setAttribute('aria-expanded', 'true');
  }
}

items.forEach(item => item.addEventListener('click', toggleAccordion));





//prev and next buttons for services section------------------------------------
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const boxContainer = document.querySelector('.box-container');

let counter = 0;
const boxWidth = document.querySelector('.box').offsetWidth;
const totalBoxes = document.querySelectorAll('.box').length;

nextBtn.addEventListener('click', () => {
    if (counter < totalBoxes - 4) {
        counter++;
        boxContainer.style.transform = `translateX(${-boxWidth * counter}px)`;
    }
});

prevBtn.addEventListener('click', () => {
    if (counter > 0) {
        counter--;
        boxContainer.style.transform = `translateX(${-boxWidth * counter}px)`;
    }
});




//function for risk predictor popup------------------------------------
function togglePopup() {
    var popup = document.getElementById("popup");
    popup.style.display = popup.style.display === "block" ? "none" : "block";
}


// function to blur the background when popup is display
function togglePopup() {
    var popup = document.getElementById("popup");
    var overlay = document.getElementById("overlay");
    if (popup.style.display === "block") {
        popup.style.display = "none";
        overlay.style.display = "none";
    } else {
        popup.style.display = "block";
        overlay.style.display = "block";
    }
}



//form submission for risk predictor
function submitForm() {
    var form = document.getElementById("prediction-form");
    var formData = new FormData(form);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        showAlert(data.result);
    })
    .catch(error => console.error("Error:", error));
}

function showAlert(result) {
    var alertBox = document.getElementById("custom-alert");
    var alertText = document.getElementById("alert-text");
    alertText.textContent = result;
    alertBox.style.display = "block"; // Show the alert box for results
    setTimeout(function(){ alertBox.style.display = "none"; }, 5000); // Hide alert box after 5 seconds
}

function closeAlert() {
    var alertBox = document.getElementById("custom-alert");
    alertBox.style.display = "none"; // Hide the alert box
}
