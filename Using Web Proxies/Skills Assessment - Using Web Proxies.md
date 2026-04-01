
## Question 1

### "The /lucky.php page has a button that appears to be disabled. Try to enable the button, and then click it to get the flag."

After spawning the target machine, students need to navigate to its website's `/lucky.php` page and notice that the "Click for a chance to win a flag!" button is disabled:

![Using_Web_Proxies_Walkthrough_Image_41.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_41.png)

Therefore, students need to run `ZAP` (`Burp Suite` can also be used), make sure that `FoxyProxy` is set to the preconfigured option "Burp (8080)" in `Firefox`, and refresh the page on `/lucky.php` to capture the request in `ZAP`. When viewing the response for the `GET` response sent to `/lucky.php`, students will notice that the button has the attribute `disabled`:

![Using_Web_Proxies_Walkthrough_Image_42.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_42.png)

Therefore, students need to open `Replacer` by clicking `Ctrl + R` and then `Add...`:

![Using_Web_Proxies_Walkthrough_Image_43.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_43.png)

Subsequently, students need to set `Match Type` to `Response Body String`, `Match String` to `disabled>`, `Replacement String` to `>`, check `Enable`, and click on `Save`:

![Using_Web_Proxies_Walkthrough_Image_44.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_44.png)

Then, students need to select the `GET` request and click on `Open/Resend with Request Editor...`:

![Using_Web_Proxies_Walkthrough_Image_45.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_45.png)

For easier usability, students can click on `Combined display for header and body`, `Request shown above Response` for the `Request` tab, and `Combined display for header and body` for the `Response` tab:

![Using_Web_Proxies_Walkthrough_Image_46.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_46.png)

Thereafter, after clicking `Send`, students will notice that the response body no longer contains `disabled`:

![Using_Web_Proxies_Walkthrough_Image_47.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_47.png)

Thus, students now need to right-click on the response and choose `Open URL in System Browser`, to notice that they can click the button as it is not disabled anymore (in case it is, it might be from cached pages, thus, students can press `Ctrl + Shift + R` to force refresh the page):

![Using_Web_Proxies_Walkthrough_Image_48.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_48.png)

![Using_Web_Proxies_Walkthrough_Image_49.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_49.png)

After clicking on the button around 8 times, students will attain the flag `HTB{d154bl3d_bu770n5_w0n7_570p_m3}`:

![Using_Web_Proxies_Walkthrough_Image_50.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_50.png)

Answer: {hidden}

# Skills Assessment - Using Web Proxies

## Question 2

### "The /admin.php page uses a cookie that has been encoded multiple time. Try to decode the cookie until you get a value with 31-characters. Submit the value as the answer."

After spawning the target machine, students need to run `ZAP` (`Burp Suite` can also be used), make sure that `FoxyProxy` is set to the preconfigured option "Burp (8080)" in `Firefox`, and navigate to `/admin.php` to capture the request in `ZAP` and notice the cookie value within the `Cookie` header:

![Using_Web_Proxies_Walkthrough_Image_51.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_51.png)

Students need to select the hash after `cookie=`, right-click and select `Encode/Decode/Hash...`:

![Using_Web_Proxies_Walkthrough_Image_52.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_52.png)

Then, students need to click on the `Decode` tab and copy the `ASCII Hex Decode` value then paste it in the `Text to be encoded/decode/hashed`. The `Base64 Decode` will contain the 31-characters value `3dac93b8cd250aa8c1a36fffc79a17a`::

![Using_Web_Proxies_Walkthrough_Image_53.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_53.png)

Answer: {hidden}

# Skills Assessment - Using Web Proxies

## Question 3

### "Once you decode the cookie, you will notice that it is only 31 characters long, which appears to be an md5 hash missing its last character. So, try to fuzz the last character of the decoded md5 cookie with all alpha-numeric characters, while encoding each request with the encoding methods you identified above. (You may use the "alphanum-case.txt" wordlist from SecLists for the payload)"

After spawning the target machine, students need to run `Burp Suite` (`ZAP` can also be used, however, it is more involved as it lacks an `ASCII-Hex` fuzzer processor, meaning that students are required to create a script for it manually), make sure that `FoxyProxy` is set to the preconfigured option "Burp (8080)" in `Firefox`, and navigate to `/admin.php` to capture the request in `Burp Suite` and notice the cookie value within the `Cookie` header. Students need to right-click on it and select `Send to Intruder`:

