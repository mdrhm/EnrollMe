function format_time(time){
    time_array = time.split(":")
    am_pm = parseInt(time_array[0]) < 12 ? "AM" : "PM"
    time_array[0] = parseInt(time_array[0]) % 12 == 0 ? "12" : parseInt(time_array[0]) % 12
    return `${time_array[0]}:${time_array[1]} ${am_pm}`
}
function format_date(date){
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    date = new Date(date)
    return `${months[date.getMonth()]} ${date.getDate() + 1}`
}

function mergeMeetings(meetings){
    let uniqueTimes = []
    let uniqueMeetings = []
    for(let meeting of meetings){
        if(!(uniqueTimes.map((m) => {return m[0] + "-" + m[1]})).includes(meeting["start_time"] + "-" + meeting["end_time"])){
            uniqueTimes.push([meeting["start_time"],meeting["end_time"]])
        }
    }
    console.log(uniqueTimes)
    for(let time of uniqueTimes){
        uniqueMeetings.push({
            day: meetings.filter((m) => {return m["start_time"] === time[0] && m["end_time"] === time[1]}).map((m) => {return m["day"]}).join(", "),
            start_time: time[0],
            end_time: time[1]
        })
    }
    return uniqueMeetings
}

function validatePassword(password) {
    const minLength = 8;
    const hasLetter = /[a-zA-Z]/;
    const hasNumber = /\d/;
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/;

    if (password.length < minLength) {
        return false;
    }
    if (!hasLetter.test(password)) {
        return false;
    }
    if (!hasNumber.test(password)) {
        return false;
    }
    if (!hasSpecialChar.test(password)) {
        return false;
    }
    return true;
}

function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

function validatePhone(phone) {
    const phonePattern = /^(?:\(\d{3}\)|\d{3}-|\d{3} )?\d{3}-?\d{4}$/;
    return phonePattern.test(phone);
}

function sanitizePhoneNumber(phone) {
    const digits = phone.replace(/\D/g, '');

    if (digits.length !== 10) {
        return null;
    }
    const formattedPhone = `${digits.substring(0, 3)}-${digits.substring(3, 6)}-${digits.substring(6)}`;
    return formattedPhone;
}
