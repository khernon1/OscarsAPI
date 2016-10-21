# -*- coding: utf-8 -*-
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
    total_budgets = 0
    film_count = 0
    for films in films_per_year:
      # removes footnotes and whitespace
      cleaned_year = re.sub("[\(\[].*?[\)\]]", '', films.values()[1]).strip()
    

      for film in films.values()[0]:
        if film['Winner'] == True:
          # removes footnotes and whitespace
          cleaned_title = re.sub("[\(\[].*?[\)\]]", '', film['Film']).strip()
          added_film = {"name": cleaned_title, "detail_url": film['Detail URL'], "year": cleaned_year}
          self.winning_films.append(added_film)
          
          self.add_budget_to_winning_films(added_film)
          self.format_budget_number(added_film)
          self.print_winning_films(added_film)
          
          if added_film['budget'] != 0:
            total_budgets += added_film['budget']
            film_count += 1
            average_budget = total_budgets/film_count
          
    print "Average - %d" % int(average_budget)
    
  def add_budget_to_winning_films(self, film):
    detail_url = film['detail_url']
    response = urlopen(detail_url)
    film_detail = json.load(response)  

    # some films don't have budget data
    if 'Budget' in film_detail:
      film['budget'] = film_detail['Budget']
      film['budget'] = re.sub("[\(\[].*?[\)\]]", '', film['budget']).strip()
    else:
      film['budget'] = '$0'

  def format_budget_number(self, film):
    # the code directly below the case number comments 
    # deals with the individual edge cases
    budget_range = re.findall(r'\-', film['budget'])
    two_budgets = re.findall(r'\or', film['budget'])

    if two_budgets:
      self.two_budgets_given(film)
    # case1 = if a range is given ie "$10 - $12 million"
    if budget_range:
      self.budget_given_as_range(film)


    # case2 = majority are in USD format ie "$10 million" 
    # or "$10.2 million" (budget variable is converted to float)
    budget_number = re.findall(r'[\d.]*\d+', film['budget'])
    budget = float(''.join(budget_number))
    million = re.findall(r'\million', film['budget'])
    usd = re.findall(r'\$', film['budget'])

    if not usd:
      self.budget_not_in_usd(film, budget)
      budget_number = re.findall(r'[\d.]*\d+', film['budget'])
      budget = float(''.join(budget_number))

    if million:            
      budget *= 1000000
    
    # case3 = actual value is given no change is needed ie "$1,430,000"
    # otherwise if there was a change to the budget above it will update here
    film['budget'] = budget


  def two_budgets_given(self, film):
    split_budgets = film['budget'].split(' or')
    film['budget'] = split_budgets[0]
      
  def budget_given_as_range(self, film):
    budget_number = re.findall(r'[\d.]*\d+', film['budget'])
    budget1 = float(''.join(budget_number[0]))
    budget2 = float(''.join(budget_number[1]))
    average_budget_range = (budget1 + budget2)/2
    film['budget'] = re.sub(r'[\d.-]*\d+', str(average_budget_range), film['budget'])
      
  def budget_not_in_usd(self, film, budget):
    currency = film['budget'][0].encode('utf-8')
    # add dict to search through and get rate
    if currency == "£":
      converted_budget = float(budget * 1.33)
      film['budget'] = re.sub(r'\d.+', str(converted_budget), film['budget'])

  def print_winning_films(self, film):    
    print film['name'] + ' - ' + film['year'] + ' - {:,d}'.format(int(round(film['budget'],0)))
    


  def run_all(self):
    self.populate_winning_films()


go = OscarsAPI()
go.run_all()