### Archivo `test_app.py`

```python
import unittest
from app import app

class CodacyAppTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_codacy_insights(self):
        response = self.app.get('/codacy/github/remote_org_name')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()