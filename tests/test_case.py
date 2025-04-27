# tests/test_case.py
def test_create_case(app, client):
    # 模拟登录获取令牌（需先实现登录测试辅助函数）
    token = get_auth_token(client)
    
    # 创建案件
    response = client.post(
        '/api/cases',
        json={
            "case_number": "20250426001",
            "location": "XX路123号"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json["location"] == "XX路123号"

