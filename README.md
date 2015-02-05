# American Time Use Analysis

## Description

Use the U.S. Department of Labor's data on Americans' time use for research and analysis.

## Objectives

### Learning Objectives

After completing this assignment, you should understand:

* How to use public data for analysis
* How to translate data from CSVs to relational databases
* How to publish your own data analysis as a notebook

### Performance Objectives

After completing this assignment, you should be able to:

* Use pandas to parse and analyze data
* Use matplotlib to chart data
* Clean data

## Details

### Deliverables

* A Git repo called atus-analysis containing at least:
  * `README.md` file explaining how to run your project
  * a `requirements.txt` file
  * an IPython notebook with your analysis
  * a suite of tests for your project

### Requirements  

* Passing unit tests
* No PEP8 or Pyflakes warnings or errors

## Normal Mode

The U.S. Bureau of Labor Statistics publishes yearly data about Americans' use
of their time: [American Time Use Survey](http://www.bls.gov/tus/home.htm#data).
This data is used to find out information like how many hours the average person
spends per day doing household activities. You can see
[the 2013 survey results](http://www.bls.gov/news.release/atus.nr0.htm)
for more examples. You should use these results to double-check your logic as well.

You will download the 2013 files and use these to do analysis. The questions you are trying to answer are up to you, but they
should at least:

* Compare different populations (people with children and people without, people
  of differing age groups, men and women, or other groupings)
* Answer macro-level questions and micro-level questions (for example, trends
  in the amount of leisure for the macro-level, trends in the types of things
  people do for leisure for the micro-level)

Your final analysis should be in the form of an IPython Notebook with both
narrative analysis and supporting charts. Your supporting code should be in
normal Python files.



## Additional Resources

* [How to use ATUS microdata files](http://www.bls.gov/tus/howto.htm)
* [ATUS Coding Lexicon - you will need this](http://www.bls.gov/tus/lexicons.htm)
