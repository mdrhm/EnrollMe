const id = document.querySelector("id").innerHTML
document.querySelector("id").remove()
console.log(id)
createDropDowns()

function addActive(x) {
    if (!x) return false;
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    x[currentFocus].classList.add("active");
}
function removeActive(x) {
    for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("active");
    }
}

document.querySelector(".add-meeting-button").addEventListener("click", () => {
    meetings = document.querySelector(".meeting-time")
    new_meeting = document.createElement("tr")
    new_meeting.innerHTML = meetings.querySelector("tr:last-child").innerHTML
    new_meeting.removeChild(new_meeting.lastElementChild)
    new_meeting.innerHTML += '<td><div><img src = "/static/images/delete.png" class="remove-meeting-button" onclick="this.parentElement.parentElement.parentElement.remove()"></div></td>'
    meetings.appendChild(new_meeting)
    createDropDowns()
})

document.getElementById('section-form').addEventListener('submit', function (e) {
    e.preventDefault();
    data = {
        course_id: document.querySelector("#course_id").getAttribute("option_id"),
        meeting_times: [],
        instruction_mode: document.querySelector("#instruction_mode").getAttribute("option_id"),
        max_capacity: document.querySelector("#max_capacity").value,
        semester_id: document.querySelector("#semester_id").getAttribute("option_id")
    }
    for(let meeting of document.querySelectorAll("tr:not(:first-child)")){
        data.meeting_times.push({
            day: meeting.querySelector("#day").getAttribute("option_id"),
            start_time: meeting.querySelector("#start_time").value,
            end_time: meeting.querySelector("#end_time").value,
            professor_id: meeting.querySelector("#professor_id").getAttribute("option_id"),
            room: meeting.querySelector("#room").value
        })
    }
    if(id === 'null') {
        fetch('/sections', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                if (!data["error"]) {
                    console.log('Success:', data);
                    window.location.href = "/dashboard"
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
    else{
        data["section_id"] = id
        fetch('/sections', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                if (!data["error"]) {
                    console.log('Success:', data);
                    window.location.href = "/dashboard"
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
})