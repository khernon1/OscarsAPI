# -*- coding: utf-8 -*-
import unittest
from main.main import OscarsAPI
import json
import re
import pdb

class TestOscarsAPI(unittest.TestCase):

  def setUp(self):
    self.test_films = []
    self.test_films = [
      {'budget': u'$10 million', 'name': u'Movie1'},
      {'budget': u'$9-11 million', 'name': u'Movie2'},
      {'budget': u'US$10 million', 'name': u'Movie3'},
      {'budget': u'$10,000,000', 'name': u'Movie4'},
      {'budget': u'£10 million', 'name': u'Movie5'},
      {'budget': u'€10 million', 'name': u'Movie6'}
    ]

  def test_budget_formatter(self):    
    run_tests = OscarsAPI()
    json_films = json.dumps(self.test_films)
    json_films = json.loads(json_films)
    # pdb.set_trace()
    for film in json_films:
      usd = re.findall(r'\$', film['budget'])

      run_tests.format_budget_number(film)
      
      if usd:
        self.assertEqual(int(film['budget']), 10000000)
      else:
        self.assertEqual(int(film['budget']), 12300000)

if __name__ == '__main__':
    unittest.main()

