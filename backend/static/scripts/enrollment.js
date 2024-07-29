let courses = JSON.parse(coursesStr)
let sections = JSON.parse(sectionsStr)
let previousEnrollments = JSON.parse(enrollmentStr)
const id = document.querySelector("id").innerHTML
document.querySelector("id").remove()
document.querySelector(".dummy-script").remove()
let enrollments = {}
initializeEnrollments()
addCourseClick()
document.querySelector("#search-bar").addEventListener("input", () =>
{
    let input = document.getElementById('search-bar').value.toLowerCase();
    const result = document.querySelector(".search-results")
    const resultInner = document.querySelector(".search-results-inner")
    Array.from(document.querySelectorAll(".course")).forEach((course) => {
        course.classList.add("hidden")
    })
    result.classList.remove("hidden")
    if (input.replaceAll(" ", "") === "") {
        result.classList.add("hidden")
        return;
    }
    Array.from(document.querySelectorAll(".course")).filter((course) => {
      return course.innerText.toLowerCase().indexOf(input) > 0 && !Object.keys(enrollments).includes(course.getAttribute("course_id"))
    }).forEach((course) => {
        course.classList.remove("hidden")
    })
})

function addCourseClick(){
    for(let c of document.querySelectorAll(".course")){
        c.addEventListener("click", () => {
            course_id = parseInt(c.getAttribute("course_id"))
            console.log(course_id)
            document.querySelector(".search-results").classList.add("hidden")
            document.querySelector("#search-bar").value = ""
            addCourse(course_id)
        })
    }
}

function addSectionClicks(){
    for (let section of document.querySelectorAll(".course-section-div")){
        section.addEventListener("click", () => {
            console.log(section.getAttribute("section_id"))
            addSectionToEnroll(section.getAttribute("section_id"))
            for(let otherSection of section.parentElement.children){
                otherSection.classList.remove("selected")
            }
            section.classList.add("selected")
            let sectionInfo = sections.filter((s) => {return s["section_id"] === parseInt(section.getAttribute("section_id"))})[0]
            section.parentElement.parentElement.querySelector(".section-info-div").innerHTML = `<p>${mergeMeetings(sectionInfo["meeting_times"]).map((meeting) => {
                return meeting["day"] + " - " + format_time(meeting["start_time"]) + " to " + format_time(meeting["end_time"])
            }).join("</p><p>")}</p> <div><p>${sectionInfo["professors"].map((professor) => {return professor["full_name"]}).join(", ")}</p> <p>${sectionInfo["rooms"].join(", ")}</p> </div> <div> <p>Seats: ${sectionInfo["enrolled"]}/${sectionInfo["max_capacity"]}</p> <p>${sectionInfo["instruction_mode"]}</p> </div>`
        })
    }
}
function addSectionToEnroll(section_id){
    let section = sections.filter((section) => {return section["section_id"] === parseInt(section_id)})[0]
    enrollments[section["course_id"]] = section
    displayEnrollments()
}

function displayEnrollments(){
    const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    const scheduleCourses = document.querySelector(".schedule-courses")
    scheduleCourses.innerHTML = ""
    for(section of Object.values(enrollments)){
        for(meeting of section["meeting_times"]){
            let hours = (new Date(`July 1, 1999, ${meeting["end_time"]}`).getTime() - new Date(`July 1, 1999, ${meeting["start_time"]}`).getTime())/3600000
            let day = days.indexOf(meeting["day"])
            let start = (new Date(`July 1, 1999, ${meeting["start_time"]}`).getTime() - new Date(`July 1, 1999, 0:00:00`).getTime())/3600000
            scheduleCourses.innerHTML += `<div class="schedule-course ${(section["enrolled"] === section["max_capacity"]) ? "full" : ""} ${(previousEnrollments.includes(section["section_id"]) ? "enrolled" : "")}" style="--hours: ${hours}; --day: ${day}; --start: ${start};"><p>${section["course_code"]}</p><p>${format_time(meeting["start_time"])} to ${format_time(meeting["end_time"])}</p></div>`
        }
    }
    disableButtonOnConflict()
    document.querySelector(".credits").innerHTML = Object.values(enrollments).map((section) => {return section["credits"]}).reduce((sum, a) => sum + a, 0).toFixed(1)
}

function removeCourse(course){
    let courseDiv = Array.from(document.querySelectorAll(".course-div")).filter((el) => {return el.contains(course)})[0]
    let course_id = courseDiv.getAttribute("course_id")
    console.log(course_id)
    if (courseDiv.querySelector(".course-status").innerHTML !== "Added to Cart"){
        courseDiv.classList.add("dropped")
        courseDiv.querySelector(".course-status").innerHTML = "Not Dropped Yet"
    }
    else{
        courseDiv.remove()
    }
    delete enrollments[course_id];
    displayEnrollments()
}

function addCourseBack(course){
    let courseDiv = Array.from(document.querySelectorAll(".course-div")).filter((el) => {return el.contains(course)})[0]
    let course_id = courseDiv.getAttribute("course_id")
    let section_id = courseDiv.querySelector(".course-section-div.selected").getAttribute("section_id")
    console.log(course_id)
    courseDiv.classList.remove("dropped")
    courseDiv.querySelector(".course-status").innerHTML = "Enrolled"
    enrollments[course_id] = sections.filter((s) => {return s["section_id"] === parseInt(section_id)})[0];
    displayEnrollments()
}

