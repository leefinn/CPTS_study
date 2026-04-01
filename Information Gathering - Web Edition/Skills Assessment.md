
---

To complete the skills assessment, answer the questions below. You will need to apply a variety of skills learned in this module, including:

- Using `whois`
- Analysing `robots.txt`
- Performing subdomain bruteforcing
- Crawling and analysing results

Demonstrate your proficiency by effectively utilizing these techniques. Remember to add subdomains to your `hosts` file as you discover them.

---

# Skills Assessment

## Question 1

### "What is the IANA ID of the registrar of the inlanefreight.com domain?"

Students need to perform a `whois` lookup on the `inlanefreight.com` domain, piping the results into `grep` so they may easily find the `IANA ID` of the registrar:

Code: shell

```shell
whois inlanefreight.com | grep IANA
```

  Skills Assessment

```shell-session
┌─[us-academy-4]─[10.10.14.3]─[htb-ac-594497@htb-ccbetqvkvg]─[~]
└──╼ [★]$ whois inlanefreight.com | grep IANA

   Registrar IANA ID: {hidden}
Registrar IANA ID: {hidden}
```

Answer: {hidden}

# Skills Assessment

## Question 2

### "What http server software is powering the inlanefreight.htb site on the target system? Respond with the name of the software, not the version, e.g., Apache."

Students need to first add the entry for `inlanefreight.htb` to their `/etc/hosts` file:

Code: shell

```shell
sudo sh -c "echo 'STMIP inlanefreight.htb' >> /etc/hosts"
```

  Skills Assessment

```shell-session
┌─[us-academy-4]─[10.10.14.3]─[htb-ac-594497@htb-ccbetqvkvg]─[~]
└──╼ [★]$ sudo sh -c "echo '94.237.50.45 inlanefreight.htb' >> /etc/hosts"
```

Then, students need to run the `curl` command against `http://inlanefreight.htb:STMPO`, supplying the `-I` option to view only the response headers:

Code: shell

```shell
curl -I http://inlanefreight.htb:STMPO
```

  Skills Assessment

```shell-session
┌─[us-academy-4]─[10.10.14.3]─[htb-ac-594497@htb-ccbetqvkvg]─[~]
└──╼ [★]$ curl -I http://inlanefreight.htb:37705

HTTP/1.1 200 OK
Server: {hidden}/1.26.1
Date: Fri, 21 Jun 2024 21:14:55 GMT
Content-Type: text/html
Content-Length: 120
Last-Modified: Fri, 07 Jun 2024 14:56:31 GMT
Connection: keep-alive
ETag: "66631f9f-78"
Accept-Ranges: bytes
```

Answer: {hidden}

# Skills Assessment

## Question 3

### "What is the API key in the hidden admin directory that you have discovered on the target system?"

Students need to use `gobuster`, and proceed to fuzz the `inlanefreight.htb` domain for additional vhosts:

Code: shell

```shell
gobuster vhost -u http://inlanefreight.htb:SMTPO -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -t 60 --append-domain
```

  Skills Assessment

```shell-session
┌─[us-academy-4]─[10.10.14.3]─[htb-ac-594497@htb-envoycaulr]─[~]
└──╼ [★]$ gobuster vhost -u http://inlanefreight.htb:58825 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -t 60 --append-domain

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:             http://inlanefreight.htb:49765
[+] Method:          GET
[+] Threads:         60
[+] Wordlist:        /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt
[+] User Agent:      gobuster/3.6
[+] Timeout:         10s
[+] Append Domain:   true
===============================================================
2024/06/22 00:31:00 Starting gobuster in VHOST enumeration mode
===============================================================
Found: web1337.inlanefreight.htb:58825 (Status: 200) [Size: 104]
                                                                
===============================================================
2024/06/22 00:33:28 Finished
===============================================================
```

After a few moments, a new virtual host will be revealed: `web1337.inlanefreight.htb`, which students need to then add to their `hosts` file:

Code: shell

```shell
sudo sh -c "echo 'STMIP web1337.inlanefreight.htb' >> /etc/hosts"
```

  Skills Assessment

```shell-session
┌─[us-academy-4]─[10.10.14.3]─[htb-ac-594497@htb-envoycaulr]─[~]
└──╼ [★]$ sudo sh -c "echo '94.237.54.176 web1337.inlanefreight.htb' >> /etc/hosts"
```

Furthermore, students need to enumerate the contents of the `robots.txt` file found on the `web1337.inlanefreight.htb` vhost:

Code: shell

```shell
curl http://web1337.inlanefreight.htb:STMPO/robots.txt
```

  Skills Assessment

```shell-session
┌─[us-academy-4]─[10.10.14.3]─[htb-ac-594497@htb-txguqg3mxx]─[~]
└──╼ [★]$ curl http://web1337.inlanefreight.htb:46840/robots.txt

User-agent: *
Allow: /index.html
Allow: /index-2.html
Allow: /index-3.html
Disallow: /admin_h1dd3n
```

Of particular interest is the single `Disallow` directive, which applies to all User Agents, and prevents them from crawling the `/admin_h1dd3n` page.

