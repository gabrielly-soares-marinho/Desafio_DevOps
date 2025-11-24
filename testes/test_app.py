import unittest
from app import app
import json
import werkzeug

# Workaround para compatibilidade com Werkzeug 3.x
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = getattr(werkzeug, 'version', '3.0.0')

class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_login_gera_token(self):
        """Testa se a rota /login retorna um token de acesso válido"""
        response = self.client.post('/login')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('access_token', data)
        self.assertIsInstance(data['access_token'], str)
        self.assertGreater(len(data['access_token']), 0)

    def test_rota_protegida_com_token(self):
        """Testa se a rota /protected funciona com token válido"""
        # Primeiro obtém o token
        login_response = self.client.post('/login')
        self.assertEqual(login_response.status_code, 200)
        token = login_response.get_json()['access_token']
        
        # Usa o token para acessar a rota protegida
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Protected route')

    def test_rota_protegida_sem_token(self):
        """Testa se a rota /protected retorna erro sem token"""
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
