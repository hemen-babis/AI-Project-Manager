import unittest
from app import app

class ProjectManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_project_creation(self):
        response = self.app.post('/start_project', json={
            'goal': 'Launch new product website',
            'deadline': '2024-12-01',
            'team_members': 5,
            'milestones': ['Design', 'Development', 'Testing', 'Launch']
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Project Created', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
