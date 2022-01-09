# PhishingAnalysisProject
Project to analyze patterns in Phishing Websites

Put domains you want to analyze in a .txt file, similar to the one shown in /sample_domains_list
I collected the phishing domains from the [Phishing.Database](https://github.com/mitchellkrogza/Phishing.Database), and the legitimate sites from the [whitelist in Ultimate-Hosts-Blacklist](https://github.com/Ultimate-Hosts-Blacklist/whitelist/blob/master/domains.list).


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
One problem with WHOIS is the data format is not consistent. 

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

To get the average RTT
````
 cat outping.txt | grep "rtt" | cut -d "/" -f 5 | cut -d "/" -f 6
````

The collected data looks like the one in /ping/pinglegit.csv and /ping/whois.csv (IP addresses are removed for privacy issues).

To get the location of the IP addresses in ping_analysis.py, IP2Location Database is used, and can be obtained from [here](https://lite.ip2location.com/database/db5-ip-country-region-city-latitude-longitude).

The outputted .csv file that includes the distance and Country should look like the ones in /ping/legitdistcountry.csv and /ping/phishdistcountry.csv (IP addresses are removed for privacy issues).

