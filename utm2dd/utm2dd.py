"""Translate UTM strings into Decimal Degrees.

This module builds off the utm package to translate batches of UTM coordinates into latitude and longitude coordinates. 

This module works with UTM coordines formatted as follows: "10M 551884.29mE 5278575.64mN"
Digits can by of any length.

"""
import pandas as pd
import numpy as np
import utm

def string_transform(utm_string, easting_northing=True):
    """Parse UTM coordinate string into a Latitude/Longitude Tuple
    
    Parameters
    ----------
    utm_string : str
        UTM coordinate string. Format as: "10M 551884.29mE 5278575.64mN"
    easting_northing : bool, optional
        Default=True. Set to False if UTM is formated with mN before mE.

    Returns
    -------
    tuple
        (Latitude, Longitude)
    """
    utm_strip = utm_string.strip()#remove leading or trailing spaces
    split_UTM = utm_strip.split() #string split the UTM elements
    
    zone_num = float(split_UTM[0][:2]) #turn the zone number into a number
    zone_let = str(split_UTM[0][2:]) #turn the zone letter into its own letter
    
    if easting_northing == True: #formated by convention
        easting = float(split_UTM[1][:-2]) 
        northing = float(split_UTM[2][:-2])

    elif easting_northing == False: #flipped the easting and northing
        northing = float(split_UTM[1][:-2]) 
        easting = float(split_UTM[2][:-2])
    
    #turn into latlon
    latlong = utm.to_latlon(easting,northing,zone_num,zone_let)
    
    return(latlong)

def list_transform(utm_list, coordinate_pairs=True, easting_northing=True):
    """Parse a list of UTM coordinates into either a list of latitude,longitude tuples or a dict of latitude and longitude lists

    Parameters
    ----------
    utm_list : list
        a list of UTM coordinate strings. Strings formated as: "10M 551884.29mE 5278575.64mN"
    coordinate_pairs : bool, optional
        Default = True. Set to False to output a dict of latitude and longitude lists
    easting_northing : bool, optional
        Default=True. Set to False if UTM is formated with mN before mE.
    
    Returns
    -------
    If coordinate_pairs is set to True:

    list
        list of tuples: (Latitude, Longitude)
    
    If coordinate_pairs is set to False:

    dict
        dict of latitude and longitude lists: {"lat":lat, "lon":lon}

    """
    
    if coordinate_pairs == True:
        output = [string_transform(coordinate, easting_northing=easting_northing) for coordinate in utm_list]
    
    elif coordinate_pairs == False:
        lat = []
        lon = []
        
        for coordinate in utm_list:
            latlong = string_transform(coordinate, easting_northing=easting_northing)
            lat.append(latlong[0])
            lon.append(latlong[1])
        
        output = {"lat":lat, "lon":lon}
    return(output)

def column_transform(df, column_name, lat_column, lon_column, new_cols=False, easting_northing=True):
    """Parse a column of UTM coordinate strings from a Pandas Dataframe into Latitude Longitude columns.

    For populating Lat Lon columns in a dataframe or creating those columns from a UTM coordinate column

    Parameters
    ----------
    df : pandas dataframe

    column_name: str
        column name containing UTM coordinate strings
    
    lat_column: str
        name of column to populate with latitude coordinates
    
    lon_column: str
        name of column to populate with longitude coordinates

    new_cols: bool
        Default=False. Set to true to generate new columns for latitude and longitude coordinates rather than populate existing columns.

    easting_northing : bool, optional
        Default=True. Set to False if UTM is formated with mN before mE.

    Returns
    -------
    A pandas dataframe copy of the input dataframe with the transformations

    """
    # Initialize df copy
    df = df.copy()
    #For populating existing Lat Lon columns:
    if new_cols == False:
        for coordinate in df.loc[:,column_name].astype(str):
            if coordinate != 'nan': #In case the column has empty entries
                latlong = string_transform(coordinate, easting_northing=easting_northing)
                df.loc[df[column_name]==coordinate, lat_column] = latlong[0]
                df.loc[df[column_name]==coordinate, lon_column] = latlong[1]
                
    #For generating new La Lon columns:            
    elif new_cols == True:
        #Initialize strings that will become columns
        lat = []
        lon = []

        for coordinate in df.loc[:,column_name].astype(str):
            if coordinate != 'nan':
                latlong = string_transform(coordinate, easting_northing=easting_northing)
                lat.append(latlong[0])
                lon.append(latlong[1])
               
            else:
                lat.append(np.nan)
                lon.append(np.nan)
                
        #Create columns using user input column names
        df[lat_column] = lat
        df[lon_column] = lon
    #Print the count report    
    return(df)

