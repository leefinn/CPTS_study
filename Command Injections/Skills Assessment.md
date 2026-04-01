## Question 1

### "What is the content of '/flag.txt'?"

After spawning the target machine, students need to navigate to its website's root webpage and login with the credentials `guest:guest`:

![Command_Injections_Walkthrough_Image_10.png](https://academy.hackthebox.com/storage/walkthroughs/43/Command_Injections_Walkthrough_Image_10.png)

Once signed in to the web-based file manager, students will find several files and a folder, with the former having four clickable buttons, `Preview`, `Copy to...`, `Direct link`, and `Download`. Out of the four, the `Copy to...` button seems the most plausible to be an attack vector, as the backend will need to use system commands such as `mv`, `move`, or `cp`. Clicking on `Copy to...` on a file will redirect students to a new page with two main options `Copy` and `Move`, while also being able to choose the destination folder:

![Command_Injections_Walkthrough_Image_11.png](https://academy.hackthebox.com/storage/walkthroughs/43/Command_Injections_Walkthrough_Image_11.png)

![Command_Injections_Walkthrough_Image_12.png](https://academy.hackthebox.com/storage/walkthroughs/43/Command_Injections_Walkthrough_Image_12.png)

If students select the destination folder `tmp` and click on `Copy`, injecting characters in the URL, no indication of command execution will appear. Therefore, students need to test the `Move` functionality. Clicking `Move` on a file without the selecting the `tmp` folder as the destination folder will throw the following error:

![Command_Injections_Walkthrough_Image_13.png](https://academy.hackthebox.com/storage/walkthroughs/43/Command_Injections_Walkthrough_Image_13.png)

Thus, most probably, the backend is using a `mv` command, and if an error occurs, it prints it out; therefore, this may be abused to capture command output, however, students need to ensure that the original `mv` command fails, otherwise error messages may not be displayed. Additionally, students need to use an injection operator that will show either both or only the second command, even if the first fails, which rules out the operator `&&`, however, any other operator may be used.

Students then need to run `Burp Suite`, set `FoxyProxy` to the preconfigured option "BURP", and then click on `Move` with no destination folder to move a file, same as done previously:

![Command_Injections_Walkthrough_Image_14.png](https://academy.hackthebox.com/storage/walkthroughs/43/Command_Injections_Walkthrough_Image_14.png)

Students need to send the intercepted request to `Repeater` (`Ctrl` + `R`) and send the request:

![Command_Injections_Walkthrough_Image_15.png](https://academy.hackthebox.com/storage/walkthroughs/43/Command_Injections_Walkthrough_Image_15.png)

After receiving the response, students will find the same error message in line 732:

![Command_Injections_Walkthrough_Image_16.png](https://academy.hackthebox.com/storage/walkthroughs/43/Command_Injections_Walkthrough_Image_16.png)

Students will notice that there are two GET parameters being passed in the request, `to` and `from`. Trying to inject different injection operators in both parameters, students will receive the error message "Malicious request denied!":

![Command_Injections_Walkthrough_Image_17.png](https://academy.hackthebox.com/storage/walkthroughs/43/Command_Injections_Walkthrough_Image_17.png)

However, when injecting the `&` operator, students will notice that it passes by, as the developers may have thought that it is required for URLs, and thus whitelisted it:

![Command_Injections_Walkthrough_Image_18.png](https://academy.hackthebox.com/storage/walkthroughs/43/Command_Injections_Walkthrough_Image_18.png)

Thus, students need to use this injection operator, however, it must be URL encoded, i.e., `%26`. Subsequently, students need to determine which parameter to be used for the injections, and in this case, either can be used, since both constitute the command being run by the backend, as seen by the printed error previously. Students need to inject `& cat /flag.txt` to read the flag file; to bypass white-space, students can either use `$IFS` or `%09`, and to bypass slashes, students need to use `${PATH:0:1}`, therefore, the payload can either be `$IFS%26c"a"t$IFS${PATH:0:1}flag.txt`, or `$IFS%26b"a"sh<<<$(base64%09-d<<<Y2F0IC9mbGFnLnR4dA==)`.

With the former payload, the URL parameters will be `/index.php?to=tmp$IFS%26c"a"t$IFS${PATH:0:1}flag.txt&from=51459716.txt&finish=1&move=1`:

![Command_Injections_Walkthrough_Image_19.png](https://academy.hackthebox.com/storage/walkthroughs/43/Command_Injections_Walkthrough_Image_19.png)

While with the the latter payload, the URL parameters will be `/index.php?to=tmp$IFS%26b"a"sh<<<$(base64%09-d<<<Y2F0IC9mbGFnLnR4dA==)&from=51459716.txt&finish=1&move=1`. Students will attain the flag `HTB{c0mm4nd3r_1nj3c70r}` with either payloads.:

![Command_Injections_Walkthrough_Image_20.png](https://academy.hackthebox.com/storage/walkthroughs/43/Command_Injections_Walkthrough_Image_20.png)

Answer: {hidden}