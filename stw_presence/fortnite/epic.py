import httpx

WORLD_INFO_URL = (
    "https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/world/info"
)


def get_world_info(access_token: str) -> dict:
    response = httpx.get(
        WORLD_INFO_URL,
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    response.raise_for_status()

    return response.json()


def exchange_authorization_code(
    authorization_code: str, client_id: str, client_secret: str
) -> str:
    response = httpx.post(
        "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
        auth=httpx.BasicAuth(client_id, client_secret),
        data={
            "grant_type": "authorization_code",
            "code": authorization_code,
        },
    )
    response.raise_for_status()

    auth_data = response.json()
    access_token = auth_data["access_token"]

    return access_token
