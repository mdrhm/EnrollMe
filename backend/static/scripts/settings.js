const account_type = document.querySelector("account").innerHTML
document.querySelector("account").remove()

createDropDowns()
document.getElementById('settings-form').addEventListener('submit', function (e) {
    e.preventDefault();
})

changePasswords = document.querySelectorAll(".change-password")
changePasswordDivs = document.querySelectorAll(".change-password-div")
changePasswordSubmits = document.querySelectorAll(".submit-change-password")
changePasswordCancels = document.querySelectorAll(".cancel-change-password")

for(let i = 0; i < changePasswords.length; i++){
    changePasswords[i].addEventListener("click", () => {
        changePasswords[i].classList.add("hidden")
        changePasswordDivs[i].classList.remove("hidden")
    })
}

for(let i = 0; i < changePasswordSubmits.length; i++) {
    changePasswordSubmits[i].addEventListener("click", () => {
        if(!validatePassword(changePasswordDivs[i].querySelector("#new_password").value)){
            document.querySelector(".new-password-error").classList.remove("hidden")
            return;
        }
        document.querySelector(".new-password-error").classList.add("hidden")
        data = {
            old_password: changePasswordDivs[i].querySelector("#old_password").value,
            new_password: changePasswordDivs[i].querySelector("#new_password").value
        }
        data[`${account_type}_id`] = id
        const savePassword = new XMLHttpRequest();
        savePassword.withCredentials = true;
        savePassword.addEventListener("readystatechange", function() {
            if(this.readyState === 4) {
                if(this.status == 200){
                    console.log('Success:', data);
                    changePasswordDivs[i].querySelector("#old_password").value = ""
                    changePasswordDivs[i].querySelector("#new_password").value = ""
                    changePasswords[i].classList.remove("hidden")
                    changePasswordDivs[i].classList.add("hidden")
                    document.querySelector(".change-password-error").classList.add("hidden")

                }
                else {
                    console.log('Error:', this.responseText);
                    document.querySelector(".change-password-error").classList.remove("hidden")
                }
            }
        });
        savePassword.open("PUT", `/${account_type}s`);
        savePassword.setRequestHeader("Content-Type", "application/json");
        savePassword.send(JSON.stringify(data));
    })
    changePasswordCancels[i].addEventListener("click", () => {
        changePasswordDivs[i].querySelector("#old_password").value = ""
        changePasswordDivs[i].querySelector("#new_password").value = ""
        changePasswords[i].classList.remove("hidden")
        changePasswordDivs[i].classList.add("hidden")
    })
}

document.querySelector('[type="submit"]').addEventListener("click", () => {
    console.log("hello")
    let data = {}
    const formFields = document.querySelectorAll("input:not(#old_password, #new_password)")
    for (let formField of formFields) {
        if (formField.getAttribute("option_id")) {
            data[formField.getAttribute("name").replaceAll("student_", "").replaceAll("professor_", "")] = formField.getAttribute("option_id")
        } else {
            data[formField.getAttribute("name").replaceAll("student_", "").replaceAll("professor_", "")] = formField.value
        }
    }
    data[`${account_type}_id`] = id
    const saveChanges = new XMLHttpRequest();
    saveChanges.withCredentials = true;
    saveChanges.addEventListener("readystatechange", function() {
        if(this.readyState === 4) {
            if(this.status == 200){
                console.log('Success:', data);
            }
            else {
                console.error('Error:', this.responseText);
            }
        }
    });
    saveChanges.open("PUT", `/${account_type}s`);
    saveChanges.setRequestHeader("Content-Type", "application/json");
    saveChanges.send(JSON.stringify(data));
})

document.querySelector(".settings-logo").addEventListener("click", () => {
    document.querySelector(".settings-div-outer").classList.remove("hidden")
})

document.querySelector(".logout-logo").addEventListener("click", () => {
    const logout = new XMLHttpRequest();
    logout.withCredentials = true;
    logout.addEventListener("readystatechange", function() {
        if(this.readyState === 4) {
            window.location.href = "/"
        }
    });
    logout.open("GET", "/logout");
    logout.setRequestHeader("Content-Type", "application/json");
    logout.send("");
})

document.querySelector(".settings-div-outer").addEventListener("click", (e) => {
    if(document.querySelector(".settings-div").contains(e.target.value)){
        document.querySelector(".settings-div-outer").classList.add("hidden")
    }
})

document.querySelector(".close-setting").addEventListener("click", (e) => {
    document.querySelector(".settings-div-outer").classList.add("hidden")
})

document.querySelector(".logo").addEventListener("click", () => {
    if(account_type === 'professor') {
        window.location.href = "/dashboard"
    }
    else if(account_type === 'student'){
        window.location.href = "/enroll"
    }
})

document.querySelector(".ai-input-div").addEventListener('submit', function (e) {
    e.preventDefault();
    let query = document.querySelector(".ai-input").value
    let currently_taking = Object.keys(enrollments)
    document.querySelector(".ai-conversation").innerHTML = `<div><div class="loader"></div></div>`
    document.querySelector(".ai-input").value = ""
    if(query.replaceAll(" ", "") !== ""){
        let data = {
            query: query,
            currently_taking: currently_taking
        }
        const ai = new XMLHttpRequest();
        ai.withCredentials = true;
        ai.addEventListener("readystatechange", function() {
            if(this.readyState === 4) {
                document.querySelector(".ai-conversation").innerHTML = JSON.parse(this.responseText)["response"]
                console.log(JSON.parse(this.responseText))
                addAICourseClicks()
                document.querySelector(".ai-container").classList.remove("hidden")
            }
        });
        ai.open("POST", "/ai");
        ai.setRequestHeader("Content-Type", "application/json");
        ai.send(JSON.stringify(data));
    }

})

function addAICourseClicks() {
    for (let course of document.querySelectorAll(".ai-conversation span")) {
        course.addEventListener("click", () => {
            if (!Object.keys(enrollments).includes(course.getAttribute("course_id"))) {
                addCourse(parseInt(course.getAttribute("course_id")))
            }

        })
    }
}

document.querySelector(".ai-logo").addEventListener("click", () => {
    document.querySelector(".ai-container").classList.toggle("hidden")
    document.querySelector(".ai-conversation").innerHTML = ""
    document.querySelector(".ai-input").value = ""

})