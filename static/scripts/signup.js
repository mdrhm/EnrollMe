const studentErrors = document.querySelectorAll("#student-form .form-error-message")

document.getElementById('student-form').addEventListener('submit', function (e) {
    e.preventDefault();
    let invalidData = false
    if(document.getElementById('student_first_name').value.replaceAll(" ", "") === ""){
        invalidData = true
        studentErrors[0].classList.remove("hidden")
    }
    else{
        studentErrors[0].classList.add("hidden")
    }
    if(document.getElementById('student_last_name').value.replaceAll(" ", "") === ""){
        invalidData = true
        studentErrors[1].classList.remove("hidden")
    }
    else{
        studentErrors[1].classList.add("hidden")
    }
    if(!validateEmail(document.getElementById('student_email').value)){
        invalidData = true
        studentErrors[2].classList.remove("hidden")
    }
    else{
        studentErrors[2].classList.add("hidden")
    }
    if(!validatePassword(document.getElementById('student_password').value)){
        invalidData = true
        studentErrors[3].classList.remove("hidden")
    }
    else{
        studentErrors[3].classList.add("hidden")
    }
    if(document.getElementById('student_password').value !== document.getElementById('student_confirm_password').value){
        invalidData = true
        studentErrors[4].classList.remove("hidden")
    }
    else{
        studentErrors[4].classList.add("hidden")
    }
    if(document.getElementById('student_major').getAttribute("option_id") === ""){
        invalidData = true
        studentErrors[5].classList.remove("hidden")
    }
    else{
        studentErrors[5].classList.add("hidden")
    }
    if(!validatePhone(sanitizePhoneNumber(document.getElementById('student_phone_number').value))){
        invalidData = true
        studentErrors[6].classList.remove("hidden")
    }
    else{
        studentErrors[6].classList.add("hidden")
    }
    if(document.querySelector("#student_dob").value === ""){
        invalidData = true
        studentErrors[7].classList.remove("hidden")
    }
    else{
        studentErrors[7].classList.add("hidden")
    }
    if(document.getElementById('student_sex').getAttribute("option_id") === ""){
        invalidData = true
        studentErrors[8].classList.remove("hidden")
    }
    else{
        studentErrors[8].classList.add("hidden")
    }
    if(invalidData){
        return
    }
    let data = {
        password: document.getElementById('student_password').value,
        email: document.getElementById('student_email').value,
        phone_number: sanitizePhoneNumber(document.getElementById('student_phone_number').value),
        major: document.getElementById('student_major').getAttribute("option_id"),
        first_name: document.getElementById('student_first_name').value,
        last_name: document.getElementById('student_last_name').value,
        dob: document.getElementById('student_dob').value,
        sex: document.getElementById('student_sex').getAttribute("option_id")
    }
    fetch('/students', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            window.location.href = "/enroll"
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

const professorErrors = document.querySelectorAll("#professor-form .form-error-message")

document.getElementById('professor-form').addEventListener('submit', function (e) {
    e.preventDefault();
    let invalidData = false
    if(document.getElementById('professor_first_name').value.replaceAll(" ", "") === ""){
        invalidData = true
        professorErrors[0].classList.remove("hidden")
    }
    else{
        professorErrors[0].classList.add("hidden")
    }
    if(document.getElementById('professor_last_name').value.replaceAll(" ", "") === ""){
        invalidData = true
        professorErrors[1].classList.remove("hidden")
    }
    else{
        professorErrors[1].classList.add("hidden")
    }
    if(!validateEmail(document.getElementById('professor_email').value)){
        invalidData = true
        professorErrors[2].classList.remove("hidden")
    }
    else{
        professorErrors[2].classList.add("hidden")
    }
    if(!validatePassword(document.getElementById('professor_password').value)){
        invalidData = true
        professorErrors[3].classList.remove("hidden")
    }
    else{
        professorErrors[3].classList.add("hidden")
    }
    if(document.getElementById('professor_password').value !== document.getElementById('professor_confirm_password').value){
        invalidData = true
        professorErrors[4].classList.remove("hidden")
    }
    else{
        professorErrors[4].classList.add("hidden")
    }
    if(document.getElementById('professor_department').getAttribute("option_id") === ""){
        invalidData = true
        professorErrors[5].classList.remove("hidden")
    }
    else{
        professorErrors[5].classList.add("hidden")
    }
    if(!validatePhone(sanitizePhoneNumber(document.getElementById('professor_phone_number').value))){
        invalidData = true
        professorErrors[6].classList.remove("hidden")
    }
    else{
        professorErrors[6].classList.add("hidden")
    }
    if(invalidData){
        return
    }
    let data = {
        password: document.getElementById('professor_password').value,
        email: document.getElementById('professor_email').value,
        phone_number: sanitizePhoneNumber(document.getElementById('professor_phone_number').value),
        department: document.getElementById('professor_department').getAttribute("option_id"),
        first_name: document.getElementById('professor_first_name').value,
        last_name: document.getElementById('professor_last_name').value
    }
    fetch('/professors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            window.location.href = "/dashboard"
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

const accountTypeOptions = document.querySelectorAll("#account_types option")
accountTypeOptions[0].addEventListener("click", () => {
    document.getElementById('student-form').classList.remove("hidden")
    document.getElementById('professor-form').classList.add("hidden")
    // document.querySelector('.signup-div').style.top = "15px"
    createDropDowns()
})

accountTypeOptions[1].addEventListener("click", () => {
    document.getElementById('student-form').classList.add("hidden")
    document.getElementById('professor-form').classList.remove("hidden")
    // document.querySelector('.signup-div').style.top = "13%"
    createDropDowns()
})

