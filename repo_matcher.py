import re


def normalize_text(s: str) -> str:
    return re.sub(r'[^a-z0-9]', ' ', s.lower()).strip()


def token_similarity(a: str, b: str) -> float:
    a_tokens = set(normalize_text(a).split())
    b_tokens = set(normalize_text(b).split())

    if not a_tokens or not b_tokens:
        return 0.0

    return len(a_tokens & b_tokens) / len(a_tokens | b_tokens)


def match_projects_with_repos(projects, repo_urls, threshold=0.4):


    for project in projects:
        best = {"url": "", "score": 0.0}

        for url in repo_urls:
            repo_name = url.rstrip("/").split("/")[-1]
            score = token_similarity(project["name"], repo_name)

            if score > best["score"]:
                best = {"url": url, "score": score}

        if best["score"] >= threshold:
            project["github_url"] = best["url"]
            project["github_match_confidence"] = round(best["score"], 2)
        else:
            project["github_url"] = ""
            project["github_match_confidence"] = 0.0

    return projects
