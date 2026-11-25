
import requests
import re


# --------------------------------
# 1. Extract skills from job details
# --------------------------------

def extract_skills(job):

    text = " ".join([
        str(job.get("title", "")),
        str(job.get("excerpt", "")),
        str(job.get("description", "")),
        " ".join(job.get("categories", []))
    ]).lower()

    skill_list = [
        "python", "java", "javascript", "typescript",
        "sql", "mysql", "postgresql", "mongodb",
        "html", "css", "react", "node.js",
        "machine learning", "deep learning",
        "pandas", "scikit-learn", "power bi",
        "excel", "c++", "c#", 
        "flutter", "dart", "firebase",
        "fastapi", "django", "flask",
        "spring boot", "docker", "kubernetes",
        "aws", "azure", "git", "linux",
        "rest api", "data analysis", "llm",
        "rag", "langchain", "swift", "objective-c"
    ]

    matched_skills = []

    for skill in skill_list:

        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"

        if re.search(pattern, text):
            matched_skills.append(skill)

    return matched_skills


# --------------------------------
# 2. Fetch jobs from Himalayas API
# --------------------------------

def load_jobs():

    url = "https://himalayas.app/jobs/api/search"

    params = {
        "country": "IN",
        "seniority": "Entry-level,Mid-level",
        "sort": "recent",
        "page": 1
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    api_jobs = data.get("jobs", [])

    jobs = []

    for job in api_jobs:

        restrictions = job.get("locationRestrictions") or []

        if not restrictions:
            location = "Remote (Worldwide)"

        else:
            location = "Remote (" + ", ".join(restrictions) + ")"

        # Extract experience from job description
        description = str(job.get("excerpt", ""))

        experience_match = re.search(
            r"(?:experience|esperienza)\s*:\s*(\d+)",
            description,
            re.IGNORECASE
        )

        required_experience = (
            int(experience_match.group(1))
            if experience_match else 0
        )

        jobs.append({

            "title": job.get("title", "Unknown"),

            "company": job.get("companyName", "Unknown"),

            "skills": extract_skills(job),

            "location": location,

            "experience": required_experience,

            "salary": job.get("minSalary"),

            "currency": job.get("currency", ""),

            "salary_period": job.get("salaryPeriod", "annual"),

            "type": job.get("employmentType", ""),

            "seniority": job.get("seniority", []),

            "application_link": job.get("applicationLink", "")

        })

    return jobs


# --------------------------------
# 3. Match candidate with jobs
# --------------------------------

def match_jobs(candidate, jobs):

    results = []

    candidate_skills = {
        skill.strip().lower()
        for skill in candidate["skills"]
    }

    for job in jobs:

        # Skip senior-level jobs for freshers
        seniority = [
            level.lower()
            for level in job.get("seniority", [])
        ]

        if candidate["experience"] == 0 and any(
            level in ["senior", "lead", "principal", "director"]
            for level in seniority
        ):
            continue

        # Filter by experience
        if candidate["experience"] < job["experience"]:
            continue

        # Find common skills
        job_skills = set(job["skills"])

        matched = candidate_skills.intersection(job_skills)

        missing = job_skills - candidate_skills

        # Calculate skill score
        if len(job_skills) > 0:

            skill_score = (
                len(matched) / len(job_skills)
            ) * 100

        else:
            skill_score = 0

        # Calculate location score
        preferred_location = candidate["preferred_location"].lower()

        # Himalayas country filter already ensures
        # these jobs are open to candidates in India.
        if (
            preferred_location == "remote"
            or preferred_location in [
                "lucknow", "noida", "bangalore", "gurugram"
            ]
        ):
            location_score = 100

        else:
            location_score = 0

        # Calculate final score
        final_score = (
            skill_score * 0.75 +
            location_score * 0.25
        )

        results.append({

            "title": job["title"],

            "company": job["company"],

            "location": job["location"],

            "salary": job["salary"],

            "currency": job["currency"],

            "salary_period": job["salary_period"],

            "type": job["type"],

            "score": round(final_score, 2),

            "matched_skills": list(matched),

            "missing_skills": list(missing),

            "application_link": job["application_link"]

        })

    # Rank jobs from highest to lowest score
    results.sort(
        key=lambda job: job["score"],
        reverse=True
    )

    return results


# --------------------------------
# 4. Test the API and matcher
# --------------------------------

if __name__ == "__main__":

    jobs = load_jobs()

    print("Total jobs fetched:", len(jobs))

    for job in jobs[:10]:

        print("\nTitle:", job["title"])
        print("Company:", job["company"])
        print("Skills:", job["skills"])
        print("Location:", job["location"])
        print("Experience:", job["experience"])
        print("Seniority:", job["seniority"])
