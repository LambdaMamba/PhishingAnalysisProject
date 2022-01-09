#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df_phish = pd.read_csv("phish.csv")
df_legit = pd.read_csv("legit.csv")

phish_days = []
legit_days = []

phish_days = df_phish.TotalDays
legit_days = df_legit.TotalDays

print(df_phish)
print(df_legit)


# In[2]:


plt.ylabel("Frequency")
plt.xlabel('Total Days')
plt.suptitle('Days active for phishing sites')

plt.hist(phish_days, bins = 25, color='red', alpha=0.3, label="Phishing sites")
plt.legend()
plt.show()

plt.ylabel("Frequency")
plt.xlabel('Total Days')
plt.suptitle('Days active for legitimate sites')

plt.hist(legit_days, bins = 25, color='green', alpha=0.3,label="Legitimate sites")
plt.legend()
plt.show()


# In[3]:


plt.figure(figsize=(20, 10))
plt.xticks(np.arange(0, 20000, 500))

plt.ylabel("Frequency")
plt.xlabel('Total Days')
plt.suptitle('Days active')


plt.hist(phish_days, bins = 50, color='red', alpha=0.3 ,label="Phishing sites")
plt.hist(legit_days, bins = 100, color='green', alpha=0.3,label="Legitimate sites")

plt.legend()
plt.show()

