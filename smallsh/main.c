// Assignment 3: smallsh 
// Author: Ru Yang
// Date: 10/30/2021
/* Discription: The program creates a shell in C. It implements the following subset of features of well-known shells (such as bash). 
*               1.Provide a prompt for running commands 2.Handle blank lines and comments 3.Provide expansion for the variable $$. 
*               4.Execute 3 built in commands exit, cd, and status 5. Execute other commands by creating new processes using a function
*               from the exec family. 6.Support input and output redirection 7.Support running commands in foreground and background 
*               processes 8.Implement custom handlers for SGINT and SIGTSTP.
*               General Syntax of a command line is: command [arg1 arg2 ...] [< input_file] [> output_file] [&]*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>
#include <signal.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <fcntl.h>


// Define several constants
#define MAX_INPUT 2048		// The maximum length of characters for command lines
#define MAX_ARGU 512		// The maximum of an argument
#define MAX_FILE_NAME 255	// The maximum of a file name


// Struct used to store all the different elements included in a command.
typedef struct userInput {
	char* command;		// Store the command
	char** arguments;	// Store the command and arguments(pass to exec)
	char* inputFile;	// Store the input file name
	char* outputFile;	// Store the output file name
	bool background;	// Use to check if running at background
	int argCount;       // Use to count arguments.
}userInput;


// Struct used linked list to store all the IDs of background running process.
typedef struct bgRunningProcess {
	pid_t pid;
	struct bgRunningProcess* next;
}bgRunningProcess;


// Function Prototypes
void handle_SIGTSTP(int signo);
struct userInput* getCommand(void);
void expansionVariable$$(char** arguments, int index);
void changeDirect(char** arguments);
void printStatus(void);
void freeInputStruct(struct userInput* parsedInput);
void checkBgProcess(struct bgRunningProcess* backgroundList);
void execOtherCmd(struct userInput* parsedInput, struct bgRunningProcess* backgroundList, struct sigaction SIGINT_action, struct sigaction SIGTSTP_action);
void inputRedir(struct userInput* parsedInput);
void outputRedir(struct userInput* parsedInput);
void killProcesses(struct bgRunningProcess* backgroundList);


//Global variables
bool fgOnly = false;	// Use to check if the foreground only mode open. 
bool stopRun = false;	// Use to check if stop running
int fgStatus = 0;        // Store the exit status or the terminating signal of last foreground process


int main(void) {

	// Initialize SIGNIT & SIGTSTP
	struct sigaction SIGINT_action = {{0}};
	struct sigaction SIGTSTP_action = {{0}};
	
	// CTRL-C
	SIGINT_action.sa_handler = SIG_IGN;			// Set to Ignore SIGINT
	sigfillset(&SIGINT_action.sa_mask);
	SIGINT_action.sa_flags = 0;	         
	sigaction(SIGINT, &SIGINT_action, NULL);


	// CTRL-Z
	SIGTSTP_action.sa_handler = handle_SIGTSTP;	// Register handle_SIGTSTP as the signal handler
	sigfillset(&SIGTSTP_action.sa_mask);
	SIGTSTP_action.sa_flags = 0;
	sigaction(SIGTSTP, &SIGTSTP_action, NULL);

	// Create a dummy head to store a list of background running processes.
	struct bgRunningProcess* backgroundList = malloc(sizeof(struct bgRunningProcess));
	backgroundList->pid = 0;
	backgroundList->next = NULL;

	while (stopRun == false) {
		
		// Check status of background running process.
		checkBgProcess(backgroundList);

		// Prompt the user for input.
		struct userInput* parsedInput;
		parsedInput = getCommand();

		// Blank lines - ignore
		if (parsedInput->command == NULL || strcmp(parsedInput->command, "#") == 0) {
			freeInputStruct(parsedInput);
			continue;
		}

		// Command exit - exit the smallsh program
		if (strcmp(parsedInput->command, "exit") == 0) {
			stopRun = true;
		}
		// Command cd - change the directory
		else if (strcmp(parsedInput->command, "cd") == 0) {
			// Call the changeDirect function.
			changeDirect(parsedInput->arguments);
		}
		// Command status - print out status.
		else if (strcmp(parsedInput->command, "status") == 0) {
			// Call the print status function.
			printStatus();
		}
		//Executing other commands
		else {
			// Append NULL to parsedInput->arguments list.
			parsedInput->arguments[parsedInput->argCount] = NULL;
			parsedInput->argCount++;
			execOtherCmd(parsedInput, backgroundList, SIGINT_action, SIGTSTP_action);
		}
		freeInputStruct(parsedInput);
	}
	// Kill all processes.
	killProcesses(backgroundList);
	// Free the dummy head of background process list.
	free(backgroundList);
	return 0;
}


/* Prompt user for a command line input then parse it and return a command struct.
 * Arguments will be stored into the arguments in the struct.
 * The input file name will be stored into the inputFile in the struct.
 * The output file name will be stored into the outputFile in the struct.
 * The info about if running at background will be stored into the background in the struct.*/
