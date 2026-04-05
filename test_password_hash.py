# coding:utf-8
# author:ila
import bcrypt

def test_password_hashing():
    """测试密码哈希功能"""
    test_password = "test123456"

    # 测试密码哈希
    hashed_password = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print(f"原始密码: {test_password}")
    print(f"哈希密码: {hashed_password}")

    # 验证密码
    is_valid = bcrypt.checkpw(test_password.encode('utf-8'), hashed_password.encode('utf-8'))
    print(f"密码验证结果: {is_valid}")

    # 测试错误密码
    is_valid_wrong = bcrypt.checkpw("wrongpassword".encode('utf-8'), hashed_password.encode('utf-8'))
    print(f"错误密码验证结果: {is_valid_wrong}")

    assert is_valid == True
    assert is_valid_wrong == False
    print("密码哈希测试通过！")

def test_jwt_token():
    """测试JWT token功能"""
    import jwt
    import datetime

    # 生成JWT token
    payload = {
        'tablename': 'users',
        'params': {'username': 'testuser'},
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }

    # 测试密钥
    test_secret_key = "test_secret_key_for_jwt"
    token = jwt.encode(payload, test_secret_key, algorithm='HS256')
    print(f"生成的JWT token: {token}")

    # 解码token
    decoded = jwt.decode(token, test_secret_key, algorithms=['HS256'])
    print(f"解码后的token: {decoded}")

    assert decoded['tablename'] == 'users'
    assert decoded['params']['username'] == 'testuser'
    print("JWT token测试通过！")

if __name__ == "__main__":
    test_password_hashing()
    test_jwt_token()