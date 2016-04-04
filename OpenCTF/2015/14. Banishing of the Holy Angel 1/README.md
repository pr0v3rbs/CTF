#Banishing of the Holy Angel 1
**Category:** exploitation, binary, reversing, pwnable
**Point:** 200
**Description:**

> blackSmoke has a guardian angel, can you break it?
> (this uses the blackSmoke binary: 172.16.18.20/blackSmoke_client88bcc83690f2ce195fc92a9c20f1af27)
> (There are two keys to be obtained in banishing. The easier one to acquire goes here)

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
int holyAngel(int a1)
{
  size_t n;
  int fd;
  int v4;
  int v5;
  void *s;
  size_t len;
  int buf;
  struct sockaddr addr;
  int v10;

  v10 = *MK_FP(__GS__, 20);
  buf = 1397967938;
  len = 2048;
  printf("loading drm system");
  putchar(46);
  s = mmap(0, 0x800u, 7, 34, -1, 0);
  putchar(46);
  memset(s, 0, 0x800u);
  putchar(46);
  fd = socket(2, 1, 0);
  memset(&addr, 0, 0x10u);
  addr.sa_family = 2;
  *(_DWORD *)&addr.sa_data[2] = inet_addr("10.0.66.77");
  *(_WORD *)&addr.sa_data[0] = htons(11113u);
  if ( connect(fd, &addr, 0x10u) )
  {
    puts("Network error!");
    exit(-1);
  }
  send(fd, &buf, 4u, 0);
  if ( !recv(fd, &n, 4u, 0) )
  {
    puts("\nHoly Angel header Download error!");
    exit(-1);
  }
  putchar(46);
  n = (n >> 8) & 0xFF00 | (n << 8) & 0xFF0000 | ((unsigned __int64)n >> 24) | (n << 24);
  v4 = recv(fd, s, n, 0);
  if ( v4 != n )
  {
    puts("\nHoly Angel Download error!");
    printf("Incomplete size %d when expecting %lu\n", v4, n);
    exit(-1);
  }
  puts("Holy Angel activated!");
  v5 = fork();
  if ( v5 )
  {
    close(**(_DWORD **)a1);
    close(*(_DWORD *)(*(_DWORD *)(a1 + 4) + 4));
    ((void (*)(const char *, ...))s)((const char *)dlopen, dlsym, dlerror, dlclose, a1, v5);	// run 'Holy Angel' code received from the server
    sleep(1u);
    exit(0);
  }
  close(**(_DWORD **)(a1 + 4));
  close(*(_DWORD *)(*(_DWORD *)a1 + 4));
  return *MK_FP(__GS__, 20) ^ v10;
}
```

I found that program run 'Holy Angel' code received from the server in holyAngel().

I modified 'if ( v5 )' code to debbuging 'Holy Angel' code.

I could see what 'Holy Angel' code have concatenate a 'deKebra', 'YUhackM', 'ahwarde', 'nlikeSHYYT' strings. And result string was the flag.

The flag is `deKebraYUhackMahwardenlikeSHYYT`