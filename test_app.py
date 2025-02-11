import unittest
from app import app

class CodacyAppTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_codacy_organization(self):
        response = self.app.get('/codacy/organizations/gh/josebaezae')
        self.assertEqual(response.status_code, 200)
    
    def test_codacy_repositories(self):
        response = self.app.get('/codacy/repositories/gh/josebaezae')
        self.assertEqual(response.status_code, 200)

    def test_codacy_files(self):
        response = self.app.get('/codacy/files/gh/josebaezae/test')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
