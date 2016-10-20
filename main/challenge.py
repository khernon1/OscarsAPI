from urllib2 import urlopen
import json
import re
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
        # removes footnotes and whitespace
        cleaned_year = re.sub("[\(\[].*?[\)\]]", '', films.values()[1]).strip()
      
      for film in films.values()[0]:
        if film['Winner'] == True:
          # removes footnotes and whitespace
          cleaned_title = re.sub("[\(\[].*?[\)\]]", '', film['Film']).strip()
          self.winning_films.append({"name": cleaned_title, "detail_url": film['Detail URL'], "year": cleaned_year})

    
  def add_budget_to_winning_films(self):
    for film in self.winning_films:
      detail_url = film['detail_url']
      response = urlopen(detail_url)
      film_detail = json.load(response)  

      # some films don't have budget data
      if 'Budget' in film_detail:
        film['budget'] = film_detail['Budget']
        film['budget'] = re.sub("[\(\[].*?[\)\]]", '', film['budget']).strip()
      else:
        film['budget'] = '0'

      # add formulas to fix the budget
      usd = re.findall(r'\$', film['budget'])
      pdb.set_trace()


  def print_winning_films(self):
    for film in self.winning_films:
      print film['name'] + ' - ' + film['year'] + ' - ' + film['budget']



  def run_all(self):
    self.populate_winning_films()
    self.add_budget_to_winning_films()
    self.print_winning_films()


go = OscarsAPI()
go.run_all()