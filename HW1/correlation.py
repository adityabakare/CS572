#import libraries
import csv
import pandas as pd
from scipy.stats import spearmanr
import statistics #import the statistics module

#read JSON files as DataFrames
result = pd.read_json("result.json")
google = pd.read_json("Google_Result2.json")

#create a list of query names
query_names = ["Query" + str(i) for i in range(1, len(result.columns) + 1)]

#create an empty list of rows
rows = []

#loop through the queries
for i in range(len(result.columns)):
    #get the query name
    query = query_names[i]
    
    #get the lists of URLs from both files
    result_urls = result[result.columns[i]].tolist()
    google_urls = google[result.columns[i]].tolist()
    
    #count the number of overlapping results
    overlap = len(set(result_urls) & set(google_urls))
    
    #calculate the percent overlap
    percent = overlap / len(result_urls) * 100
    
    #calculate the Spearman correlation and the p-value
    rho, p = spearmanr(result_urls, google_urls)
    
    #create a row with the query name and the results
    row = [query, overlap, percent, rho]
    
    #append the row to the list of rows
    rows.append(row)

#calculate the average of each column using the statistics.mean () function
avg_overlap = statistics.mean([row[1] for row in rows])
avg_percent = statistics.mean([row[2] for row in rows])
avg_rho = statistics.mean([row[3] for row in rows])

#create a row with the label "Averages" and the averages of the columns
avg_row = ["Averages", avg_overlap, avg_percent, avg_rho]

#append the row to the rows list
rows.append(avg_row)

#open a csv file in write mode
with open("results.csv", "w") as f:
    #create a csv writer object
    writer = csv.writer(f)
    
    #write the header row with the column names
    writer.writerow(["Queries", "Number of Overlapping Results", "Percent Overlap", "Spearman Coefficient"])
    
    #write the data rows with the csv writer object
    writer.writerows(rows)

#close the csv file
f.close()
