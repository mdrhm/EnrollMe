document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();

    let data = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        account_type: document.getElementById('account_type').getAttribute("option_id")
    };
    const login = new XMLHttpRequest();
    login.withCredentials = true;
    login.addEventListener("readystatechange", function() {
        if(this.readyState === 4) {
            if(this.status == 200){
                if(document.getElementById('account_type').getAttribute("option_id") === 'professor') {
                    window.location.href = "/dashboard"
                }
                else if(document.getElementById('account_type').getAttribute("option_id") === 'student') {
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