struct userInput* getCommand(void) {
	// Print ": " as a prompt to get user input.
	printf(": ");
	fflush(stdout);
	char commandLineInput[MAX_INPUT + 1];
	fgets(commandLineInput, MAX_INPUT + 1, stdin);

	// Remove the newline character fron the input.
	commandLineInput[strcspn(commandLineInput, "\n")] = '\0';

	// Initialize a new struct for parse the input command.
	struct userInput* newInput = malloc(sizeof(struct userInput));
	newInput->command = NULL;
	newInput->arguments = malloc(MAX_ARGU * sizeof(*newInput->arguments));;
	newInput->inputFile = NULL;
	newInput->outputFile = NULL;
	newInput->background = false;
	newInput->argCount = 0;

	// Reset the memory for newInput->arguments.
	memset(newInput->arguments, 0, MAX_ARGU);

	// Parse the userInput
	char* saveptr;
	int index = 0;															// The position use to store next arg in the newInput->arguments.
	char* token = strtok_r(commandLineInput, " ", &saveptr);				// 1st token is command
	if (token) {
		newInput->command = calloc(strlen(token) + 1, sizeof(char));
		strcpy(newInput->command, token);									// Store the 1st token into command in struct. 
		newInput->arguments[0] = calloc(strlen(token) + 1, sizeof(char));
		strcpy(newInput->arguments[index], token);							// Store the 1st token into 1st postion of newInput->arguments in struct.
		newInput->argCount++;
		index++;

		token = strtok_r(NULL, " ", &saveptr);
		while (token) {
			// Check if the current token is ">" (output file).
			if (strcmp(token, ">") == 0) {
				token = strtok_r(NULL, " ", &saveptr);
				newInput->outputFile = calloc(strlen(token) + 1, sizeof(char));
				strcpy(newInput->outputFile, token);
			}
			// Check if the current token is "<" (input file).
			else if (strcmp(token, "<") == 0) {
				token = strtok_r(NULL, " ", &saveptr);
				newInput->inputFile = calloc(strlen(token) + 1, sizeof(char));
				strcpy(newInput->inputFile, token);
			}
			// The current token is command argument.
			else {
				newInput->arguments[index] = calloc((strlen(token) + 1), sizeof(char));
				strcpy(newInput->arguments[index], token);
				// Check if the arguments contain $$ (need to expand).
				if (strstr(newInput->arguments[index], "$$") != NULL) {
					expansionVariable$$(newInput->arguments, index);
				}
				index++;
				newInput->argCount++;
			}
			token = strtok_r(NULL, " ", &saveptr);
		}

		// Check if & character at the end of the input.
		if (newInput->argCount > 1) {
			if (strcmp(newInput->arguments[newInput->argCount - 1], "&") == 0) {
				// if &, set background in the newInput struct to 1.
				newInput->background = true;
				free(newInput->arguments[newInput->argCount - 1]);				// Free the memory used to store &.
				newInput->argCount--;											// Decrease the argCount in the newInput struct.
			}
		}
	}
	return newInput;
}


