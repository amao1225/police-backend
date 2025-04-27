# tests/test_task.py
def test_assign_task(app, client):
    token = get_auth_token(client)  # 管理员令牌
    response = client.post(
        '/api/tasks',
        json={
            "title": "现场勘查",
            "content": "前往XX地点勘查",
            "assignee_id": 1  # 假设存在用户ID为1的警员
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json["title"] == "现场勘查"