Therefore, students need to enumerate page further; starting by using `curl -I` to make a `HEAD` request and viewing the response headers:

Code: shell

```shell
curl -I http://web1337.inlanefreight.htb:STMPO/admin_h1dd3n
```

  Skills Assessment

```shell-session
┌─[us-academy-4]─[10.10.14.3]─[htb-ac-594497@htb-txguqg3mxx]─[~]
└──╼ [★]$ curl -I http://web1337.inlanefreight.htb:46840/admin_h1dd3n

HTTP/1.1 301 Moved Permanently
Server: nginx/1.26.1
Date: Sat, 22 Jun 2024 17:25:19 GMT
Content-Type: text/html
Content-Length: 169
Location: http://web1337.inlanefreight.htb/admin_h1dd3n/
Connection: keep-alive
```

Examining the response closely, students will find the HTTP Response Code: `301 Moved Permanently`, with the `Location` set to `http://web1337.inlanefreight.htb/admin_h1dd3n/`.

Subsequently, students need make a `GET` request to the aforementioned `/admin_h1dd3n/` endpoint:

Code: shell

```shell
curl http://web1337.inlanefreight.htb:STMPO/admin_h1dd3n/
```

  Skills Assessment

```shell-session
┌─[us-academy-4]─[10.10.14.3]─[htb-ac-594497@htb-txguqg3mxx]─[~]
└──╼ [★]$ curl http://web1337.inlanefreight.htb:46840/admin_h1dd3n/

<!DOCTYPE html><html><head><title>web1337 admin</title></head><body><h1>Welcome to web1337 admin site</h1><h2>The admin panel is currently under maintenance, but the API is still accessible with the key {hidden}</h2></body></html>
```

Students may note that In URLs, the presence of a trailing slash typically indicates that the resource is a directory, while the absence of a trailing slash usually suggests a file. However, this is not a strict rule and can vary based on how the web server is configured; with this scenario being an exception to the rule.

Answer: {hidden}

# Skills Assessment

## Question 4

### "After crawling the inlanefreight.htb domain on the target system, what is the email address you have found? Respond with the full email, e.g., mail@inlanefreight.htb."

To begin, students need to add entries for both `inlanefreight.htb` and`web1337.inlanefreight.htb` to their `/etc/hosts` file:

Code: shell

```shell
sudo sh -c "echo 'STMIP inlanefreight.htb web1337.inlanefreight.htb' >> /etc/hosts"
```

  Skills Assessment

```shell-session
┌─[us-academy-4]─[10.10.14.50]─[htb-ac-594497@htb-jq82a8ul9t]─[~]
└──╼ [★]$ sudo sh -c "echo '94.237.54.176 inlanefreight.htb web1337.inlanefreight.htb' >> /etc/hosts"
```

Then, students need to continue fuzzing for virtual hosts, this time targeting `web1337.inlanefreight.htb`:

Code: shell

```shell
gobuster vhost -u http://web1337.inlanefreight.htb:STMPO -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -t 60 --append-domain
```

  Skills Assessment

```shell-session
┌─[us-academy-1]─[10.10.14.50]─[htb-ac-594497@htb-jq82a8ul9t]─[~]
└──╼ [★]$ gobuster vhost -u http://web1337.inlanefreight.htb:49765 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -t 60 --append-domain

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:             http://web1337.inlanefreight.htb:49765
[+] Method:          GET
[+] Threads:         60
[+] Wordlist:        /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt
[+] User Agent:      gobuster/3.6
[+] Timeout:         10s
[+] Append Domain:   true
===============================================================
2024/06/22 04:28:53 Starting gobuster in VHOST enumeration mode
===============================================================
Found: dev.web1337.inlanefreight.htb:52590 (Status: 200) [Size: 123]
```

In just a few moments, students will see `dev.web1337.inlanefreight.htb` appear in the `gobuster` output; a compelling candidate for a web crawler. Students need to add `dev.web1337.inlanefreight.htb` to their hosts file:

Code: shell

```shell
sudo sh -c "echo 'STMIP dev.web1337.inlanefreight.htb' >> /etc/hosts"
```

  Skills Assessment

```shell-session
┌─[us-academy-4]─[10.10.14.50]─[htb-ac-594497@htb-jq82a8ul9t]─[~]
└──╼ [★]$ sudo sh -c "echo '94.237.54.176 dev.web1337.inlanefreight.htb' >> /etc/hosts"
```

Now, students need install the `Scrapy` python library, along with the `ReconSpider.py` crawler (previously showcased in the `Creepy Crawlies` section):

Code: shell

```shell
pip3 install scrapy --break-system-packages
wget https://academy.hackthebox.com/storage/modules/279/ReconSpider.zip ; unzip ReconSpider.zip
```

  Skills Assessment

