const id = document.querySelector("id").innerHTML
document.querySelector("id").remove()
fetch('/sections?professor=' + id, {
    method: 'GET',
})
    .then(response => response.json())
    .then(data => {
        const sections = document.querySelector("#sections")
        for(let section of data) {
            sections.innerHTML += `<a class="section" section-id="${section["section_id"]}" href="/section/${section["section_id"]}/edit">
<div class = "section-header">
    <div class = "section-header-1">
    <h1>${section["course_code"]} </h1>
    <h3>${section["semester"]}: ${format_date(section["start_date"])} - ${format_date(section["end_date"])} </h3>
    </div>
    <div class= "section-header-2">
    <div class = "section-header-2-left">
    <h2>${section["course_name"]}</h2>
    <h3>${section["professors"].map((professor) => {return professor["full_name"]}).join(", ")}</h3>
    </div>
    <div class="section-days"><p>${mergeMeetings(section["meeting_times"]).map((meeting) => {
                return meeting["day"] + " - " + format_time(meeting["start_time"]) + " to " + format_time(meeting["end_time"])
            }).join("</p><p>")}</p>
    </div>
    </div>
    </div>
    <div class ="section-content">
        <div>
        <p>Room: ${section["rooms"].join(", ")}</p>
        <p>Credits: ${section["credits"]}</p>
        </div>
        <div>
        <p>Seats: ${section["enrolled"]}/${section["max_capacity"]}</p>
        <p>Instruction Mode: ${section["instruction_mode"]}</p>
        </div>
        </div>
</a>`
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
