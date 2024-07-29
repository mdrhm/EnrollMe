createDropDowns()
createPasswords()

function createDropDowns() {
    const inputs = document.querySelectorAll('input[autocomplete="off"]:not(#search-bar)')
    const datalists = document.querySelectorAll("datalist")
    const inputDivs = document.querySelectorAll('div:has(> input[type="dropdown"])')
    for (let i = 0; i < inputs.length; i++) {
        datalists[i].style.width = inputs[i].offsetWidth + 'px'
        inputs[i].onfocus = function () {
            datalists[i].style.display = 'block';
        };

        for (let option of datalists[i].options) {
            option.onclick = function () {
                inputs[i].value = option.innerHTML;
                inputs[i].setAttribute("option_id", option.value);
                datalists[i].style.display = 'none';
            }
        }

        document.addEventListener("click", (e) => {
            if (!inputDivs[i].contains(e.target.value)) {
                datalists[i].style.display = "none"
            }
        })

        inputs[i].oninput = function () {
            currentFocus = -1;
            var text = inputs[i].value.toUpperCase();
            for (let option of datalists[i].options) {
                if (option.innerHTML.toUpperCase().indexOf(text) > -1) {
                    option.style.display = "flex";
                } else {
                    option.style.display = "none";
                }
            }
            ;
        }
        var currentFocus = -1;
        inputs[i].onkeydown = function (e) {
            if (e.keyCode == 40) {
                currentFocus++
                addActive(datalists[i].options);
            } else if (e.keyCode == 38) {
                currentFocus--
                addActive(datalists[i].options);
            } else if (e.keyCode == 13) {
                e.preventDefault();
                if (currentFocus > -1) {
                    /*and simulate a click on the "active" item:*/
                    if (datalists[i].options) datalists[i].options[currentFocus].click();
                }
            }
        }
        if(inputs[i].getAttribute("option_id") !== ""){
            inputs[i].value = datalists[i].querySelector(`[value="${inputs[i].getAttribute("option_id")}"]`).innerHTML
        }

    }
}

function createPasswords(){
    const showPasswords = document.querySelectorAll(".show-password")
    const hidePasswords = document.querySelectorAll(".hide-password")
    const passwords = document.querySelectorAll('input[type="password"]')
    for(let i = 0; i < passwords.length; i++){
        showPasswords[i].addEventListener("click", () => {
            showPasswords[i].classList.add("hidden")
            hidePasswords[i].classList.remove("hidden")
            passwords[i].type = "text"
        })
        hidePasswords[i].addEventListener("click", () => {
            hidePasswords[i].classList.add("hidden")
            showPasswords[i].classList.remove("hidden")
            passwords[i].type = "password"
        })
    }
}

