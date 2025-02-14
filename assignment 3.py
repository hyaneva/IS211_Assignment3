#!/usr/bin/env python
# coding: utf-8

# In[413]:


import argparse
import urllib.request
import csv
import re
from datetime import datetime


# In[414]:


def downloadData(url):
    
    #Opens the URL and read the file content into a string
    with urllib.request.urlopen(url) as response:
        the_file = response.read().decode('utf-8')     
    return the_file   


# In[415]:


def processData(data1):
    
    csv_dict = {}
    split_by_line = csv.reader(data1.strip().splitlines())        #Handles commas inside quotes
    
    for linenum, line in enumerate(split_by_line, start=1):      #Loops through each line starting from 1
        if len(line) == 5:                                    #Ensures the line has exactly 5 fields
            file_path, access_time, browser, request_status, request_size = line
         
                #Stores data in the dictionary with line number as the key
            csv_dict[linenum] = {
                    "file_path": file_path,
                    "access_date": access_time,
                    "browser": browser,
                    "request_status": request_status,
                    "request_size": request_size
                }
            
        
    return csv_dict


# In[ ]:





# In[416]:


def imageHits(data):
    
    how_many_images = 0
    total_hits = 0
    
    #Loops through each entry in the data to check if the file path is an image
    
    for key in data:
        
        total_hits += 1
        if re.search(r"\.(jpg|png|gif)$", data[key]["file_path"], re.IGNORECASE):
            how_many_images += 1
        
    #Calculate the percentage of image hits from total hits   
    percentage = (how_many_images / total_hits) * 100 if total_hits > 0 else 0      
    
    return(f"\nThere were exactly {how_many_images} image hits out of {total_hits} total hits. Image requests account for {percentage}% of all requests. \n")


# In[ ]:





# In[ ]:





# In[417]:


def popularBrowser(data2):
    
    
    how_many_browsers = {"Firefox": 0,
                    "Safari": 0,
                    "Chrome": 0,
                    "Internet Explorer": 0
                }
    
    #Loops through each entry and categorize by browser type
    for key2 in data2:
        
        if re.search(r"Firefox/", data2[key2]["browser"], re.IGNORECASE):
            how_many_browsers["Firefox"] += 1
        
        elif re.search(r"Chrome/", data2[key2]["browser"], re.IGNORECASE):
            how_many_browsers["Chrome"] += 1
        
        elif re.search(r"MSIE|Trident", data2[key2]["browser"], re.IGNORECASE):
            how_many_browsers["Internet Explorer"] += 1
        
        #Excludes Chrome because Safari can aslo be present in chrome user agent, avoids false positives
        
        elif re.search(r"Safari/", data2[key2]["browser"], re.IGNORECASE) and not re.search(r"Chrome", data2[key2]["browser"], re.IGNORECASE):
            how_many_browsers["Safari"] += 1
    
    #Finds browser with highest count of hits
    most_popular_browser = max(how_many_browsers, key=how_many_browsers.get)     #Gets highest value in dict       
    return f"The most popular browser is {most_popular_browser} with {how_many_browsers[most_popular_browser]} hits. \n"


# In[ ]:





# In[ ]:





# In[421]:


def hourCount(data3):
    hour_dict = {}
    
    for hour in range(0, 24):                    #Populates dictionary with every hour
        hour_dict[f"Hour {hour:02}"] = 0
    
    for key3 in data3:
        
        access_time = data3[key3]["access_date"]
    
        try:
            #Loop s through each entry and increment the count for the hour of the access
            hours = datetime.strptime(access_time, "%Y-%m-%d %H:%M:%S").hour
            hour_dict[f"Hour {hours:02}"] += 1                   
        
        except ValueError:
            continue                              #Skips dates with wrong format

    
    #Sorts from highest value to lowest
    for hours, count in sorted(hour_dict.items(), key=lambda x: x[1], reverse=True):     
        print(f"{hours} has {count} hits")



# In[422]:


def main(url):
    
    print(f"Running main with URL = {url} ...")
    
    #Attemps to download data
    try:
        csv_data = downloadData(url)   #Downloads data with whichever url was put in
    except Exception as e:
        print(f"Error downloading data: {e}")
        return
        
    processed_csv = processData(csv_data) 
    print(imageHits(processed_csv))  
    print(popularBrowser(processed_csv))
    print("The total number of hits that occurred in every hour of the day: ")
    hourCount(processed_csv)  


# In[423]:


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)


# In[ ]:





# In[ ]:




