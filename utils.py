def analyze_profile(data):
    issues = []

    if data["projects"] < 3:
        issues.append("Low number of projects")

    if data["internships"] == 0:
        issues.append("No internship experience")

    if data["cgpa"] < 8:
        issues.append("CGPA below industry standard")

    if data["coding_score"] < 60:
        issues.append("Weak coding skills")

    return issues


def generate_roadmap(data):
    roadmap = []

    if "DSA" not in data["skills"]:
        roadmap.append("Week 1-2: Learn Arrays & Strings")
        roadmap.append("Week 3-4: Solve 50 LeetCode problems")

    if data["projects"] < 3:
        roadmap.append("Month 2: Build 2 production-level projects")

    if data["internships"] == 0:
        roadmap.append("Month 3: Apply for internships")

    if data["target_role"] == "ML Engineer":
        roadmap.append("Learn Deep Learning, NLP, and MLOps")

    elif data["target_role"] == "SDE":
        roadmap.append("Focus on System Design & Backend")

    return roadmap