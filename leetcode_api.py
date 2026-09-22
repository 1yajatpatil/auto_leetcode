import random

import requests

GRAPHQL_URL = "https://leetcode.com/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
    "User-Agent": "Mozilla/5.0 (maintainstreak-bot/1.0; personal practice digest)",
}

LIST_QUERY = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: $filters
  ) {
    total: totalNum
    questions: data {
      difficulty
      frontendQuestionId: questionFrontendId
      title
      titleSlug
      paidOnly: isPaidOnly
    }
  }
}
"""

DETAIL_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    title
    titleSlug
    content
    difficulty
    exampleTestcases
    topicTags { name }
    hints
  }
}
"""


def _graphql(query, variables):
    resp = requests.post(
        GRAPHQL_URL, json={"query": query, "variables": variables}, headers=HEADERS, timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(f"LeetCode GraphQL error: {data['errors']}")
    return data["data"]


def fetch_problem_pool(difficulty, limit=300):
    variables = {"categorySlug": "", "skip": 0, "limit": limit, "filters": {"difficulty": difficulty}}
    data = _graphql(LIST_QUERY, variables)
    questions = data["problemsetQuestionList"]["questions"]
    return [q for q in questions if not q["paidOnly"]]


def fetch_problem_detail(title_slug):
    data = _graphql(DETAIL_QUERY, {"titleSlug": title_slug})
    return data["question"]


def pick_random_problems(count, easy_ratio, excluded_slugs):
    n_easy = round(count * easy_ratio)
    n_medium = count - n_easy

    easy_pool = [q for q in fetch_problem_pool("EASY") if q["titleSlug"] not in excluded_slugs]
    medium_pool = [q for q in fetch_problem_pool("MEDIUM") if q["titleSlug"] not in excluded_slugs]

    random.shuffle(easy_pool)
    random.shuffle(medium_pool)

    picked = easy_pool[:n_easy] + medium_pool[:n_medium]

    # If one pool ran short (e.g. nearing the end of the fresh-problem supply
    # after months of runs), backfill from whichever pool has leftovers.
    shortfall = count - len(picked)
    if shortfall > 0:
        leftovers = easy_pool[n_easy:] + medium_pool[n_medium:]
        random.shuffle(leftovers)
        picked += leftovers[:shortfall]

    random.shuffle(picked)
    return picked[:count]
