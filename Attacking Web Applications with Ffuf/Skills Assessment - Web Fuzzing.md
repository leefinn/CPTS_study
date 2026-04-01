# 

---

You are given an online academy's IP address but have no further information about their website. As the first step of conducting a Penetration Test, you are expected to locate all pages and domains linked to their IP to enumerate the IP and domains properly.

Finally, you should do some fuzzing on pages you identify to see if any of them has any parameters that can be interacted with. If you do find active parameters, see if you can retrieve any data from them.

---
# Skills Assessment - Web Fuzzing

## Question 1

### "Run a sub-domain/vhost fuzzing scan on '*.academy.htb' for the IP shown above. What are all the sub-domains you can identify?"

After spawning the target machine, students first need to determine the response size of a sent request with an inexistent/erroneous VHost:

Code: shell

```shell
ffuf -w /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://STMIP:STMPO -H 'Host: FUZZ.academy.htb'
```

  Skills Assessment - Web Fuzzing

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-2lv8nqz9tn]─[~]
└──╼ [★]$ ffuf -w /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://206.189.27.155:30596 -H 'Host: FUZZ.academy.htb'

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://206.189.27.155:30596
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt
 :: Header           : Host: FUZZ.academy.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

pop3                    [Status: 200, Size: 985, Words: 423, Lines: 55, Duration: 1ms]
mail                    [Status: 200, Size: 985, Words: 423, Lines: 55, Duration: 1ms]
localhost               [Status: 200, Size: 985, Words: 423, Lines: 55, Duration: 2ms]

<SNIP>
```

The response size for any erroneous VHost is 985, thus, students need to filter it out using the `-fs` flag:

Code: shell

```shell
ffuf -w /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://STMIP:STMPO -H 'Host: FUZZ.academy.htb' -fs 985
```

  Skills Assessment - Web Fuzzing

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-2lv8nqz9tn]─[~]
└──╼ [★]$ ffuf -w /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://206.189.27.155:30596 -H 'Host: FUZZ.academy.htb' -fs 985

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://206.189.27.155:30596
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt
 :: Header           : Host: FUZZ.academy.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
 :: Filter           : Response size: 985
________________________________________________

test                    [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 1ms]
archive                 [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 4ms]
faculty                 [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 4ms]
:: Progress: [4997/4997] :: Job [1/1] :: 595 req/sec :: Duration: [0:00:08] :: Errors: 0 ::
```

Alternatively, instead of manually fuzzing the erroneous response size, students can use the `-ac` flag to automatically calibrate filtering options:

Code: shell

```shell
ffuf -w /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://STMIP:STMPO-H 'Host: FUZZ.academy.htb' -ac
```

  Skills Assessment - Web Fuzzing

```shell-session
┌─[htb-ac413848@htb-xihle56b8d]─[~]
└──╼ $ffuf -w /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://178.128.37.153:32342 -H 'Host: FUZZ.academy.htb' -ac

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://178.128.37.153:32342
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt
 :: Header           : Host: FUZZ.academy.htb
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
 :: Filter           : Response size: 985
 :: Filter           : Response words: 423
 :: Filter           : Response lines: 55
________________________________________________

archive                 [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 20ms]
faculty                 [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 21ms]
test                    [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 3574ms]
:: Progress: [4997/4997] :: Job [1/1] :: 802 req/sec :: Duration: [0:00:05] :: Errors: 0 ::
```

Three VHosts exist, `test`, `archive`, and `faculty`.

Answer: {hidden}

# Skills Assessment - Web Fuzzing

## Question 2

### "Before you run your page fuzzing scan, you should first run an extension fuzzing scan. What are the different extensions accepted by the domains?"

From the previous question, students know that there are three VHosts, `test`, `archive`, and `faculty`, therefore, they need to run an extension fuzzing scan on all of them, one by one. However, students first need to add these entries into `/etc/hosts`:

Code: shell