function submitEnrollment(){
    document.querySelector(".submit-enrollment").innerHTML = "Enrolling..."
    document.querySelector(".submit-enrollment").classList.add("disabled")
    const data = {
        student_id: id,
        sections: Object.values(enrollments).map((section) => {return section["section_id"]}).filter((section_id) => {return section_id})
    }
    previousEnrollments = data["sections"]
    const enrollmentsSubmit = new XMLHttpRequest();
    enrollmentsSubmit.withCredentials = true;
    enrollmentsSubmit.addEventListener("readystatechange", function() {
        if(this.readyState === 4) {
            console.log(this.responseText);
            document.querySelector(".submit-enrollment").innerHTML = "Enrolled"
            initializeEnrollments()
            setTimeout(() => {
                document.querySelector(".submit-enrollment").innerHTML = "Enroll"
                document.querySelector(".submit-enrollment").classList.remove("disabled")
            }, 5000);
        }
    });
    enrollmentsSubmit.open("PUT", "/enrollments");
    enrollmentsSubmit.setRequestHeader("Content-Type", "application/json");
    enrollmentsSubmit.send(JSON.stringify(data));
}

function initializeEnrollments(){
    for(let enrollment of previousEnrollments){
        document.querySelector(".courses-div").innerHTML = ''
        let section = sections.filter((section) => {return section["section_id"] === parseInt(enrollment)})[0]
        enrollments[section["course_id"]] = section
        displayEnrollments()
    }
    for(let course of Object.keys(enrollments)){
        addCourse(parseInt(course))
    }
}

function addCourse(course_id){
    let course = courses.filter((currentCourse) => {return currentCourse["course_id"] === course_id})[0]
    console.log(course)
    let course_sections = sections.filter((section) => {return section["course_id"] === course_id})
    document.querySelector(".courses-div").innerHTML += `<div class = "course-div" course_id = ${course["course_id"]}><div class="course-div-header"><div class="course-status">${(course_sections.map((s) => {return s["section_id"]}).filter((s) => {return previousEnrollments.includes(s)}).length > 0) ? "Enrolled" : "Added to Cart"}</div><div><img src="/static/images/delete.png" class="remove-course-button" onclick="removeCourse(this)"><img src="/static/images/plus.png" class="add-course-back-button" onclick="addCourseBack(this)"></div></div><h2>${course["subject"]} ${course["course_level"]}</h2><h3>${course["name"]}</h3><h4>Credits: ${course["credits"]}</h4><p>Description: ${course["description"]}</p>
                    Sections: ${(course_sections.length > 0) ? `<div class="sections-div">${course_sections.map((section) => {return `<div class = "course-section-div" section_id="${section["section_id"]}">${section["section_id"]}</div>`}).join("")}</div><div class="section-info-div hidden"></div><div><img src="static/images/dropdown.png" class="expand-course"></div>` : `<p class="no-sections">There are currently no sections offered for this course</p>`}`

    addSectionClicks()
    addExpandClicks()
    let previouslyEnrolledSection = course_sections.map((s) => {return s["section_id"]}).filter((s) => {return previousEnrollments.includes(s)})
    if(previouslyEnrolledSection.length > 0){
        document.querySelector(`[section_id="${previouslyEnrolledSection[0]}"]`).click()
    }
    else {
        for (let section of document.querySelectorAll(`[course_id="${course_id}"] .course-section-div`)) {
            section.click()
            if (!checkForConclicts()["conflict"]) {
                break;
            }
        }
    }
}

function checkForConclicts(){
    if(Object.values(enrollments).map((section) => {return section["credits"]}).reduce((sum, a) => sum + a, 0) > 17){
        return {conflict: true, message: "Exceeding maxmimum amount of credits"}
    }
    if(Object.values(enrollments).filter((section) => {
        return section["enrolled"] == section["max_capacity"] &&
            !section["roster"].map((student) => {
                return student["student_id"]
            }).includes(parseInt(id))}).length > 0){
        return {conflict: true, message: "At least of one the classes are full"}
    }
    let scheduleInfo = Array.from(document.querySelectorAll(".schedule-course")).map((element) => {return {
        day: parseFloat(getComputedStyle(element).getPropertyValue('--day')),
        start: parseFloat(getComputedStyle(element).getPropertyValue('--start')),
        hours: parseFloat(getComputedStyle(element).getPropertyValue('--hours'))
    }});
    console.log(scheduleInfo)
    for(let i = 0; i < scheduleInfo.length; i++){
        if((scheduleInfo.filter((section) => {
            return scheduleInfo[i] !== section && (scheduleInfo[i]["day"] === section["day"] && scheduleInfo[i]["start"] >= section["start"] && scheduleInfo[i]["start"] <= section["start"] + section["hours"])}).length) > 0){
            console.log("Conflict")
            return {conflict: true, message:"Two or more of your courses conflict with each other"}
        }
    }
    return {conflict: false};
}

function disableButtonOnConflict(){
    let conflict = checkForConclicts()
    let message = ""
    if(conflict["conflict"]){
        document.querySelector(".submit-enrollment").classList.add("disabled")
        message = conflict["message"]
    }
    else{
        document.querySelector(".submit-enrollment").classList.remove("disabled")
    }
    document.querySelector(".conflict-message").innerHTML = message
}

function addExpandClicks(){
    for(let expand of document.querySelectorAll(".expand-course")){
        expand.addEventListener("click", () => {
            expand.parentElement.parentElement.querySelector(".section-info-div").classList.toggle("hidden")
            expand.classList.toggle("collapse")
        })
    }
}



document.querySelector(".submit-enrollment").addEventListener("click", submitEnrollment)

