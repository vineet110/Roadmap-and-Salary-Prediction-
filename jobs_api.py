import requests
from bs4 import BeautifulSoup

def fetch_jobs(role="software engineer"):
    url = f"https://www.naukri.com/{role.replace(' ', '-')}-jobs"

    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []

    for job in soup.select(".title")[:5]:
        jobs.append(job.text.strip())

    return jobs