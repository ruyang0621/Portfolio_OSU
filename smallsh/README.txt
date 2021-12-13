Discription: 
The program creates a shell in C. It implements the following subset of features of well-known shells (such as bash). 

1.Provide a prompt for running commands.

2.Handle blank lines and comments.

3.Provide expansion for the variable $$. 

4.Execute 3 built in commands exit, cd, and status.

5. Execute other commands by creating new processes using a function from the exec family. 
6. Support input and output redirection. 
7. Support running commands in foreground and background processes 
8. Implement custom handlers for SGINT and SIGTSTP.

Compile Instruction:
gcc --std=gnu99 -o smallsh main.c

General Syntax of a command line is: 
command [arg1 arg2 ...] [< input_file] [> output_file] [&]
