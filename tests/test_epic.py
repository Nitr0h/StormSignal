import httpx

from stw_presence.fortnite.epic import exchange_authorization_code, get_world_info


def test_get_world_info(monkeypatch) -> None:
    expected_data = {
        "missions": [],
        "theaters": [],
        "missionAlerts": [],
    }

    def fake_get(url: str, headers: dict) -> httpx.Response:
        assert headers["Authorization"] == "Bearer test-token"

        return httpx.Response(
            200,
            json=expected_data,
            request=httpx.Request("GET", url),
        )

    monkeypatch.setattr(httpx, "get", fake_get)

    result = get_world_info("test-token")

    assert result == expected_data


def test_exchange_authorization_code(monkeypatch) -> None:
    expected_data = {
        "access_token": "fake-access-token",
        "expires_in": 7200,
    }

    def fake_post(
        url: str,
        auth: httpx.BasicAuth,
        data: dict,
    ) -> httpx.Response:
        assert data["grant_type"] == "authorization_code"
        assert data["code"] == "fake-auth-code"

        return httpx.Response(
            200,
            json=expected_data,
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(httpx, "post", fake_post)

    result = exchange_authorization_code(
        "fake-auth-code",
        "fake-client-id",
        "fake-client-secret",
    )

    assert result == "fake-access-token"