```shell-session
┌─[us-academy-4]─[10.10.14.50]─[htb-ac-594497@htb-jq82a8ul9t]─[~]
└──╼ [★]$ pip3 install scrapy --break-system-packages

Collecting scrapy
  Downloading Scrapy-2.11.2-py2.py3-none-any.whl (290 kB)
     |████████████████████████████████| 290 kB 28.7 MB/s 
Requirement already satisfied: setuptools in /usr/lib/python3/dist-packages (from scrapy) (66.1.1)
<SNIP>
Successfully installed PyDispatcher-2.0.7 cssselect-1.2.0 defusedxml-0.7.1 itemadapter-0.9.0 itemloaders-1.3.1 parsel-1.9.1 protego-0.3.1 queuelib-1.7.0 requests-file-2.1.0 scrapy-2.11.2 tldextract-5.1.2 w3lib-2.2.1

┌─[us-academy-4]─[10.10.14.50]─[htb-ac-594497@htb-jq82a8ul9t]─[~]
└──╼ [★]$ wget https://academy.hackthebox.com/storage/modules/279/ReconSpider.zip ; unzip ReconSpider.zip

--2024-06-24 02:22:36--  https://academy.hackthebox.com/storage/modules/279/ReconSpider.zip
Resolving academy.hackthebox.com (academy.hackthebox.com)... 104.18.20.126, 104.18.21.126, 2606:4700::6812:147e, ...
Connecting to academy.hackthebox.com (academy.hackthebox.com)|104.18.20.126|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1706 (1.7K) [application/zip]
Saving to: ‘ReconSpider.zip’

ReconSpider.zip     100%[==================>]   1.67K  --.-KB/s    in 0s      

2024-06-24 02:22:36 (30.9 MB/s) - ‘ReconSpider.zip’ saved [1706/1706]

Archive:  ReconSpider.zip
  inflating: ReconSpider.py       
```

Now, students need to use `ReconSpider.py` to crawl the recently discovered `dev.web1337.inlanefreight.htb` virtual host:

Code: shell

```shell
python3 ReconSpider.py http://dev.web1337.inlanefreight.htb:STMPO
```

  Skills Assessment

```shell-session
┌─[us-academy-4]─[10.10.14.50]─[htb-ac-594497@htb-jq82a8ul9t]─[~]
└──╼ [★]$ python3 ReconSpider.py http://dev.web1337.inlanefreight.htb:52590

2024-06-24 04:48:53 [scrapy.utils.log] INFO: Scrapy 2.11.2 started (bot: scrapybot)
2024-06-24 04:48:53 [scrapy.utils.log] INFO: Versions: lxml 4.6.3.0, libxml2 2.9.10, cssselect 1.2.0, parsel 1.9.1, w3lib 2.2.1, Twisted 20.3.0, Python 3.9.2 (default, Feb 28 2021, 17:03:44) - [GCC 10.2.1 20210110], pyOpenSSL 23.1.1 (OpenSSL 3.1.0 14 Mar 2023), cryptography 40.0.1, Platform Linux-6.1.0-1parrot1-amd64-x86_64-with-glibc2.31
2024-06-24 04:48:53 [scrapy.addons] INFO: Enabled addons:
<SNIP>
2024-06-24 04:49:11 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 31487,
 'downloader/request_count': 100,
 'downloader/request_method_count/GET': 100,
 'downloader/response_bytes': 34099,
 'downloader/response_count': 100,
 'downloader/response_status_count/200': 100,
 'elapsed_time_seconds': 17.719844,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2024, 6, 24, 3, 49, 11, 489386, tzinfo=datetime.timezone.utc),
 'log_count/INFO': 10,
 'log_count/WARNING': 1,
 'memusage/max': 67969024,
 'memusage/startup': 67969024,
 'request_depth_max': 99,
 'response_received_count': 100,
 'scheduler/dequeued': 100,
 'scheduler/dequeued/memory': 100,
 'scheduler/enqueued': 100,
 'scheduler/enqueued/memory': 100,
 'start_time': datetime.datetime(2024, 6, 24, 3, 48, 53, 769542, tzinfo=datetime.timezone.utc)}
2024-06-24 04:49:11 [scrapy.core.engine] INFO: Spider closed (finished)
```

At last, students need to analyze any email addresses that were identified and saved into the `results.json` file:

Code: shell

```shell
cat results.json | jq '.emails'
```

  Skills Assessment

```shell-session
┌─[us-academy-4]─[10.10.14.50]─[htb-ac-594497@htb-jq82a8ul9t]─[~]
└──╼ [★]$ cat results.json | jq '.emails'

[
  "{hidden}"
]
```

Answer: {hidden}

# Skills Assessment

## Question 5

### "What is the API key the inlanefreight.htb developers will be changing too?"

Students need to analyze the data saved to the `results.json` file, after successfully crawling the `dev.web1337.inlanefreight.htb` virtual host during the previous question. Specifically, students need to focus on any `comments` that were found by the crawler:

Code: shell

```shell
cat results.json | jq '.comments'
```

  Skills Assessment

```shell-session
┌─[us-academy-4]─[10.10.14.50]─[htb-ac-594497@htb-jq82a8ul9t]─[~]
└──╼ [★]$ cat results.json | jq '.comments'

[
  "<!-- Remember to change the API key to {hidden} -->"
]
```

Answer: {hidden}