#blackSmoke - highLow
**Category:** exploitation, binary, reversing, pwnable
**Point:** 300
**Description:**

> can you play and win 100% a simple casino game? NO CHEATING - 172.16.18.20/blackSmoke_client88bcc83690f2ce195fc92a9c20f1af27

##Write-up

blackSmoke binary is the program that run code received from the server.

When I decompiled the binary, main function code was same with below.

```c
int main(int argc, const char **argv, const char **envp)
{
  int result;
  int v4;
  int v5;
  int v6;
  int *v7;
  int *v8;
  int v9;
  int v10;

  v10 = *MK_FP(__GS__, 20);
  pipe(&v5);
  pipe(&v6);
  v7 = &v5;
  v8 = &v6;
  puts("blackSmoke_client v1.4");
  antidebugging((int)envp);
  holyAngel((int)&v7);
  puts("pulling down a list of games available");
  loadGame((int)&v7, "GETGAMES\n");
  fgets((char *)&v9, 1024, _bss_start);
  loadGame((int)&v7, (const char *)&v9);
  sleep(1u);
  result = 0;
  v4 = *MK_FP(__GS__, 20) ^ v10;
  return result;
}
```

main function had a antidebugging function, and I overwrote it 'nop' for debugging.

```c
int loadGame(int a1, const char *a2)
{
  size_t v2;
  size_t buf;
  int fd;
  int v6;
  void *s;
  size_t len;
  struct sockaddr addr;
  int v10;

  v10 = *MK_FP(__GS__, 20);
  v6 = 0;
  buf = 0;
  len = 2048;
  putchar(46);
  s = mmap(0, 0x800u, 7, 34, -1, 0);
  putchar(46);
  memset(s, 0, 0x800u);
  putchar(46);
  fd = socket(2, 1, 0);
  memset(&addr, 0, 0x10u);
  addr.sa_family = 2;
  *(_DWORD *)&addr.sa_data[2] = inet_addr("10.0.66.76");
  *(_WORD *)&addr.sa_data[0] = htons(11112u);
  if ( connect(fd, &addr, 0x10u) )
  {
    puts("Network error!");
  }
  else
  {
    v2 = strlen(a2);
    send(fd, a2, v2, 0);
    if ( recv(fd, &buf, 4u, 0) )
    {
      putchar(46);
      buf = (buf >> 8) & 0xFF00 | (buf << 8) & 0xFF0000 | ((unsigned __int64)buf >> 24) | (buf << 24);
      printf("Got size %lu...", buf);
      v6 = recv(fd, s, buf, 0);
      if ( v6 == buf )
      {
        close(fd);
        printf("done");
        putchar(46);
        ((void (*)(const char *, ...))s)((const char *)dlopen, dlsym, dlerror, dlclose, a1);	// run code received from the server
        puts(".");
        munmap(s, len);
      }
      else
      {
        puts("\nGame Download error!");
        printf("Incomplete size %d when expecting %lu\n", v6, buf);
      }
    }
    else
    {
      puts("\nGame Download error!");
    }
  }
  return *MK_FP(__GS__, 20) ^ v10;
}
```

I found that program run code received from the server in loadGame().

I found that 'highLow' game code when the loadGame() was second called.

highLow is the simple game that to get point by compare the two card. (current top and next top)

If correct all 100 round, then get the flag.

Specially I had find score check assembly in gamecode.

```Assembly
0xb7fd8cb1:	call   eax
0xb7fd8cb3:	jmp    0xb7fd8cc6
0xb7fd8cb5:	sub    DWORD PTR [ebp-0x274],0x1
0xb7fd8cbc:	mov    DWORD PTR [ebp-0x268],0x1
0xb7fd8cc6:	add    DWORD PTR [ebp-0x274],0x1
0xb7fd8ccd:	cmp    DWORD PTR [ebp-0x274],0x63	// for loop check
0xb7fd8cd4:	jle    0xb7fd8a1d
0xb7fd8cda:	cmp    DWORD PTR [ebp-0x278],0x63	// score check
0xb7fd8ce1:	jle    0xb7fd8d7d
0xb7fd8ce7:	mov    eax,DWORD PTR [ebp-0x2ac]
0xb7fd8ced:	add    eax,0x4
0xb7fd8cf0:	mov    eax,DWORD PTR [eax]
0xb7fd8cf2:	add    eax,0x4
```

I had set breakpoint on '0xb7fd8cda' address, and then modified score.

Program was printed a `The Key is : theBankIsAlwaysRight` string.

But 'theBankIsAlwaysRight' is not the real key. :(

So I captured packet when program print a string, I can find the key.

I found the key by capturing packets when program printing the string.

The flag is `theBankIsAlwaysRightButAreTheTellers`