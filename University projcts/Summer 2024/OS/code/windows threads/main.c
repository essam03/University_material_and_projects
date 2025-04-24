#include <stdio.h>
#include <windows.h>
#include<unistd.h>

#define num_threads 4
#define R 100
#define C 100

int Arr[R][C];
int sum[num_threads]={0};
int s;

DWORD WINAPI test_Thread(LPVOID Param)
{
    int var=*(int*)Param;
    printf("Thread %d started\n",var);
    for(int i=var*25;i<(var+1)*25;i++)
        for(int j=0;j<C;j++)
            sum[var]+=Arr[i][j];
    printf("Thread %d Ended\n",var);
    return 0;

}

int main()
{
    for(int i=0;i<R;i++)
        for(int j=0;j<C;j++)
            Arr[i][j]=i+j;

    DWORD threadId[num_threads];
    HANDLE threadHandle[num_threads];
    int param[num_threads]={0,1,2,3};

    for(int i=0;i<num_threads;i++)
    {
        threadHandle[i]=CreateThread(NULL,0,test_Thread,&param[i],0,&threadId[i]);
        printf("Thread %d created with ID: %d\n",i,threadId[i]);
    }

    for(int i=0;i<num_threads;i++)
        WaitForSingleObject(threadHandle[i],INFINITE);

    for(int i=0;i<num_threads;i++)
        CloseHandle(threadHandle[i]);

    for(int i=0;i<num_threads;i++)
        s+=sum[i];

    printf("sum= %d\n",s);
    return 0;
}
