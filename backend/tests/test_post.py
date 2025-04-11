# tests/test_post.py
def test_create_post(client, access_token):
    res = client.post(
        "/posts/",
        json={
            "title": "테스트 제목",
            "slug": "test-post",
            "content_md": "# 마크다운입니다",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "테스트 제목"
    assert data["slug"] == "test-post"
    assert data["content_html"].startswith("<h1>")


def test_get_post_by_slug(client, access_token):
    res = client.get("/posts/test-post")
    assert res.status_code == 200
    data = res.json()
    assert data["slug"] == "test-post"


def test_list_posts(client):
    res = client.get("/posts/?skip=0&limit=5")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_update_post(client, access_token):
    res = client.put(
        "/posts/test-post",
        json={
            "title": "수정된 제목",
            "slug": "updated-post",
            "content_md": "## 수정된 마크다운",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "수정된 제목"
    assert data["slug"] == "updated-post"
    assert "<h2>" in data["content_html"]


def test_delete_post(client, access_token):
    res = client.delete(
        "/posts/updated-post", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert res.status_code == 200
    assert res.json() == {"message": "삭제 완료"}

    # 삭제 후 조회 시 404
    res = client.get("/posts/updated-post")
    assert res.status_code == 404