```shell
sudo bash -c 'echo "STMIP test.academy.htb archive.academy.htb faculty.academy.htb" >> /etc/hosts'
```

  Skills Assessment - Web Fuzzing

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-2lv8nqz9tn]─[~]
└──╼ [★]$ sudo bash -c 'echo "206.189.27.155 test.academy.htb archive.academy.htb faculty.academy.htb" >> /etc/hosts'
```

Then, starting with the `test` VHost, students need to fuzz extensions on the `index` webpage, to know that the extensions `.php` and `.phps` are accepted:

Code: shell

```shell
ffuf -w /opt/useful/SecLists/Discovery/Web-Content/web-extensions.txt:FUZZ -u http://test.academy.htb:STMPO/indexFUZZ
```

  Skills Assessment - Web Fuzzing

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-2lv8nqz9tn]─[~]
└──╼ [★]$ ffuf -w /opt/useful/SecLists/Discovery/Web-Content/web-extensions.txt:FUZZ -u http://test.academy.htb:30596/indexFUZZ

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://test.academy.htb:30596/indexFUZZ
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/Web-Content/web-extensions.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

.php                    [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 1ms]
.phps                   [Status: 403, Size: 284, Words: 20, Lines: 10, Duration: 2ms]
:: Progress: [39/39] :: Job [1/1] :: 214 req/sec :: Duration: [0:00:02] :: Errors: 0 ::
```

Then, extension fuzzing on the `/index` webpage needs to be done for the `archive` VHost, to know that the extensions `.php` and `.phps` are accepted:

Code: shell

```shell
ffuf -w /opt/useful/SecLists/Discovery/Web-Content/web-extensions.txt:FUZZ -u http://archive.academy.htb:STMPO/indexFUZZ
```

  Skills Assessment - Web Fuzzing

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-2lv8nqz9tn]─[~]
└──╼ [★]$ ffuf -w /opt/useful/SecLists/Discovery/Web-Content/web-extensions.txt:FUZZ -u http://archive.academy.htb:30596/indexFUZZ

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://archive.academy.htb:30596/indexFUZZ
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/Web-Content/web-extensions.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

.phps                   [Status: 403, Size: 287, Words: 20, Lines: 10, Duration: 1ms]
.php                    [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 2ms]
:: Progress: [39/39] :: Job [1/1] :: 576 req/sec :: Duration: [0:00:01] :: Errors: 0 ::
```

At last, extension fuzzing on the `/index` webpage needs to be done for the `faculty` VHost, to know that the extensions `.phps`, `.php`, and `.php7` are accepted:

Code: shell

```shell
ffuf -w /opt/useful/SecLists/Discovery/Web-Content/web-extensions.txt:FUZZ -u http://faculty.academy.htb:STMPO/indexFUZZ
```

  Skills Assessment - Web Fuzzing

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-2lv8nqz9tn]─[~]
└──╼ [★]$ ffuf -w /opt/useful/SecLists/Discovery/Web-Content/web-extensions.txt:FUZZ -u http://faculty.academy.htb:30596/indexFUZZ

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://faculty.academy.htb:30596/indexFUZZ
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/Web-Content/web-extensions.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

.phps                   [Status: 403, Size: 287, Words: 20, Lines: 10, Duration: 1ms]
.php                    [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 1ms]
.php7                   [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 2ms]
:: Progress: [39/39] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errors: 0 ::
```

Answer: {hidden}

# Skills Assessment - Web Fuzzing

## Question 3

### "One of the pages you will identify should say 'You don't have access!'. What is the full page URL?"

From the hint for this question, students know that they need to perform recursive fuzzing on all of the VHosts found, therefore, after fuzzing the `test` and `archive` VHosts, students will know that they do not contain the answer. Students need to perform directory fuzzing on the `faculty` VHost, setting the recursion depth to 1 and utilizing the three previously found extensions `.php`, `.phps`, and `.php7`. The response size of a request with an erroneous directory is 287, therefore, students need to filter this response size out (or alternatively, use the `-ac` option for automatically calibrating the filtering options). Additionally, students can utilize the `-mr` matcher option, which matches a regular expression, which in this case is "You don't have access!":

Code: shell

