UTM2DD - Mikhail Garcia Echavarri - Feb 24 2021

utm2dd is a python module that allows users to quickly transform UTM coordinates into Decimal Degree latitude and longitude coordinates. 
Its builds off the utm package to_latlon() function. utm2dd takes UTMs written as "10M 551884.29mE 5278575.64mN" and parses them to work
with the utm package's input parameters. utm2dd can take a single string, a list, or a pandas column and out puts accordingly

Requires the following packages:

pandas
utm