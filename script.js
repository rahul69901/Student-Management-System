function checkForm(form) {
    let inputs = form.querySelectorAll("input");

    for (let input of inputs) {
        if (input.value.trim() === "") {
            alert("Please fill all fields");
            return false;
        }
    }

    return true;
}

function confirmDelete() {
    return confirm("Are you sure you want to delete?");
}