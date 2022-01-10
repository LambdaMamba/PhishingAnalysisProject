# Phishing Analysis Project
Project to analyze active days and RTT in Phishing Websites using WHOIS and PING.

Put domains you want to analyze in a .txt file, similar to the one shown in /sample_domains_list.

I collected the phishing domains from the [Phishing.Database](https://github.com/mitchellkrogza/Phishing.Database), and the legitimate sites from the [Whitelist in Ultimate-Hosts-Blacklist](https://github.com/Ultimate-Hosts-Blacklist/whitelist/blob/master/domains.list).

I also wanted to analyze Steam and gaming phishing/scam sites, so I got the Gaming Phishing sites from [DevSpen's Scam-Links](https://github.com/DevSpen/scam-links) and [Wishihab's Steamscamsite](https://github.com/wishihab/steamscamsite). I got the legitimate Gaming Trading sites from [CSGO whitelist](https://www.reddit.com/r/GlobalOffensiveTrade/wiki/whitelist/), [Gamezod](https://gamezod.com/buy-csgo-skins/), [CSGO meister](https://csgomeister.com/csgo-trading-sites/), and [TF2 Trading Sites](https://guide.tf/tf2-trading-sites).


## WHOIS

Redirect output of whois.py to outwhois.txt
````
whois.py > outwhois.txt
````
To get the Creation date of the domain
````
cat outwhois.txt | grep "Creat"
````

To get the Expiration date of the domain
````
cat outwhois.txt | grep "Expir"
````
One problem with WHOIS is the data format is not consistent. Some use "Created on" and "Expires on", while others use "Creation Date" and "Expiration date" (there could be other variations as well). Some are in DD-MM-YY format, while others are in DD/MM/YY format. Some include time, while others do not. Before this data can be used, some processing is required to isolate the DD/MM/YY, then the difference between the Creation date and Expiration date can be calculated to be put into the .csv. 

The processed WHOIS data looks like the one in /whois/legit.csv and /whois/phish.csv, which can be used for whois_analysis.py.


## PING

Redirect output of ping.py to outping.txt
````
ping.py > outping.txt
````

To get the successful pings
````
cat outping.txt | grep "is active" | cut -d "'" -f 2
````
The RTT statistics are in the following format:
rtt min/avg/max/mdev = 10.537/15.892/22.083/4.751 ms

The following command is used to get the average RTT (Only the PINGs that were successful will have the RTT statistics) 
````
 cat outping.txt | grep "rtt" | cut -d "/" -f 5 | cut -d "/" -f 6
````

The collected data looks like the one in /ping/pinglegit.csv and /ping/whois.csv (IP addresses are removed for privacy issues).

To get the location of the IP addresses in ping_analysis.py, IP2Location Database is used, and can be obtained from [here](https://lite.ip2location.com/database/db5-ip-country-region-city-latitude-longitude).

The outputted .csv file that includes the distance and Country should look like the ones in /ping/legitdistcountry.csv and /ping/phishdistcountry.csv (IP addresses are removed for privacy issues).

