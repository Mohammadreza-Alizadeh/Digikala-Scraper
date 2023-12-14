# Digikala-Scraper
a simple script for scraping Digikala and storing data in a CSV 

## Project Summary
this is a web scraper built with selenium and BeautifulSoup4 in python  
it will search for a product that you gave to it as input and extrat all related products  
it then stores title and price of all of it in a csv file  

you have to provide following inputs  
- product name (this will use to search in Digikala.com)
- file name (a new unique name for your custom CSV file like 'ps5-data')

## Getting Started
To get this project up and running, you should start by having Python installed on your computer. It’s advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with pip install virtualenv.

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project
```
python -m venv env
```

That will create a new folder naemd env in your project directory. Next activate it with this command on mac/linux:
```
source env/bin/active
```
or if you use windows activate it with this command :
```
.\env\scripts\activate
```

Then install the project dependencies with:
```
pip install -r requirements.txt
```
