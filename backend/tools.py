import requests


def get_github_api():
    """Get basic information from GitHub API."""
    url = "https://api.github.com"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()


def get_users():
    """Get users from JSONPlaceholder API."""
    url = "https://jsonplaceholder.typicode.com/users"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()

from langchain_core.tools import tool


@tool
def github_info():
    """Get basic information from the GitHub REST API."""
    return get_github_api()


@tool
def users_info():
    """Get sample users from a REST API."""
    return get_users()