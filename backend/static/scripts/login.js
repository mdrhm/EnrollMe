const account_type = document.querySelector("account").innerHTML
document.querySelector("account").remove()

document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();

    let data = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        account_type: account_type
    };
    const login = new XMLHttpRequest();
    login.withCredentials = true;
    login.addEventListener("readystatechange", function() {
        if(this.readyState === 4) {
            if(this.status == 200){
                if(account_type === 'professor') {
                    window.location.href = "/dashboard"
                }
                else if(account_type === 'student') {
                    window.location.href = "/enroll"
                }
            }
            else {
                document.querySelector(".login-error").classList.remove("hidden")
            }
        }
    });
    login.open("POST", "/login");
    login.setRequestHeader("Content-Type", "application/json");
    login.send(JSON.stringify(data));
});