![Using_Web_Proxies_Walkthrough_Image_54.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_54.png)

Within `Intruder`, students first need to click on `Clear §`, replace the default cookie with the `MD5` hash `3dac93b8cd250aa8c1a36fffc79a17a` attained in the previous question, select it, and click on `Add §`:

![Using_Web_Proxies_Walkthrough_Image_55.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_55.png)

Subsequently, students need to click on the `Payloads` tab then on `Load ...` under `Payload Options` and load the file `alphanum-case.txt` from `/opt/useful/SecLists/Fuzzing/`:

![Using_Web_Proxies_Walkthrough_Image_56.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_56.png)

Then, under `Payload Processing`, students need to click on `Add`, select `Add prefix` as the processing rule, and paste in the `MD5` hash `3dac93b8cd250aa8c1a36fffc79a17a` for `Prefix`:

![Using_Web_Proxies_Walkthrough_Image_57.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_57.png)

Additionally, students need to add the `Base64-encode` and `Encode as ASCII hex` processing rules:

![Using_Web_Proxies_Walkthrough_Image_58.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_58.png)

![Using_Web_Proxies_Walkthrough_Image_59.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_59.png)

Thereafter, students need to click on `Start attack`:

![Using_Web_Proxies_Walkthrough_Image_60.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_60.png)

After fuzzing has completed, students can click on the `Length` column to sort by response size, and any response with the size of 1248 will contain the flag `HTB{burp_1n7rud3r_n1nj4!}` on line 42 in the response body:

![Using_Web_Proxies_Walkthrough_Image_61.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_61.png)

Answer: {hidden}

# Skills Assessment - Using Web Proxies

## Question 4

### "You are using the 'auxiliary/scanner/http/coldfusion_locale_traversal' tool within Metasploit, but it is not working properly for you. You decide to capture the request sent by Metasploit so you can manually verify it and repeat it. Once you capture the request, what is the 'XXXXX' directory being called in '/XXXXX/administrator/..'?"

Students first need to launch `msfconsole`:

Code: shell

```shell
msfconsole -q
```

  Skills Assessment - Using Web Proxies

```shell-session
┌─[eu-academy-1]─[10.10.14.153]─[htb-ac413848@htb-xx2fcfymke]─[~]
└──╼ [★]$ msfconsole -q

[msf](Jobs:0 Agents:0) >>
```

Subsequently, students need to use the module `auxiliary/scanner/http/coldfusion_locale_traversal`:

Code: shell

```shell
use auxiliary/scanner/http/coldfusion_locale_traversal
```

  Skills Assessment - Using Web Proxies

```shell-session
[msf](Jobs:0 Agents:0) >> use auxiliary/scanner/http/coldfusion_locale_traversal
[msf](Jobs:0 Agents:0) auxiliary(scanner/http/coldfusion_locale_traversal) >>
```

Then students need to set `PROXIES` to be the same as the one `Burp Suite`/`ZAP` listens on, while for `RHOST` and `RPORT` any random valid values can be used:

Code: shell

```shell
set PROXIES HTTP:127.0.0.1:8080
set RHOST STMIP
set RPORT STMPO
```

  Skills Assessment - Using Web Proxies

```shell-session
[msf](Jobs:0 Agents:0) auxiliary(scanner/http/coldfusion_locale_traversal) >> set PROXIES HTTP:127.0.0.1:8080

PROXIES => HTTP:127.0.0.1:8080
[msf](Jobs:0 Agents:0) auxiliary(scanner/http/coldfusion_locale_traversal) >> set RHOSTS 159.65.63.151
RHOSTS => 159.65.63.151
[msf](Jobs:0 Agents:0) auxiliary(scanner/http/coldfusion_locale_traversal) >> set RPORT 31845
RPORT => 31845
```

Before running the exploit, students need to make sure that `Burp Suite`/`ZAP` are intercepting requests, and then run the exploit:

Code: shell

```shell
run
```

  Skills Assessment - Using Web Proxies

```shell-session
auxiliary(scanner/http/coldfusion_locale_traversal) >> run
```

From the intercepted request, students will know that the directory the `msfconsole` module is sending a request to is `CFIDE`:

![Using_Web_Proxies_Walkthrough_Image_62.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_62.png)

Answer: {hidden}