/* The function is used to expansion of variable $$ in a argument
 * into the process ID of the smallsh itself. Input index is the
 * index of the argument in the arguments array.*/
void expansionVariable$$(char** arguments, int index) {
	// Find the process ID and convert it to string.
	pid_t pid = getpid();
	int pidLength = snprintf(NULL, 0, "%d", pid);
	char* pidStr = malloc(pidLength + 1);
	sprintf(pidStr, "%d", pid);

	char* argExpanded;									// Use to store the command after expansion
	int argLength = strlen(arguments[index]);			// The length of origin command
	int count = 0;                                      // Number of replacements

	// Count the number of $$ need to be replaced.
	for (int i = 0; arguments[index][i + 1]; i++) {
		if (arguments[index][i] == '$' && arguments[index][i + 1] == '$') {
			count++;
			i++;
		}
	}

	// Allocate memory to argExpanded according to length.
	int argExpandedLen = argLength + (pidLength - 2) * count;
	argExpanded = malloc((argExpandedLen + 1)*sizeof(char));
	memset(argExpanded, 0, argExpandedLen + 1);
	int i;		// index used to go through origin comment
	int j = 0;  // Point to next storage position in argExpanded 
	// Iterate through the origin commend.
	for (i = 0; arguments[index][i + 1]; i++) {
		// If $$ found, append pidStr to the end of argExpanded.
		if (arguments[index][i] == '$' && arguments[index][i + 1] == '$') {
			argExpanded = strcat(argExpanded,pidStr);
			j += pidLength;		// move j steps of pidLength to next storage position.
			i++;
		}
		else {
			// If no $$ found, store the current value point by i in origin commend into argExpanded.
			argExpanded[j] = arguments[index][i];
			j++;	// move one step to next storage position.
		}
	}
	// Check if the last char in origin commend has been added into argExpanded.
	if (j < argExpandedLen) {
		argExpanded[j] = arguments[index][i];
	}
	free(arguments[index]);												// Free the memory of origin commend.
	arguments[index] = malloc(sizeof(char) * (argExpandedLen + 1));		// Allocate new memory with size of argExpandedLen + 1.
	arguments[index] = strdup(argExpanded);								// Copy commend after expanded into the arguments array.

	// Free memory not used.
	free(pidStr);
	free(argExpanded);
}


/* The function is used to catch the SIGTSTP signal.
 * And turn on or off the foreground only mode. */
void handle_SIGTSTP(int signo) {
	// If foreground only mode is not open, turn it on.
	if (fgOnly == false) {
		char* msg = "Entering foreground-only mode (& is now ignored)\n";
		write(STDOUT_FILENO, msg, 50);
		fflush(stdout);
		fgOnly = true;
	}
	// If foreground only mode is open, turn it off.
	else {
		char* msg = "Exiting foreground-only mode\n";
		write(STDOUT_FILENO, msg, 30);
		fflush(stdout);
		fgOnly = false;
	}
}


/* The funcion is used to change the working directory of smallsh.
 * When the first argument is cd, the function will be called.
 * If the directory is specified, it will be store in the second argument.*/
void changeDirect(char** arguments) {
	// If the directory is not specified.
	if (arguments[1] == 0) {
		chdir(getenv("HOME"));
	}
	// If the directory is specified.
	else {
		int result = chdir(arguments[1]);
		// If no such directory print the error msg.
		if (result == -1) {
			printf("No such file or directory.\n");
			fflush(stdout);
		}
	}
}


/* The function is used to print out either the exit status or
 * the terminating signal of the last foreground process run by
 * the smallsh. fgStatus is global variable.*/
