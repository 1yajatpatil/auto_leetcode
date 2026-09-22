import random

import requests

# LeetCode's own API/GraphQL endpoint is unreachable from the cloud routine's
# sandboxed network (egress is blocked for leetcode.com entirely), so problem
# data comes from a community-maintained mirror hosted on GitHub instead --
# github.com/raw.githubusercontent.com is reachable from the sandbox since
# that's also where this repo itself is cloned from/pushed to.
DATASET_URL = "https://raw.githubusercontent.com/neenza/leetcode-problems/master/merged_problems.json"

_cache = None


def _load_all_problems():
    global _cache
    if _cache is None:
        resp = requests.get(DATASET_URL, timeout=90)
        resp.raise_for_status()
        _cache = resp.json()["questions"]
    return _cache


def pick_random_problems(count, easy_ratio, excluded_slugs):
    problems = _load_all_problems()

    def usable(p, difficulty):
        return (
            p.get("difficulty") == difficulty
            and p.get("problem_slug") not in excluded_slugs
            and p.get("description")
        )

    easy_pool = [p for p in problems if usable(p, "Easy")]
    medium_pool = [p for p in problems if usable(p, "Medium")]

    random.shuffle(easy_pool)
    random.shuffle(medium_pool)

    n_easy = round(count * easy_ratio)
    n_medium = count - n_easy

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
