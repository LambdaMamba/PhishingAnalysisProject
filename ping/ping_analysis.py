#!/usr/bin/env python
# coding: utf-8

# In[1]:


from ip2geotools.databases.noncommercial import DbIpCity
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from geopy.distance import geodesic
import socket
import os
import IP2Location
import csv  
from requests import get

database = IP2Location.IP2Location()


#Get the IP2Location database from here : https://lite.ip2location.com/database/db5-ip-country-region-city-latitude-longitude


database.open(os.path.join("IP2LOCATION-LITE-DB5.BIN"))

my_ip = get('https://api.ipify.org').content.decode('utf8')

myloc = database.get_all(my_ip)

my_coord = (myloc.latitude, myloc.longitude)

# You can also use DbIPCity from IP2GeoTools to get location information for IP, but this seems to have a limit on how many requests you can make per day
# myloc = DbIpCity.get(my_ip, api_key='free')
# my_coord = (myloc.latitude, myloc.longitude)


print(my_coord)
print(myloc.country_long)


# In[2]:

#The .csv in this dataset has the IP addresses removed for privacy and license issues related to IP2Location
df_phish = pd.read_csv("pingphish.csv")
df_legit = pd.read_csv("pinglegit.csv")

phish_distance = []
legit_distance = []

phish_country = []
legit_country = []

phish_IP = df_phish.IP
legit_IP = df_legit.IP


# In[3]:

#Get country and coordinates for phishing sites, and calculate geographical distance
for ip in phish_IP:
    response = database.get_all(ip)
    phish_country.append(response.country_long)
    coord = (response.latitude, response.longitude)
    #Calculate the geographical distance in Kilometers from current location to the site's IP location using Geodesic
    dist = geodesic(my_coord, coord).kilometers
    phish_distance.append(dist)


# In[4]:


from collections import Counter

df_phish['Dist'] = phish_distance
df_phish['Country'] = phish_country

#Example of output .csv shown in /output_sample
df_phish.to_csv('phish_distance_country.csv')

print(df_phish)


#Order based on frequency so histogram is cleaner
counts = Counter(phish_country)
ordered_phish = sorted(phish_country, key=counts.get, reverse=True)

most_occur_phish= counts.most_common(1000)
  
print(most_occur_phish)

plt.figure(figsize=(20, 10))

plt.ylabel("Frequency")
plt.xlabel('Country')
plt.suptitle('Location of Phishing Sites')

plt.hist(ordered_phish, bins = 100, color =  'red')
plt.xticks(rotation=90)


plt.show()


# In[5]:

#Get country and coordinates for legitimate sites, and calculate geographical distance
for ip in legit_IP:
    response = database.get_all(ip)
    legit_country.append(response.country_long)
    coord = (response.latitude, response.longitude)
    dist = geodesic(my_coord, coord).kilometers
    legit_distance.append(dist)


# In[6]:


from collections import Counter

df_legit['Dist'] = legit_distance
df_legit['Country'] = legit_country

df_legit.to_csv('legit_distance_country.csv')


print(df_legit)

counts = Counter(legit_country)
ordered_legit = sorted(legit_country, key=counts.get, reverse=True)

most_occur_legit = counts.most_common(1000)
  
print(most_occur_legit)

plt.figure(figsize=(20, 10))

plt.ylabel("Frequency")
plt.xlabel('Country')
plt.suptitle('Location of Legitimate Sites')

plt.hist(ordered_legit, bins = 100, color =  'green')
plt.xticks(rotation=90)

plt.show()


# In[7]:


phish_RTT = df_phish.RTTavg
legit_RTT = df_legit.RTTavg


avgphish = np.average(phish_RTT)

print("Average RTT of phishing sites: ", avgphish)

stddevphish = np.std(phish_RTT)
print("Standard Deviation of RTT of phishing sites: ", stddevphish)


avglegit = np.average(legit_RTT)

print("Average RTT of legitimate sites: ", avglegit)

stddevlegit = np.std(legit_RTT)
print("Standard Deviation of RTT of legitimate sites: ", stddevlegit)


# In[8]:


plt.figure(figsize=(10, 10))

plt.ylabel("RTT [ms]")
plt.xlabel("Distance [km]")
plt.suptitle('Distance vs RTT')

plt.scatter(df_phish.Dist, df_phish.RTTavg, label="Phishing Sites",color='red', alpha=0.3)

plt.scatter(df_legit.Dist, df_legit.RTTavg, label="Legitimate Sites", color='green', alpha=0.3)
plt.legend()

plt.show


# In[9]:

#Use linear regression, fit using Numpy Polyfit to the first order (straight line)

y_phish = np.polyfit(df_phish.Dist, df_phish.RTTavg, 1)

p_phish = np.poly1d(y_phish)

y_legit = np.polyfit(df_legit.Dist, df_legit.RTTavg, 1)

p_legit = np.poly1d(y_legit)

print("Fitted line for phishing sites: ", p_phish)
print("Fitted line for legitimate sites: ", p_legit)

plt.figure(figsize=(10, 10))

plt.ylabel("RTT [ms]")
plt.xlabel("Distance [km]")
plt.suptitle('Distance vs RTT')

plt.plot(df_phish.Dist ,np.polyval(y_phish, df_phish.Dist),color='red',label='Phish fitted line')
plt.plot( df_legit.Dist ,np.polyval(y_legit, df_legit.Dist),color='green',label='Legit fitted line')


plt.scatter(df_phish.Dist, df_phish.RTTavg, label="Phishing Sites",color='red', alpha=0.3)

plt.scatter(df_legit.Dist, df_legit.RTTavg, label="Legitimate Sites", color='green', alpha=0.3)
plt.legend()
plt.show


# In[10]:


from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


print("MSE for phishing sites: ", mean_squared_error(df_phish.RTTavg, np.polyval(y_phish, df_phish.Dist)))
print("R2 score for phishing sites", r2_score(df_phish.RTTavg, np.polyval(y_phish, df_phish.Dist)))

print("MSE for legitimate sites: ", mean_squared_error(df_legit.RTTavg, np.polyval(y_legit, df_legit.Dist)))
print("R2 score for legitimate sites", r2_score(df_legit.RTTavg, np.polyval(y_legit, df_legit.Dist)))




