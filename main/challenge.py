from urllib2 import urlopen
import json
import pdb

class OscarsAPI:

  def __init__(self):
    url = 'http://oscars.yipitdata.com/'
    response = urlopen(url)
    self.all_films = json.load(response)
    self.winning_films = []

  def populate_winning_films(self):
    films_per_year = self.all_films['results']
    for films in films_per_year:
      for film in films.values()[0]:
        if film['Winner'] == True:
          self.winning_films.append({"name": film['Film'], "detail_url": film['Detail URL'], "year": films.values()[1]})
    
  def add_budget_to_winning_films(self):
    for film in self.winning_films:
      detail_url = film['detail_url']
      response = urlopen(detail_url)
      film_detail = json.load(response)  
      # if film_detail['Budget']:
      film['budget'] = film_detail['Budget']
      # else:
        # film['budget'] = 0
      pdb.set_trace()





  def print_winning_films(self):
    for film in self.winning_films:
      pdb.set_trace()
      print film['name'] + ' - ' + film['year'] + ' - ' + film['budget']




  def run_all(self):
    self.populate_winning_films()
    self.add_budget_to_winning_films()
    self.print_winning_films()


go = OscarsAPI()
go.run_all()