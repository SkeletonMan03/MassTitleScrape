# MassTitleScrape
This is for scraping titles from a list of IPs or domains.  

# What purpose does this serve?
* To scrape titles of your sites of course.  
* You could use this to grab titles of all your websites in your environment via their IP addresses or domain names.  
* If you run a lot of websites and can't remember what everything is, this could be an easy way to check.  
* It could be useful on a pentest to see what web services are running in an unfamiliar environment.  
* To make a point about how websites that use Clouflare can have their host IP addresses discovered, thereby rendering their protection pointless.  

# How to use:
0) `pip install -r requirements.txt`
1) `python3 main.py -c <list.txt> -o <output.txt> -t <threads>`

# Okay, but why?
As previously stated, it can be an easy way to keep track of all of your sites or part of a way to determine what is running in an environment for a number of reasons.  
Aside from that:  
I had this realization one night that *a lot* of sites that use Cloudflare don't block all but Cloudflare's IPs.  
Not only that, but it would be pretty easy to find the IP of a site that uses Cloudflare by just searching for website titles if you only know the site's provider or general location (or guess).  
It's best practice to block all but Cloudflare's IP addresses from accessing your website if you're using their services, and for good reason.  
Someone could just scan large subnets for ports 80 and/or 443 and use something like this (or Shodan/Censys) to find the actual IP address of the website if they're able to connect directly.  
If you're using Cloudflare, you should be using it to keep your host system hidden so it can't be attacked.  
Leaving it accessible to non-Cloudflare IPs obviously puts you at risk and defeats the purpose of trying to protect your site with Cloudflare as it can be easily bypassed.  
This is absolutely not the only way to find origin IPs of Cloudflare protected sites, but is an easily avoidable one.  

# Disclaimer
* This is a proof of concept to make the point that a lot of websites that use Cloudflare or other DDoS/attack protection services don't configure their websites properly.  
* Hopefully with something as simple as this existing, more admins will actually configure them properly.  
* I do not condone messing with anything you don't own.  
* Most hosts/ISPs also frown upon mass scanning, so even though I explained the idea, that doesn't mean you should do it.  
* This exists solely for educational purposes.  
* We're not responsible for anything anyone does with this.  

# But how would I even block all requests that aren't Cloudflare?
Actually, that's pretty easy, but is going to depend on your environment.  
If you just want to do it via UFW, here's an easy solution:  
[From here](https://www.stavros.io/posts/block-non-cloudflare-ips-with-ufw/), but slightly changed
```
curl -s https://www.cloudflare.com/ips-v4 -o /tmp/cloudflareips.txt
echo "" >> /tmp/cloudflareips.txt
ufw --force reset
ufw enable
ufw allow from 1.2.3.4 #Replace with any IP that NEEDS direct IP access, probably your's that is currently logged in
ufw allow ssh #I assume you'd still like to manage via ssh and not get kicked out when you reload
for ip in $(cat /tmp/cloudflareips.txt)
do
  ufw allow proto tcp from $ip comment 'Cloudflare'
done
ufw reject 80
ufw reject 443
ufw reload
ufw status numbered
```
Congrats, with that, you're now configured more properly and have to worry less about DDoS attacks, but should probably do some more work now making sure it's as secure as you can from other attacks.  

# Contributors
* [Lord SkeletonMan](https://github.com/SkeletonMan03)
* [CRAWNiiK](https://github.com/CRAWNiiK)
