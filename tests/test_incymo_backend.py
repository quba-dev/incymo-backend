import urllib.parse as urlparse
from typing import Dict
from urllib.parse import urlencode

from fastapi.testclient import TestClient

from incymo_backend import __version__
from incymo_backend.main import app

client = TestClient(app)


def path_with_query_params(path: str, query_params: Dict) -> str:
    """Return URI for a endpoint with specified path and query parameters."""
    url_parts = list(urlparse.urlparse(path))
    url_parts[4] = urlencode(query_params)

    return urlparse.urlunparse(url_parts)


def test_version():
    assert __version__ == "0.1.0"


def test_liveness_probe():
    """LiveProbes for kubernetes always must give the 200 HTTP Status code."""

    url = app.url_path_for("liveness_probe")
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_get_experiment_is_working():
    """Check work and structure of response."""
    path_string = app.url_path_for("get_experiment")
    url = path_with_query_params(
        path=path_string,
        query_params={"api_key": 1, "user_id": 1},
    )
    response = client.get(url)
    assert response.status_code == 200
    rjson = response.json()

    assert rjson["assignment"]
    assert rjson["assignment"]["inputs"] == {"userid": "1"}
    assert rjson["debug_info"]


def test_idempotency_experiment_results():
    """Checking a invariability of experimental results"""
    path_string = app.url_path_for("get_experiment")

    result_map = {}
    for num_item in range(10):
        url = path_with_query_params(
            path=path_string,
            query_params={"api_key": 1, "user_id": num_item},
        )
        response = client.get(url)
        assert response.status_code == 200
        result_map[num_item] = response.json()

    # make 100 requests for getting the same results
    for attempt in range(10):
        for num_item in range(10):
            url = path_with_query_params(
                path=path_string,
                query_params={"api_key": 1, "user_id": num_item},
            )
            response = client.get(url)
            assert response.status_code == 200
            assert (
                result_map[num_item] == response.json()
            ), f"On attempt {attempt} occurred error."
