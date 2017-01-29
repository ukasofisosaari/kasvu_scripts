# kasvu_scripts
Scripts for making statistics graphs for scout district membership growth committee/group/something.


These are really specific for use in Kuksa, Finnish Scout organization membership registry that is online. Because it doesnt have a API,
I needed to use Selenium to fetch member data with limits. I didnt want to do this manually since it would have meant hundreds of fetches.

Selenium for Python and plotly are required and xlrd. All can be installed from pip.

Scripts:
* kuksa_fetch.py
  * Fetches data from kuksa, all members that joined during a month and year, with specifying their birth year and sex
  * Converts excel to csv

* kuksa_clean_columns.py:
  * Cleans out columns not specified from excel

* plot_bar.py:
  * Plot per month all scouts that have joined in barchart by sexes and agegroups
  * Does this district and city wide
