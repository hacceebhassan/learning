// Including dependencies

#include <iostream>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
using namespace std;

// Main Function
int main()
{    
    int pid;
    pid = getpid();
    
    cout<<"Current Process ID is :"<<pid<<endl;

    cout<<"Forking Child Process..."<<endl; 
    
    // This will Create Child Process and Returns Child's PID */
    pid = fork(); 
    
    if (pid < 0)
    {
        // Process Creation Failure!
        exit(-1);
    }
    
    else if (pid == 0) 
    {
        // Child Process

        cout<<"Starting Child Process..."<<endl;
        cout<<"Child Process Completed !!"<<endl;
        
    }

    else 
    {
        // Parent Process

        sleep (10);
        cout<<"Running Parent Process..."<<endl;
        cout<<"--- Zombie State ---"<<endl;
        
        while(1)
        {
            // Infinite Loop

        }
    }    
    return 0;
}
