import unittest
from main.main import OscarsAPI
import re
import pdb

class TestOscarsAPI(unittest.TestCase):

  def setUp(self):
    self.test_films = []
    add_film = {'budget': u'US$ 2 million', 'name': u'Movie1'}
    # add_film = {'name': u'Movie1', 'budget': u'$1 million'}
    self.test_films.append(add_film) 
    self.test_budget_formatter()

  def test_budget_formatter(self):    
    run_tests = OscarsAPI()
    for film in self.test_films:
      # pdb.set_trace()      
      run_tests.format_budget_number(film)

      budget = film['budget']
      # int(budget) == 5000000
      # self.assertEqual(int(budget), 5000000)

# go = TestOscarsAPI()

if __name__ == '__main__':
    unittest.main()