void printStatus(void) {
	// If terminated normally.
	if (WIFEXITED(fgStatus)) {
		printf("exit value %d\n", WEXITSTATUS(fgStatus));
	}
	// If terminated abnormally.
	else if (WIFSIGNALED(fgStatus)) {
		printf("termination signal %d\n", WTERMSIG(fgStatus));
	}
	fflush(stdout);
}


/* Check on the background processes. It take a list of background Process.
 * The list start with a dummy head. If the process is complete remove PID
 * from the list then print the exit status or the terminating signal.*/
void checkBgProcess(struct bgRunningProcess* bgProcessList) {
	pid_t childPid;
	int childStatus;

	// the list contain at least one background process.
	if (bgProcessList->next != NULL) {
		struct bgRunningProcess* prevPointer = bgProcessList;
		struct bgRunningProcess* currPointer = prevPointer->next;
		// Go through the list.
		while (currPointer != NULL) {
			childPid = waitpid(currPointer->pid, &childStatus, WNOHANG);

			// Check if the child process is complete
			if (childPid == currPointer->pid) {
				//remove PID from the list of background process.
				struct bgRunningProcess* tempPointer = currPointer;
				currPointer = currPointer->next;
				prevPointer->next = currPointer;
				free(tempPointer);

				// If terminated normally. Print the pid and exit status.
				if (WIFEXITED(childStatus)) {
					printf("background pid %d is done: exit value %d\n", childPid, WEXITSTATUS(childStatus));
				}
				// If terminated abnormally. Print the terminate signal.
				else {
					printf("background pid %d is done: terminated by signal %d\n", childPid, WTERMSIG(childStatus));
				}
				fflush(stdout);

			}
			else {
				prevPointer = currPointer;		// Move prevPointer to next
				currPointer = currPointer->next;	// Move currPoint to next
			}
		}
	}
}

/*Execute the non-built-in command.*/
void execOtherCmd(struct userInput* parsedInput, struct bgRunningProcess* backgroundList, struct sigaction SIGINT_action, struct sigaction SIGTSTP_action) {
	int childStatus;
	pid_t childPid = fork();

	/* Foreground only mode is offand the process is set to run in background.
	 * Add it PID to the list of background running process.*/
	if (parsedInput->background && !fgOnly) {
		// Create new node for this new background process.
		struct bgRunningProcess* newBgProcess = malloc(sizeof(struct bgRunningProcess));
		newBgProcess->pid = childPid;
		newBgProcess->next = NULL;

		// Find the position to add the new node.
		struct bgRunningProcess* temp = backgroundList;
		while (temp->next != NULL) {
			temp = temp->next;
		}
		temp->next = newBgProcess;
	}
	switch (childPid) {
		case -1:
			perror("fork() failed!");
			exit(1);
			break;
		case 0:
			/* If the child process running as a foreground.
			 * Set to receive the signal SIGINT.*/
			if (!parsedInput->background || fgOnly) {
				SIGINT_action.sa_handler = SIG_DFL;
				sigaction(SIGINT, &SIGINT_action, NULL);
			}

			/* A child process ignore SIGTSTP.
			 * Set to ignore the signal SIGTSTP*/
			SIGTSTP_action.sa_handler = SIG_IGN;
			sigaction(SIGTSTP, &SIGTSTP_action, NULL);

			// Redirect input and output.
			inputRedir(parsedInput);
			outputRedir(parsedInput);
			
			// Use exec() to run the command.
			execvp(parsedInput->arguments[0], parsedInput->arguments);
			fprintf(stderr, "%s: ", parsedInput->arguments[0]);
			perror("");
			exit(1);
			break;
		default:		// The parent process
			// Child runs in background, parent does not wait.
			if(parsedInput->background && !fgOnly) {
				printf("background pid is %d\n", childPid);
				fflush(stdout);
			}
			else {
				// Child runs in foreground, parent wait.
				childPid = waitpid(childPid, &childStatus, 0);
				if (!WIFEXITED(childStatus)){
					printf("terminated by signal %d\n", WTERMSIG(childStatus));
					fflush(stdout);
				}
				fgStatus = childStatus;
			}
			break;
	}	
}


