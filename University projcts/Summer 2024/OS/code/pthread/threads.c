#include<stdio.h>
#include<pthread.h>
#include<unistd.h>

#define R 100
#define C 100
#define num_threads 4

int Arr[R][C];
int sum[num_threads]={0};
int s=0;

void *runTest(void *param)
{
	int num;
	num=*(int*)param;
	printf("thread %d started\n",num);
	for(int i=num*25;i<(num+1)*25;i++)
	{
		for(int j=0;j<C;j++)
		{
			sum[num]+=Arr[i][j];
		}
	}
	
			
	printf("thread %d ended\n",num);
	pthread_exit(0);
}

int main()
{
	for(int i=0;i<R;i++)
		for(int j=0;j<C;j++)
			Arr[i][j]=i+j;
	
	pthread_t tid[num_threads];
	pthread_attr_t attr[num_threads];
	
	int T[num_threads];
	for(int i=0;i<num_threads;i++)
		T[i]=i;
	
	for(int i=0;i<num_threads;i++)
	{
		pthread_attr_init(&attr[i]);
	}
	
	for(int i=0;i<num_threads;i++)
	{
		pthread_create(&tid[i],&attr[i],runTest,&T[i]);
		printf("Thread %d created with id: %li\n",i,tid[i]);
	}
	
	for(int i=0;i<num_threads;i++)
	{
		pthread_join(tid[i],NULL);
	}
	
	for(int i=0;i<num_threads;i++)
		s+=sum[i];
	
	printf("application Terminated s= %d\n",s);
	
	return 0;
}
