#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
	char command[1023] = "";

	char success_criteria[] = ":)";
	char user_input[100] = "";

	printf(">");
	fflush(stdout);
    scanf("%s", user_input);
    if (strcmp(user_input, success_criteria) == 0)
    {
		sprintf(command, "/bin/bash %s", argv[1]);
		system(command);
    }	
	
	return 0;
}