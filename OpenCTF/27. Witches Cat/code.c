#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int gIsCatNameExist;
char gReadBuf[0x100];
int pipe1[2];
int gBufCount;
int pipe2[2];
int gIsCatAdded;
int gCatNameIdx;
char gCatName[128];
char gStrRmResult[256];

char* GetAddCatBuf()
{
	gIsCatAdded = 1;
	return "Cat added successfully";
}

char* GetRmCatBuf()
{
	char *result;

	strcpy(gStrRmResult, "Cat removed successfully -- ");
	strcat(gStrRmResult, gCatName);

	if (gIsCatAdded == 1)
	{
		gIsCatAdded = 0;
		result = gStrRmResult;
	}
	else
	{
		result = "Cat was not removed successfully";
	}

	return result;
}

int WriteToPipe(int fd, char *buf)
{
	size_t strLen;
	size_t writeBuf;

	writeBuf = strlen(buf);
	write(fd, &writeBuf, 1);
	strLen = strlen(buf);
	return write(fd, buf, strLen);
}

char* ReadFromPipe(int fd)
{
	size_t readSize;
	read(fd, &readSize, 1);
	if (readSize > 0xff) exit(-1);
	read(fd, gReadBuf, readSize);
	return gReadBuf;
}

char* ParseCatName(char* userCmdBuf)
{
	char catName[0x98];
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

int main(int argc, const char **argv, const char **envp)
{
	gIsCatAdded = 0;

	if (pipe(pipe1) < 0)
	{
		exit(-1);
	}
	else
	{
		if (pipe(pipe2) < 0)
		{
			exit(-1);
		}
		else
		{
			if (fork() != 0)	// parent
			{
				alarm(0x64);
				close(pipe2[1]);
				close(pipe1[0]);
				char *strCatNamed = "cat successfully named!";
				char cmd[2];
				char buf[0x400];
				int currentCmd;

				while (1)
				{
					read(pipe2[0], cmd, 1);
					printf("-->master received [%08x]\n", (short)cmd[0]);
					read(pipe2[0], cmd, 1);
					printf("-->master received [%08x]\n", (short)cmd[0]);
					if ((short)cmd[0] != currentCmd)
					{
						currentCmd = (short)cmd[0];
					}
					if ((short)cmd[0] == 0x42)
					{
						exit(-1);
					}
					if ((short)cmd[0] == 1)
					{
						WriteToPipe(pipe1[1], GetAddCatBuf());
					}
					if ((short)cmd[0] == 2)
					{
						WriteToPipe(pipe1[1], GetRmCatBuf());
					}
					if ((short)cmd[0] == 3)
					{
						read(pipe2[0], cmd, 1);
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
					if ((short)cmd[0] == 0x41)
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
				}
			}
			else	// child
			{
				char buf[0x400];
				char binary[0x200000];
				char *strScoop = "scoop";
				char *strAddCat = "addCat";
				char *strRemoveCat = "removeCat";
				char *strNameCat = "nameCat";
				char *strExit = "exit";
				int binarySize;
				alarm(0x64);
				putchar(0x0a);
				close(pipe2[0]);
				close(pipe1[1]);
				int fd = open("witches_cat", 0);
				gBufCount = 0;

				while (gBufCount <= 0x1FFFFF)
				{
					if (read(fd, &binary[gBufCount], 1) != 1)
					{
						binary[gBufCount] = 0;
						binarySize = gBufCount;
						break;
					}
					gBufCount++;
				}
				if (prctl(0x16, 1, 0, 0, 0) < 0)
					exit(-1);
				int check = 0;
				char cmd[2];
				cmd[1] = 0;
				char temBuf[1];
				temBuf[0] = '\0';
				while (check == 0)
				{
					puts("\nHood kitty, here's the litterbox\n");
					puts("Commands");
					puts("\tscoop\t\t careful with this one!");
					puts("\taddCat");
					puts("\tremoveCat");
					puts("\tnameCat name");
					puts("\texit");
					printf("# ");
					fflush(stdout);
					gBufCount = 0;
					while (gBufCount <= 0x3ff)
					{
						read(0, temBuf, 1);
						if (temBuf[0] != '\xa')
						{
							buf[gBufCount] = (char)temBuf[0];
							gBufCount += 1;
						}
						else
						{
							buf[gBufCount++] = '\0';
							buf[gBufCount] = '\0';
							break;
						}
					}
					if (strncmp(strScoop, buf, strlen(strScoop)) == 0)
					{
						printf("scooping %d bytes...\n", binarySize);
						gBufCount = 0;
						while (gBufCount < binarySize)
						{
							write(1, &binary[gBufCount], 1);
							gBufCount += 1;
						}
						fflush(stdout);
					}
					if (strncmp(strAddCat, buf, strlen(strAddCat)) == 0)
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
				}
			}
		}
	}
}
