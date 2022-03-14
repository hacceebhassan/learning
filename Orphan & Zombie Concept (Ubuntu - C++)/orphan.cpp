// Incuding dependencies

#include <iostream>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
using namespace std;

int main()
{    
    int pid;
    pid = getpid();
    
    cout<<"Current Process ID is : "<<pid<<endl;

    cout<<"Forking Child Process ..."<<endl;
        
    pid = fork(); //This will Create Child Process and Returns Child's PID

    if (pid < 0)
    {
        // Failure
        exit(-1);
    }
    
    else if (pid == 0) 
    {
        // Child Process

        cout<<"Child Process - Sleeping..."<<endl;
        sleep(5);

        // Orphan Child's Parent ID 

        cout<<"Orphan Child's Parent ID : "<<getppid()<<endl;
    }
    
    else 
    {
        // Parent Process

        cout<<"Parent Process Successful ..."<<endl;
    }
        
    return 0;
}
