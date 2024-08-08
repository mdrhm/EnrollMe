from queries import SELECT_FROM_WHERE
import json
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def get_section_ids(section):
    if type(section) == dict:
        return section.get('section_id')
    return section

def get_response(user_input):
    response = model.generate_content([user_input])
    return response.text


    return response
def generate_course(input, current_courses):
    courses = SELECT_FROM_WHERE("course_id, CONCAT(subject, ' ', course_level) AS course_code, name", "course")
    response = get_response("Based on the following list of courses,provide an explanation on which courses do you recommend based on the provided query if they are looking for a recommendation, otherwise answer the query along with an explanation. In your response, only use the course_code of the courses, not the course_id. In addition, whenever you make a reference to a course course_code, I want you to wrap the course_code and with a <span course_id = [course_id]><h4>[course_code]</h4></span>, where [course_id] would be the course_id of the course and don't mention the query or anything I have mentioned before in your response. If the course_id is in currently_taking_courses, you don't have to mention it. Query:" + str(input) + " Courses: " + str(courses) + " currently_taking_courses: " + str(current_courses))
    return response
