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

    def test_swagger_json_served(self):
        """Testa se /swagger.json serve o spec do swagger"""
        response = self.client.get('/swagger.json')
        # swagger.json é um arquivo estático - deve retornar sucesso
        self.assertEqual(response.status_code, 200)
        try:
            data = response.get_json()
            # If file is JSON, we at least expect an 'openapi' or 'swagger' key
            self.assertTrue('openapi' in data or 'swagger' in data)
        except Exception:
            # If not parsable as JSON, ensure it's returned as text
            self.assertTrue(response.data and len(response.data) > 0)

    def test_misspelled_swagger_redirects(self):
        """Requests to the common misspelling '/swgger' should redirect to '/swagger/'"""
        response = self.client.get('/swgger', follow_redirects=False)
        # Expect a redirect to the correct swagger UI
        self.assertIn(response.status_code, (301, 302))
        location = response.headers.get('Location', '')
        # The Location header should point to the correct path
        self.assertTrue(location.endswith('/swagger/') or location.endswith('/swagger'))

if __name__ == '__main__':
    unittest.main()
