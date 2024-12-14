from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

class UserAuthTests(APITestCase):
    def setUp(self):
        """테스트를 위한 초기 사용자 생성"""
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='testuser',
            blog_name='Test Blog',
            password='secure_password'
        )
        self.login_url = '/login/' # 로그인 엔드포인트
        self.register_url = '/register/' # 회원가입 엔드포인트
        self.refresh_url = '/token/refresh/' # 토큰 갱신 엔드포인트
    
    def test_user_registration(self):
        """회원가입 테스트"""
        data = {
            'username': 'testuser',
            'blog_name': 'Tester Blog',
            'password': 'testuser'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('blog_name', response.data)
        self.assertNotIn('password', response.data) # 비밀번호는 응답에 포함되지 않아야 함
    
    def test_user_login(self):
        """로그인 테스트"""
        data = {
            'username': 'testuser', # 'username'를 'username'으로 사용
            'password': 'secure_password'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data) # JWT access 토큰
        self.assertIn('refresh', response.data) # JWT refresh 토큰
        
    def test_protected_endpoint(self):
        """JWT 인증된 요청 테스트"""
        # 로그인해서 access_token 얻기
        login_data = {'username': 'testuser', 'password': 'secure_password'}
        login_response = self.client.post(self.login_url, login_data)
        refresh_token = login_response.data['refresh']
        
        # 토큰 갱신 요청
        refresh_data = {'refresh': refresh_token}
        refresh_response = self.client.post(self.refresh_url, refresh_data)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data) # 새로운 access_token 반환
        
        
        