```shell
ffuf -w /opt/useful/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://faculty.academy.htb:STMPO/FUZZ -recursion -recursion-depth 1 -e .php,.phps,.php7 -fs 287 -mr "You don't have access!" -t 100
```

  Skills Assessment - Web Fuzzing

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-2lv8nqz9tn]─[~]
└──╼ [★]$ ffuf -w /opt/useful/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://faculty.academy.htb:30511/FUZZ -recursion -recursion-depth 1 -e .php,.php,.php7 -fs 287 -mr "You don't have access!" -t 100

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://faculty.academy.htb:30511/FUZZ
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt
 :: Extensions       : .php .php .php7 
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Regexp: You don't have access!
 :: Filter           : Response size: 287
________________________________________________

[INFO] Adding a new job to the queue: http://faculty.academy.htb:30511/courses/FUZZ
```

`Ffuf` will quickly find the `/courses/` directory, therefore, instead of waiting for the other entries to be fuzzed, students can speed up the process by canceling this `Ffuf` command and starting a new one without recursion, specifying the directory path to be `/courses/FUZZ`:

Code: shell

```shell
ffuf -w /opt/useful/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://faculty.academy.htb:STMPO/courses/FUZZ -e .php,.php,.php7 -fs 287 -mr "You don't have access!" -t 100
```

  Skills Assessment - Web Fuzzing

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-2lv8nqz9tn]─[~]
└──╼ [★]$ ffuf -w /opt/useful/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://faculty.academy.htb:30511/courses/FUZZ -e .php,.php,.php7 -fs 287 -mr "You don't have access!" -t 100

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://faculty.academy.htb:30511/courses/FUZZ
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt
 :: Extensions       : .php .php .php7 
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Regexp: You don't have access!
 :: Filter           : Response size: 287
________________________________________________

linux-security.php7     [Status: 200, Size: 774, Words: 223, Lines: 53, Duration: 3ms]
```

From the output of `Ffuf`, students will know that the page `/linux-security.php7` is the one says "You don't have access". Thus, the full path to this file becomes `http://faculty.academy.htb:PORT/courses/linux-security.php7`.

Answer: {hidden}

# Skills Assessment - Web Fuzzing

## Question 4

### "In the page from the previous question, you should be able to find multiple parameters that are accepted by the page. What are they?"

From the previous question, students know that the page is located at `/courses/linux-security.php7`, therefore, they need to utilize the same technique that was taught in the "Parameter Fuzzing - POST" section of the module. First, students need to know the response size of a request with an inexistent `POST` parameter:

Code: shell

```shell
ffuf -w /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://faculty.academy.htb:STMPO/courses/linux-security.php7 -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded'
```

  Skills Assessment - Web Fuzzing

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-y2llhq5gie]─[~]
└──╼ [★]$ ffuf -w /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://faculty.academy.htb:32569/courses/linux-security.php7 -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded'

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://faculty.academy.htb:32569/courses/linux-security.php7
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : FUZZ=key
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

password                [Status: 200, Size: 774, Words: 223, Lines: 53, Duration: 1ms]
debug                   [Status: 200, Size: 774, Words: 223, Lines: 53, Duration: 1ms]
page                    [Status: 200, Size: 774, Words: 223, Lines: 53, Duration: 2ms]
email                   [Status: 200, Size: 774, Words: 223, Lines: 53, Duration: 2ms]

<SNIP>
```

The response size for any erroneous `POST` parameter is 774, thus, students need to filter it out using the `-fs` flag:

Code: shell

```shell
ffuf -w /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://faculty.academy.htb:STMPO/courses/linux-security.php7 -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded' -fs 774 -t 100
```

  Skills Assessment - Web Fuzzing

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-y2llhq5gie]─[~]
└──╼ [★]$ ffuf -w /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://faculty.academy.htb:32569/courses/linux-security.php7 -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded' -fs 774 -t 100

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://faculty.academy.htb:32569/courses/linux-security.php7
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : FUZZ=key
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
 :: Filter           : Response size: 774
________________________________________________

user                    [Status: 200, Size: 780, Words: 223, Lines: 53, Duration: 1ms]
username                [Status: 200, Size: 781, Words: 223, Lines: 53, Duration: 431ms]
:: Progress: [2588/2588] :: Job [1/1] :: 286 req/sec :: Duration: [0:00:06] :: Errors: 0 ::
```

