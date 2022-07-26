#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
	char command[1023] = "";

	sprintf(command, "/bin/bash %s", argv[1]);
	system(command);
	
	return 0;
}