// Input Redirection
void inputRedir(struct userInput* parsedInput) {
	// If the inputFile was specified.
	if (parsedInput->inputFile) {
		// Open the file according to user input.
		int input = open(parsedInput->inputFile, O_RDONLY);
		if (input == -1) {
			printf("cannot open %s for input\n", parsedInput->inputFile);
			fflush(stdout);
			exit(1);
		}
		// Redirect the input to input file.
		int result = dup2(input, 0);
		if (result == -1) {
			printf("Fail to redirect the input to input file\n");
			fflush(stdout);
			exit(1);
		}
	}
	/* If the process running at the backgroundand
	 * and the inputFile was not specified, redirect
	 * the stdin to /dev/null.*/
	else {
		if (!fgOnly && parsedInput->background) {
			int input = open("/dev/null", O_RDONLY);
			if (input == -1) {
				printf("cannot open /dev/null for input\n");
				fflush(stdout);
				exit(1);
			}
			int result = dup2(input, 0);
			if (result == -1) {
				printf("Fail to redirect the input to /dev/null\n");
				fflush(stdout);
				exit(1);
			}
		}
	}
}

// Output redirection
void outputRedir(struct userInput* parsedInput) {
	// If the outputFile was specified.
	if (parsedInput->outputFile) {
		// Open the file according to user input.
		int output = open(parsedInput->outputFile, O_WRONLY | O_CREAT | O_TRUNC, 0640);
		if (output == -1) {
			printf("cannot open %s for output\n", parsedInput->outputFile);
			fflush(stdout);
			exit(1);
		}
		// Redirect the output to input file.
		int result = dup2(output, 1);
		if (result == -1) {
			printf("Fail to redirect the input to output file\n");
			fflush(stdout);
			exit(1);
		}
	}
	/* If the process running at the backgroundand
	 * and the outputFile was not specified, redirect
	 * the stdout to /dev/null.*/
	else {
		if (!fgOnly && parsedInput->background) {
			int output = open("/dev/null", O_WRONLY | O_CREAT | O_TRUNC, 0640);
			if (output == -1) {
				printf("cannot open /dev/null for output\n");
				fflush(stdout);
				exit(1);
			}
			int result = dup2(output, 1);
			if (result == -1) {
				printf("Fail to redirect the output to /dev/null\n");
				fflush(stdout);
				exit(1);
			}
		}
	}
}


// Kill all background running processes.
void killProcesses(struct bgRunningProcess* backgroundList) {
	// No background process, return directly.
	if (backgroundList->next == NULL) {
		return;
	}
	// Kill all process one by one.
	int childStatus;
	struct bgRunningProcess* curr = backgroundList->next;
	struct bgRunningProcess* next = curr->next;
	while (next != NULL) {
		kill(curr->pid, SIGKILL);
		waitpid(curr->pid, &childStatus, WNOHANG);
		free(curr);
		curr = next;
		next = next->next;
	}
	// Kill the last node in background list.
	kill(curr->pid, SIGKILL);
	waitpid(curr->pid, &childStatus, WNOHANG);
	free(curr);
}


// Free struct userInput.
void freeInputStruct(struct userInput* parsedInput) {
	// Free memory allocation for parsedInput.
	if (parsedInput->command != NULL) {
		free(parsedInput->command);
		for (int i = 0; i < parsedInput->argCount; i++) {
			free(parsedInput->arguments[i]);
		}
	}
	// if inputFile specified
	if (parsedInput->inputFile != NULL) {
		free(parsedInput->inputFile);
	}
	// if outputFile specified
	if (parsedInput->outputFile != NULL) {
		free(parsedInput->outputFile);
	}
	free(parsedInput->arguments);
	free(parsedInput);
}
