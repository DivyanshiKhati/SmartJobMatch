
import streamlit as st
from matcher import load_jobs, match_jobs

# Page configuration
st.set_page_config(
    page_title="SmartJobMatch",
    page_icon="💼",
    layout="centered"
)

st.title("💼 SmartJobMatch")
st.write("Find jobs that match your skills and preferences.")

st.divider()

# Candidate details
st.subheader("Your Profile")

skills_input = st.text_input(
    "Enter your skills (comma separated)",
    placeholder="Python, SQL, Java"
)

location = st.selectbox(
    "Preferred Location",
    ["Remote", "Noida", "Bangalore", "Lucknow", "Gurugram"]
)

experience = st.number_input(
    "Years of Experience",
    min_value=0,
    max_value=10,
    value=0
)

# Find jobs
if st.button("Find Matching Jobs"):

    if not skills_input.strip():
        st.warning("Please enter at least one skill.")

    else:
        candidate = {
            "skills": [
                skill.strip().lower()
                for skill in skills_input.split(",")
            ],
            "preferred_location": location,
            "experience": experience
        }

        jobs = load_jobs()

        # Make job skills lowercase for comparison
        for job in jobs:
            job["skills"] = [
                skill.lower() for skill in job["skills"]
            ]

        recommendations = match_jobs(candidate, jobs)

        st.divider()
        st.subheader("Your Job Recommendations")

        if not recommendations:
            st.info("No matching jobs found.")

        for job in recommendations:
            with st.container(border=True):
                st.markdown(f"### {job['title']}")
                st.write("Company:", job["company"])
                st.write("Location:", job["location"])
                st.write(
    "Salary:",
    job["salary"],
    job["currency"],
    "/",
    job["salary_period"]
)
                st.write("Job Type:", job["type"])

                st.link_button(
    "Apply for this Job",
    job["application_link"]
)
                st.metric("Match Score", f"{job['score']}%")

                st.write("**Matched Skills:**",
                         ", ".join(job["matched_skills"]) or "None")

                st.write("**Skills to Learn:**",
                         ", ".join(job["missing_skills"]) or "None")