From the output of `Ffuf`, students will know that the `POST` parameters are `user` and `username`.

Answer: {hidden}

# Skills Assessment - Web Fuzzing

## Question 5

### "Try fuzzing the parameters you identified for working values. One of them should return a flag. What is the content of the flag?"

From the previous question, students will know that the two `POST` parameters are `user` and `username`. Therefore, students need to fuzz the valid value for the parameter `username`. First, students need to determine the response size of a request with an erroneous value for the `username` `POST` parameter, finding it to be 781:

Code: shell

```shell
ffuf -w /opt/useful/SecLists/Usernames/Names/names.txt:FUZZ -u http://faculty.academy.htb:STMPO/courses/linux-security.php7 -X POST -d 'username=FUZZ' -H 'Content-Type: application/x-www-form-urlencoded' -t 100
```

  Skills Assessment - Web Fuzzing

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-y2llhq5gie]─[~]
└──╼ [★]$ ffuf -w /opt/useful/SecLists/Usernames/Names/names.txt:FUZZ -u http://faculty.academy.htb:31312/courses/linux-security.php7 -X POST -d 'username=FUZZ' -H 'Content-Type: application/x-www-form-urlencoded'

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://faculty.academy.htb:31312/courses/linux-security.php7
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Usernames/Names/names.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : username=FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

abbie                   [Status: 200, Size: 781, Words: 223, Lines: 53, Duration: 2ms]
aaliyah                 [Status: 200, Size: 781, Words: 223, Lines: 53, Duration: 2ms]
abahri                  [Status: 200, Size: 781, Words: 223, Lines: 53, Duration: 1ms]
abbi                    [Status: 200, Size: 781, Words: 223, Lines: 53, Duration: 3ms]
```

Thus, students need to filter it out using the `-fs` flag:

Code: shell

```shell
ffuf -w /opt/useful/SecLists/Usernames/Names/names.txt:FUZZ -u http://faculty.academy.htb:STMPO/courses/linux-security.php7 -X POST -d 'username=FUZZ' -H 'Content-Type: application/x-www-form-urlencoded' -fs 781 -t 100
```

  Skills Assessment - Web Fuzzing

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-y2llhq5gie]─[~]
└──╼ [★]$ ffuf -w /opt/useful/SecLists/Usernames/Names/names.txt:FUZZ -u http://faculty.academy.htb:31312/courses/linux-security.php7 -X POST -d 'username=FUZZ' -H 'Content-Type: application/x-www-form-urlencoded' -fs 781 -t 100

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://faculty.academy.htb:31312/courses/linux-security.php7
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Usernames/Names/names.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : username=FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
 :: Filter           : Response size: 781
________________________________________________

harry                   [Status: 200, Size: 773, Words: 218, Lines: 53, Duration: 0ms]
:: Progress: [10164/10164] :: Job [1/1] :: 215 req/sec :: Duration: [0:00:24] :: Errors: 0 ::
```

From the output, students will know that the valid value for the `POST` parameter `username` is `harry`. At last, to attain the flag `HTB{w3b_fuzz1n6_m4573r}`, students need to use `cURL` with the `POST` parameter `username` and the value `harry`:

Code: shell

```shell
curl -s http://faculty.academy.htb:STMPO/courses/linux-security.php7 -X POST -d 'username=harry' | grep "HTB{.*}"
```

  Skills Assessment - Web Fuzzing

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-y2llhq5gie]─[~]
└──╼ [★]$ curl -s http://faculty.academy.htb:31312/courses/linux-security.php7 -X POST -d 'username=harry' | grep "HTB{.*}"

<div class='center'><p>HTB{w3b_fuzz1n6_m4573r}</p></div>
```

Answer: {hidden}
