# 

---

Applications that are connected to services often include connection strings that can be leaked if they are not protected sufficiently. In the following paragraphs, we will go through the process of enumerating and exploiting applications that are connected to other services in order to extend their functionality. This can help us collect information and move laterally or escalate our privileges during penetration testing.

---

## ELF Executable Examination

The `octopus_checker` binary is found on a remote machine during the testing. Running the application locally reveals that it connects to database instances in order to verify that they are available.

  Attacking Applications Connecting to Services

```shell-session
xF1NN@htb[/htb]$ ./octopus_checker 

Program had started..
Attempting Connection 
Connecting ... 

The driver reported the following diagnostics whilst running SQLDriverConnect

01000:1:0:[unixODBC][Driver Manager]Can't open lib 'ODBC Driver 17 for SQL Server' : file not found
connected
```

The binary probably connects using a SQL connection string that contains credentials. Using tools like [PEDA](https://github.com/longld/peda) (Python Exploit Development Assistance for GDB) we can further examine the file. This is an extension of the standard GNU Debugger (GDB), which is used for debugging C and C++ programs. GDB is a command line tool that lets you step through the code, set breakpoints, and examine and change variables. Running the following command we can execute the binary through it.

  Attacking Applications Connecting to Services

```shell-session
xF1NN@htb[/htb]$ gdb ./octopus_checker

GNU gdb (Debian 9.2-1) 9.2
Copyright (C) 2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./octopus_checker...
(No debugging symbols found in ./octopus_checker)
```

Once the binary is loaded, we set the `disassembly-flavor` to define the display style of the code, and we proceed with disassembling the main function of the program.

Code: assembly

```assembly
gdb-peda$ set disassembly-flavor intel
gdb-peda$ disas main

Dump of assembler code for function main:
   0x0000555555555456 <+0>:	endbr64 
   0x000055555555545a <+4>:	push   rbp
   0x000055555555545b <+5>:	mov    rbp,rsp
 
 <SNIP>
 
   0x0000555555555625 <+463>:	call   0x5555555551a0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x000055555555562a <+468>:	mov    rdx,rax
   0x000055555555562d <+471>:	mov    rax,QWORD PTR [rip+0x299c]        # 0x555555557fd0
   0x0000555555555634 <+478>:	mov    rsi,rax
   0x0000555555555637 <+481>:	mov    rdi,rdx
   0x000055555555563a <+484>:	call   0x5555555551c0 <_ZNSolsEPFRSoS_E@plt>
   0x000055555555563f <+489>:	mov    rbx,QWORD PTR [rbp-0x4a8]
   0x0000555555555646 <+496>:	lea    rax,[rbp-0x4b7]
   0x000055555555564d <+503>:	mov    rdi,rax
   0x0000555555555650 <+506>:	call   0x555555555220 <_ZNSaIcEC1Ev@plt>
   0x0000555555555655 <+511>:	lea    rdx,[rbp-0x4b7]
   0x000055555555565c <+518>:	lea    rax,[rbp-0x4a0]
   0x0000555555555663 <+525>:	lea    rsi,[rip+0xa34]        # 0x55555555609e
   0x000055555555566a <+532>:	mov    rdi,rax
   0x000055555555566d <+535>:	call   0x5555555551f0 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1EPKcRKS3_@plt>
   0x0000555555555672 <+540>:	lea    rax,[rbp-0x4a0]
   0x0000555555555679 <+547>:	mov    edx,0x2
   0x000055555555567e <+552>:	mov    rsi,rbx
   0x0000555555555681 <+555>:	mov    rdi,rax
   0x0000555555555684 <+558>:	call   0x555555555329 <_Z13extract_errorNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEPvs>
   0x0000555555555689 <+563>:	lea    rax,[rbp-0x4a0]
   0x0000555555555690 <+570>:	mov    rdi,rax
   0x0000555555555693 <+573>:	call   0x555555555160 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEED1Ev@plt>
   0x0000555555555698 <+578>:	lea    rax,[rbp-0x4b7]
   0x000055555555569f <+585>:	mov    rdi,rax
   0x00005555555556a2 <+588>:	call   0x5555555551d0 <_ZNSaIcED1Ev@plt>
   0x00005555555556a7 <+593>:	cmp    WORD PTR [rbp-0x4b2],0x0

<SNIP>

   0x0000555555555761 <+779>:	mov    rbx,QWORD PTR [rbp-0x8]
   0x0000555555555765 <+783>:	leave  
   0x0000555555555766 <+784>:	ret    
End of assembler dump.
```

This reveals several call instructions that point to addresses containing strings. They appear to be sections of a SQL connection string, but the sections are not in order, and the endianness entails that the string text is reversed. Endianness defines the order that the bytes are read in different architectures. Further down the function, we see a call to SQLDriverConnect.

Code: assembly

```assembly
   0x00005555555555ff <+425>:	mov    esi,0x0
   0x0000555555555604 <+430>:	mov    rdi,rax
   0x0000555555555607 <+433>:	call   0x5555555551b0 <SQLDriverConnect@plt>
   0x000055555555560c <+438>:	add    rsp,0x10
   0x0000555555555610 <+442>:	mov    WORD PTR [rbp-0x4b4],ax
```

Adding a breakpoint at this address and running the program once again, reveals a SQL connection string in the RDX register address, containing the credentials for a local database instance.

Code: assembly

```assembly
gdb-peda$ b *0x5555555551b0

Breakpoint 1 at 0x5555555551b0


gdb-peda$ run

Starting program: /htb/rollout/octopus_checker 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Program had started..
Attempting Connection 
[----------------------------------registers-----------------------------------]
RAX: 0x55555556c4f0 --> 0x4b5a ('ZK')
RBX: 0x0 
RCX: 0xfffffffd 
RDX: 0x7fffffffda70 ("DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost, 1401;UID=username;PWD=password;")
RSI: 0x0 
RDI: 0x55555556c4f0 --> 0x4b5a ('ZK')

<SNIP>
```

Apart from trying to connect to the MS SQL service, penetration testers can also check if the password is reusable from users of the same network.

---

## DLL File Examination

A DLL file is a `Dynamically Linked Library` and it contains code that is called from other programs while they are running. The `MultimasterAPI.dll` binary is found on a remote machine during the enumeration process. Examination of the file reveals that this is a .Net assembly.

  Attacking Applications Connecting to Services

```powershell-session
C:\> Get-FileMetaData .\MultimasterAPI.dll

<SNIP>
M .NETFramework,Version=v4.6.1 TFrameworkDisplayName.NET Framework 4.6.1    api/getColleagues        ! htt
p://localhost:8081*POST         Ò^         øJ  ø,  RSDSœ»¡ÍuqœK£"Y¿bˆ   C:\Users\Hazard\Desktop\Stuff\Multimast
<SNIP>
```

Using the debugger and .NET assembly editor [dnSpy](https://github.com/0xd4d/dnSpy), we can view the source code directly. This tool allows reading, editing, and debugging the source code of a .NET assembly (C# and Visual Basic). Inspection of `MultimasterAPI.Controllers` -> `ColleagueController` reveals a database connection string containing the password.

![Code editor showing MultimasterAPI with methods Get and GetColleagues, including SQL connection string.](https://academy.hackthebox.com/storage/modules/113/apps_conn_to_services/dnspy_hidden.png)

Apart from trying to connect to the MS SQL service, attacks like password spraying can also be used to test the security of other services.

---
## Question 1

### "What credentials were found for the local database instance while debugging the octopus_checker binary?"

Students need to first connect to the target as `htb-student:HTB_@cademy_stdnt!` using SSH:

Code: shell

```shell
ssh htb-student@STMIP
```

  Attacking Applications Connecting to Services

```shell-session
┌─[eu-academy-1]─[10.10.14.228]─[htb-ac-594497@htb-llk3gi0m2q]─[~]
└──╼ [★]$ ssh htb-student@10.129.205.20

The authenticity of host '10.129.205.20 (10.129.205.20)' can't be established.
ECDSA key fingerprint is SHA256:YTRJC++A+0ww97kJGc5DWAsnI9iusyCE4Nt9fomhxdA.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.205.20' (ECDSA) to the list of known hosts.
htb-student@10.129.205.20's password: 
<SNIP>
htb-student@htb:~$ 
```

Then, students need to use `gdb` to debug the `octopus_checker` binary:

Code: shell

```shell
gdb ./octopus_checker
```

  Attacking Applications Connecting to Services

```shell-session
htb-student@htb:~$ gdb ./octopus_checker 

GNU gdb (Ubuntu 9.2-0ubuntu1~20.04.1) 9.2
Copyright (C) 2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./octopus_checker...
(No debugging symbols found in ./octopus_checker)
gdb-peda$ 
```

The `disassembly-flavor` command can be used to define the display style of the code prior to disassembling:

Code: shell

```shell
set disassembly-flavor intel
disas main
```

  Attacking Applications Connecting to Services

```shell-session
gdb-peda$ set disassembly-flavor intel
gdb-peda$ disas main
Dump of assembler code for function main:
   0x0000000000001456 <+0>:	endbr64 
   0x000000000000145a <+4>:	push   rbp
   0x000000000000145b <+5>:	mov    rbp,rsp
   0x000000000000145e <+8>:	push   rbx
   0x000000000000145f <+9>:	sub    rsp,0x4b8
   0x0000000000001466 <+16>:	mov    rax,QWORD PTR fs:0x28
   0x000000000000146f <+25>:	mov    QWORD PTR [rbp-0x18],rax
   0x0000000000001473 <+29>:	xor    eax,eax
   0x0000000000001475 <+31>:	lea    rsi,[rip+0xbe5]        # 0x2061
   0x000000000000147c <+38>:	lea    rdi,[rip+0x2bbd]        # 0x4040 <_ZSt4cout@@GLIBCXX_3.4>
   0x0000000000001483 <+45>:	call   0x11a0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x0000000000001488 <+50>:	mov    rdx,rax
   0x000000000000148b <+53>:	mov    rax,QWORD PTR [rip+0x2b3e]        # 0x3fd0
   0x0000000000001492 <+60>:	mov    rsi,rax
   0x0000000000001495 <+63>:	mov    rdi,rdx
   0x0000000000001498 <+66>:	call   0x11c0 <_ZNSolsEPFRSoS_E@plt>
   0x000000000000149d <+71>:	lea    rax,[rbp-0x4b0]
   0x00000000000014a4 <+78>:	mov    rdx,rax
   0x00000000000014a7 <+81>:	mov    esi,0x0
   0x00000000000014ac <+86>:	mov    edi,0x1
   0x00000000000014b1 <+91>:	call   0x1170 <SQLAllocHandle@plt>
   0x00000000000014b6 <+96>:	mov    rax,QWORD PTR [rbp-0x4b0]
   0x00000000000014bd <+103>:	mov    ecx,0x0
   0x00000000000014c2 <+108>:	mov    edx,0x3
   0x00000000000014c7 <+113>:	mov    esi,0xc8
   0x00000000000014cc <+118>:	mov    rdi,rax
   0x00000000000014cf <+121>:	call   0x1230 <SQLSetEnvAttr@plt>
   0x00000000000014d4 <+126>:	mov    rax,QWORD PTR [rbp-0x4b0]
   0x00000000000014db <+133>:	lea    rdx,[rbp-0x4a8]
   0x00000000000014e2 <+140>:	mov    rsi,rax
   0x00000000000014e5 <+143>:	mov    edi,0x2
   0x00000000000014ea <+148>:	call   0x1170 <SQLAllocHandle@plt>
--Type <RET> for more, q to quit, c to continue without paging--

```

Students need to press Return to continue debugging the binary, until they find the call to `SQLDriverConnect`:

  Attacking Applications Connecting to Services

```shell-session
   0x00000000000015f7 <+417>:	mov    r8,rsi
   0x00000000000015fa <+420>:	mov    ecx,0xfffffffd
   0x00000000000015ff <+425>:	mov    esi,0x0
   0x0000000000001604 <+430>:	mov    rdi,rax
   0x0000000000001607 <+433>:	call   0x11b0 <SQLDriverConnect@plt>
   0x000000000000160c <+438>:	add    rsp,0x10
```

Upon finding the call to `SQLDriverConnect`, students need to set the breakpoint and run it again. Note that setting the breakpoint directly on the Procedure Linkage Table will produce an error. Therefore, students need to set the breakpoint on the function. In the output, students will find the credentials `SA:N0tS3cr3t!`:

Code: shell

```shell
b SQLDriverConnect
run
```

  Attacking Applications Connecting to Services

```shell-session
gdb-peda$ b SQLDriverConnect

Breakpoint 1 at 0x11b0

gdb-peda$ run

Starting program: /home/htb-student/octopus_checker 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Program had started..
Attempting Connection 
[----------------------------------registers-----------------------------------]
RAX: 0x55555556c4f0 --> 0x4b5a ('ZK')
RBX: 0x5555555557d0 (<__libc_csu_init>:	endbr64)
RCX: 0xfffffffd 
RDX: 0x7fffffffde40 ("DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost, 1401;UID=SA;PWD=N0tS3cr3t!;")
RSI: 0x0 
RDI: 0x55555556c4f0 --> 0x4b5a ('ZK')
RBP: 0x7fffffffe2c0 --> 0x0 
RSP: 0x7fffffffdde8 --> 0x55555555560c (<main+438>:	add    rsp,0x10)
RIP: 0x7ffff7d61c20 (<SQLDriverConnect>:	push   r15)
R8 : 0x7fffffffdea0 --> 0x7ffff7d4b008 --> 0x7ffff7d45458 --> 0x7ffff7c9f7c0 (<_ZTv0_n24_NSt13basic_ostreamIwSt11char_traitsIwEED1Ev>:	endbr64)
R9 : 0x400 
R10: 0xfffffffffffff8ff 
R11: 0x246 
R12: 0x555555555240 (<_start>:	endbr64)
R13: 0x7fffffffe3b0 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x213 (CARRY parity ADJUST zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x7ffff7d61c15 <__handle_attr_extensions_cs+149>:	pop    rbp
   0x7ffff7d61c16 <__handle_attr_extensions_cs+150>:	ret    
   0x7ffff7d61c17:	nop    WORD PTR [rax+rax*1+0x0]
=> 0x7ffff7d61c20 <SQLDriverConnect>:	push   r15
   0x7ffff7d61c22 <SQLDriverConnect+2>:	push   r14
   0x7ffff7d61c24 <SQLDriverConnect+4>:	mov    r14d,ecx
   0x7ffff7d61c27 <SQLDriverConnect+7>:	push   r13
   0x7ffff7d61c29 <SQLDriverConnect+9>:	mov    r13,r8
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdde8 --> 0x55555555560c (<main+438>:	add    rsp,0x10)
0008| 0x7fffffffddf0 --> 0x7fffffffde0a --> 0xb3b000007ffff7fe 
0016| 0x7fffffffddf8 --> 0x0 
0024| 0x7fffffffde00 --> 0x7ffff7d45418 --> 0x8 
0032| 0x7fffffffde08 --> 0x7ffff7fe0197 (<_dl_fixup+215>:	mov    r8,rax)
0040| 0x7fffffffde10 --> 0x55555556b3b0 --> 0x4b59 ('YK')
0048| 0x7fffffffde18 --> 0x55555556c4f0 --> 0x4b5a ('ZK')
0056| 0x7fffffffde20 --> 0x7ffff7d4b000 --> 0x7ffff7d45430 --> 0x7ffff7c9f790 (<_ZNSt13basic_ostreamIwSt11char_traitsIwEED1Ev>:	endbr64)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, SQLDriverConnect (hdbc=0x55555556c4f0, hwnd=0x0, 
    conn_str_in=0x7fffffffde40 "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost, 1401;UID=SA;PWD=N0tS3cr3t!;", len_conn_str_in=0xfffd, 
    conn_str_out=0x7fffffffdea0 "\b\260\324\367\377\177", conn_str_out_max=0x400, ptr_conn_str_out=0x7fffffffde0a, driver_completion=0x0) at SQLDriverConnect.c:686
686	SQLDriverConnect.c: No such file or directory.
```

Answer: {hidden}