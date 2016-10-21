# -*- coding: utf-8 -*-
from urllib2 import urlopen
import json
import re
import pdb

class OscarsAPI():

  def __init__(self):
    # get request to api to get all of the films to start
    url = 'http://oscars.yipitdata.com/'
    response = urlopen(url)
    self.all_films = json.load(response)
    self.winning_films = []
    self.total_budgets = 0
    self.film_count = 0
    self.currency_list = {"£": 1.23}

  def populate_winning_films(self):
    films_per_year = self.all_films['results']
    # iterate through each year's list of films
    for films in films_per_year:
      # removes footnotes and whitespace
      cleaned_year = re.sub("[\(\[].*?[\)\]]", '', films.values()[1]).strip()
    
      # iterate through for the winner's title, detail_url, and year
      for film in films.values()[0]:
        if film['Winner'] == True:
          # removes footnotes and whitespace
          cleaned_title = re.sub("[\(\[].*?[\)\]]", '', film['Film']).strip()
          added_film = {"name": cleaned_title, "detail_url": film['Detail URL'], "year": cleaned_year}
          # add each film to the winning_films list
          self.winning_films.append(added_film)

          # these four are run here so as to limit the iterations required
          self.add_budget_to_winning_films(added_film)
          self.format_budget_number(added_film)
          self.print_winning_films(added_film)
          
          if added_film['budget'] != 0:
            self.average_budget(added_film)

    print "Average - %d" % int(self.total_budgets/self.film_count)
  

  def add_budget_to_winning_films(self, film):
    # requires another api get request to detail url
    detail_url = film['detail_url']
    response = urlopen(detail_url)
    film_detail = json.load(response)  

    # some films don't have budget data
    if 'Budget' in film_detail:
      film['budget'] = film_detail['Budget']
      # removes footnotes and whitespace
      film['budget'] = re.sub("[\(\[].*?[\)\]]", '', film['budget']).strip()
    else:
      film['budget'] = '0'


  def format_budget_number(self, film):
    # pdb.set_trace()
    # the code directly below the case number comments 
    # explains the individual edge cases
    
    # case1 = if budget is given twice ie "$10m or £500,000"
    # the first one is taken
    two_budgets = re.findall(r'\or', film['budget'])
    if two_budgets:
      self.two_budgets_given(film)

    # case2 = if a range is given ie "$10 - $12 million"
    # the average of the two is calculated
    budget_range = re.findall(r'\-|\–', film['budget'].encode('utf-8'))
    if budget_range:
      self.budget_given_as_range(film)

    # case3 = majority are in USD format ie "$10 million" or "$10.2 million"
    # grabs only the integers and periods from the string for manipulation
    budget_number = re.findall(r'[\d.]*\d+', film['budget'])    
    budget = float(''.join(budget_number))
    million = re.findall(r'\illion', film['budget'])
    usd = re.findall(r'\$', film['budget'])

    # case4 = if another currency symbol is given
    if not usd and budget != 0:
      self.budget_not_in_usd(film, budget)
      # have to reset these variables after the conversion
      budget_number = re.findall(r'[\d.]*\d+', film['budget'])
      budget = float(''.join(budget_number))
    
    # case5 = if budget is formatted as string ie "10 million" in any currency
    if million:            
      budget *= 1000000
    
    # case6 = actual value is given no change is needed ie "$1,430,000"
    # otherwise if there was any change to the budget above it will update here
    film['budget'] = budget


  def two_budgets_given(self, film):
    split_budgets = film['budget'].split(' or')
    film['budget'] = split_budgets[0]

      
  def budget_given_as_range(self, film):
    # budget range is broken into a list    
    budget_number = re.findall(r'[\d.]*\d+', film['budget'])
    budget1 = float(''.join(budget_number[0]))
    budget2 = float(''.join(budget_number[1]))
    average_budget_range = (budget1 + budget2)/2
    film['budget'] = re.sub(r'[\d.–-]*\d+', str(average_budget_range), film['budget'].encode('utf-8'))

      
  def budget_not_in_usd(self, film, budget):
    currency = film['budget'][0].encode('utf-8')
    if self.currency_list[currency]:
      converted_budget = float(budget * self.currency_list[currency])
      film['budget'] = re.sub(r'\d.+', str(converted_budget), film['budget'])


  def print_winning_films(self, film):    
    print film['name'] + ' - ' + film['year'] + ' - {:,d}'.format(int(round(film['budget'],0)))
  

  def average_budget(self, film):
    self.total_budgets += film['budget']
    self.film_count += 1


  def run_all(self):
    self.populate_winning_films()

if __name__ == "__main__":
  get_films = OscarsAPI()
  get_films.run_all()