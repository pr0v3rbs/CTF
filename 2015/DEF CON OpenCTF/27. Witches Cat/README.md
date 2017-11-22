#Witches Cat
**Category:** binary,exploitation,pwnable
**Point:** 350
**Description:**

> sand...sand everywhere

##Write-up

Simple binary.(cat naming management binary?)

It has vulnerability in parent program logic.(when check command value)

We can see the parent-program send key-string to child-program if child-program send cmd '0x41(65)'

```c
		if ((short)cmd[0] == 0x41)	// 141 line
		{
			int keyFd = open("/home/witchescat/key", 0);
			int readByte = 0;
			while (readByte <= 0x3F)
			{
				if (read(keyFd, buf + readByte, 1) != 1)
				{
					buf[readByte] = 0;
					break;
				}
				readByte++;
			}
			close(keyFd);
			WriteToPipe(pipe1[1], buf);
		}
```

Generally child-program send cmd with '\x1'(addCat), '\x2'(removeCat), '\x3'(nameCat) and '\x42'(exit) to parent-program.

```c
		if (strncmp(strAddCat, buf, strlen(strAddCat)) == 0)	// 231 line
		{
			cmd[0] = '\x1';
			WriteToPipe(pipe2[1], cmd);
			puts(ReadFromPipe(pipe1[0]));
		}
		if (strncmp(strRemoveCat, buf, strlen(strRemoveCat)) == 0)
		{
			cmd[0] = '\x2';
			WriteToPipe(pipe2[1], cmd);
			puts(ReadFromPipe(pipe1[0]));
		}
		if (strncmp(strNameCat, buf, strlen(strNameCat)) == 0)
		{
			cmd[0] = '\x3';
			WriteToPipe(pipe2[1], cmd);
			WriteToPipe(pipe2[1], ParseCatName(buf));
			puts(ReadFromPipe(pipe1[0]));
		}
		if (strncmp(strExit, buf, strlen(strExit)) == 0)
		{
			cmd[0] = '\x42';
			WriteToPipe(pipe2[1], cmd);
			break;
		}
```

But, there is a hole in parent-program.

```c
		if ((short)cmd[0] == 3)	// 127 line
		{
			read(pipe2[0], cmd, 1);	// overwrite cmd[0] value
			int temCnt;
			int bufCnt = (short)cmd[0];
			if (bufCnt <= 0x7F)
			{
				temCnt = 0;
				while (temCnt < bufCnt)
					read(pipe2[0], &gCatName[temCnt++], 1);
				gCatName[temCnt] = 0;
			}
			WriteToPipe(pipe1[1], strCatNamed);
		}
```

cmd-value can be changed when child-program send 'nameCat' cmd to parent-program by cat name length.

But buffer of cat-name is not initialize in ParseCatName() function.

```c
char* ParseCatName(char* userCmdBuf)
{
	char catName[0x98];	// not correct size.
	gIsCatNameExist = 0;
	gCatNameIdx = 0;
	for (gBufCount = 0; ; ++gBufCount)
	{
		if (gBufCount >= strlen(userCmdBuf))
			break;
		if (gIsCatNameExist == 1)
			catName[gCatNameIdx++] = userCmdBuf[gBufCount];
		else if (userCmdBuf[gBufCount] == ' ')
			gIsCatNameExist = 1;
	}

	return catName;
}
```

So catName buffer has 0x41 size sometimes. And if buffer have 0x41 size, then parent process send key-string to child process.

And there are BOF vulnerability, too.

The flag is `hur_hurr_hurr_MEOW_AAAA`