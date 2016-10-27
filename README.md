# OscarsAPI
___
### Goal:

Send requests to the API and calculate the average budget for all Oscar winning films.
___
### To run:

1. Clone the repo and cd into the directory
2. Activate the virtual environment `source env/bin/activate`
3. In the terminal, run `python main/main.py` and the results will print
4. To run the tests, run `python test.py`. There is only one test but it runs for all of the edge cases.

___

The average budget using my calculations is $17,240,234.

Cases where assumptions were needed:

1. If a range was given, the average of the two was calculated.
2. For foreign currencies, today's rate was used. Only GBP was given but more could be added to the dictionary.

Below is a quick demo:

![yipit](https://cloud.githubusercontent.com/assets/17169813/19592707/e7c05240-974a-11e6-9375-eddd20604b11.gif)

