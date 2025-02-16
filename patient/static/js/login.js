
//selects all elements with the class "input
const inputs = document.querySelectorAll(".input");

//adds the class "focus" to the parent element of the input field when it gains focus
function addcl(){
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
}

//removes the class "focus" from the parent element of the input field when it loses focus and is empty
function remcl(){
	let parent = this.parentNode.parentNode;
	if(this.value == ""){
		parent.classList.remove("focus");
	}
}

//When an input field gains focus the addcl() function is called to add the "focus" class to its parent element
//When an input field loses focus the remcl() function is called to remove the "focus" class if the input field is empty.
inputs.forEach(input => {
	input.addEventListener("focus", addcl);
	input.addEventListener("blur", remcl);
});
