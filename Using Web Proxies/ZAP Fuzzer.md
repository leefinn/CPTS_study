
---

ZAP's Fuzzer is called (`ZAP Fuzzer`). It can be very powerful for fuzzing various web end-points, though it is missing some of the features provided by Burp Intruder. ZAP Fuzzer, however, does not throttle the fuzzing speed, which makes it much more useful than Burp's free Intruder.

In this section, we will try to replicate what we did in the previous section using ZAP Fuzzer to have an "apples to apples" comparison and decide which one we like best.

---

## Fuzz

To start our fuzzing, we will visit the URL from the exercise at the end of this section to capture a sample request. As we will be fuzzing for directories, let's visit `<http://SERVER_IP:PORT/test/>` to place our fuzzing location on `test` later on. Once we locate our request in the proxy history, we will right-click on it and select (`Attack>Fuzz`), which will open the `Fuzzer` window:

![Fuzz Locations interface with HTTP request details on the left and empty fuzz locations list on the right. Options to add, remove, and configure payloads and processors. 'Remove Without Confirmation' is checked.](https://academy.hackthebox.com/storage/modules/110/zap_fuzzer.jpg)

The main options we need to configure for our Fuzzer attack are:

- Fuzz Location
- Payloads
- Processors
- Options

Let's try to configure them for our web directory fuzzing attack.

---

## Locations

The `Fuzz Location` is very similar to `Intruder Payload Position`, where our payloads will be placed. To place our location on a certain word, we can select it and click on the `Add` button on the right pane. So, let's select `test` and click on `Add`:

![Fuzz Locations interface with highlighted 'test' in HTTP request. Popup shows location 'Header 31, 35', value 'test', and empty payloads list. 'Remove Without Confirmation' is checked.](https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_add.jpg)

As we can see, this placed a `green` marker on our selected location and opened the `Payloads` window for us to configure our attack payloads.

---

## Payloads

The attack payloads in ZAP's Fuzzer are similar in concept to Intruder's Payloads, though they are not as advanced as Intruder's. We can click on the `Add` button to add our payloads and select from 8 different payload types. The following are some of them:

- `File`: This allows us to select a payload wordlist from a file.
- `File Fuzzers`: This allows us to select wordlists from built-in databases of wordlists.
- `Numberzz`: Generates sequences of numbers with custom increments.

One of the advantages of ZAP Fuzzer is having built-in wordlists we can choose from so that we do not have to provide our own wordlist. More databases can be installed from the ZAP Marketplace, as we will see in a later section. So, we can select `File Fuzzers` as the `Type`, and then we will select the first wordlist from `dirbuster`:

![File Fuzzers interface with 'dirbuster' and 'directory-list-1.0.txt' selected. Payloads preview shows directory names like 'cgi-bin', '.git', '.svn'.](https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_add_payload.jpg)

Once we click the `Add` button, our payload wordlist will get added, and we can examine it with the `Modify` button.

---

## Processors

We may also want to perform some processing on each word in our payload wordlist. The following are some of the payload processors we can use:

- Base64 Decode/Encode
- MD5 Hash
- Postfix String
- Prefix String
- SHA-1/256/512 Hash
- URL Decode/Encode
- Script

As we can see, we have a variety of encoders and hashing algorithms to select from. We can also add a custom string before the payload with `Prefix String` or a custom string with `Postfix String`. Finally, the `Script` type allows us to select a custom script that we built and run on every payload before using it in the attack.

We will select the `URL Encode` processor for our exercise to ensure that our payload gets properly encoded and avoid server errors if our payload contains any special characters. We can click on the `Generate Preview` button to preview how our final payload will look in the request:

![URL Encode interface with UTF-8 encoding. Current and processed payloads include 'cgi-bin', '.git', '.svn'. 'Lock Scroll' is checked.](https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_add_processor.jpg)

Once that's done, we can click on `Add` to add the processor and click on `Ok` in the processors and payloads windows to close them.

---

## Options

Finally, we can set a few options for our fuzzers, similar to what we did with Burp Intruder. For example, we can set the `Concurrent threads per scan` to `20`, so our scan runs very quickly:

![Options interface for fuzzing. Retries on IO error: 3. Limit max errors: 1000. Depth First strategy selected. 20 concurrent threads. No delay in fuzzing. Follow Redirects unchecked.](https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_options.jpg)

The number of threads we set may be limited by how much computer processing power we want to use or how many connections the server allows us to establish.

We may also choose to run through the payloads `Depth first`, which would attempt all words from the wordlist on a single payload position before moving to the next (e.g., try all passwords for a single user before brute-forcing the following user). We could also use `Breadth first`, which would run every word from the wordlist on all payload positions before moving to the next word (e.g., attempt every password for all users before moving to the following password).

---

## Start

With all of our options configured, we can finally click on the `Start Fuzzer` button to start our attack. Once our attack is started, we can sort the results by the `Response` code, as we are only interested in responses with code `200`:

![Table showing task IDs, message types, HTTP codes, reasons, round-trip times, response sizes, states, and payloads. Example: Task ID 908, 200 OK, 109 ms, 246 bytes, state 'skills'.](https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_attack.jpg)

As we can see, we got one hit with code `200` with the `skills` payload, meaning that the `/skills/` directory exists on the server and is accessible. We can click on the request in the results window to view its details: ![Request and response details. Request: HTTP GET to /skills/. Response: 200 OK, includes Set-Cookie header, HTML content with 'Welcome' title.](https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_dir.jpg)

We can see from the response that this page is indeed accessible by us. There are other fields that may indicate a successful hit depending on the attack scenario, like `Size Resp. Body` which may indicate that we got a different page if its size was different than other responses, or `RTT` for attacks like `time-based SQL injections`, which are detected by a time delay in the server response.


---
## Question 1

### "The directory we found above sets the cookie to the md5 hash of the username, as we can see the md5 cookie in the request for the (guest) user. Visit '/skills/' to get a request with a cookie, then try to use ZAP Fuzzer to fuzz the cookie for different md5 hashed usernames to get the flag. (You may use the wordlist: /opt/useful/SecLists/Usernames/top-usernames-shortlist.txt)"

After spawning the target machine, students need to navigate to the `/skills/` directory, run `ZAP`, make sure that `FoxyProxy` is set to the preconfigured option "Burp (8080)" in `Firefox`, refresh the page on `/skills/` to capture the request in `ZAP` and view the cookie within the request:

![Using_Web_Proxies_Walkthrough_Image_18.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_18.png)

Students need to right-click on the request and select `Attack` -> `Fuzz`:

![Using_Web_Proxies_Walkthrough_Image_19.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_19.png)

Afterward, students need to select the value after `cookie=` and click on `Add` -> `Add`:

![Using_Web_Proxies_Walkthrough_Image_20.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_20.png)

![Using_Web_Proxies_Walkthrough_Image_21.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_21.png)

Subsequently, students need to choose `File` for `Type` and load the `/opt/useful/SecLists/Usernames/top-usernames-shortlist.txt` wordlist after clicking on `Select`:

![Using_Web_Proxies_Walkthrough_Image_22.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_22.png)

![Using_Web_Proxies_Walkthrough_Image_23.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_23.png)

After the wordlist is loaded, students need to click on `Add`:

![Using_Web_Proxies_Walkthrough_Image_24.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_24.png)

Subsequently, students need to click on `Processors`:

![Using_Web_Proxies_Walkthrough_Image_25.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_25.png)

And then click on `Add`:

![Using_Web_Proxies_Walkthrough_Image_26.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_26.png)

For `Type`, students need to choose `MD5 Hash` and then click on `Add`:

![Using_Web_Proxies_Walkthrough_Image_27.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_27.png)

After clicking on the two subsequent `OK` buttons, students need to click on `Start Fuzzer`:

![Using_Web_Proxies_Walkthrough_Image_28.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_28.png)

After fuzzing has finished, students need to sort the responses by body size and will find that one of the responses has a response size of 450 bytes; viewing the response body will reveal the flag `HTB{fuzz1n6_my_f1r57_c00k13}`:

![Using_Web_Proxies_Walkthrough_Image_29.png](https://academy.hackthebox.com/storage/walkthroughs/56/Using_Web_Proxies_Walkthrough_Image_29.png)

Answer: {hidden}