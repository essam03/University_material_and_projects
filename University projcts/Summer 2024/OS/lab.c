#include <stdio.h>
#include<time.h>
#include<stdlib.h>
#include<pthread.h>
#include<unistd.h>

int num;
#define num_of_threads 2

void *thread1(void* num){
  int val=*(int*)num;
for(int i=0;i<51;i++){
  if(i==val){
    printf("I foundd it I'am thread number 1 the num is %d and num of attempts is %d",*(int*)num,i);
    pthread_exit(0);
  }
 
  
}
pthread_exit(0);
}

void *thread2(void*num){
    int val=*(int*)num;
for(int i=51;i<101;i++){
  if(i==val){
    printf("I foundd it I'am thread number 2 the num is %d and num of attempts is %d",*(int*)num,i);
    pthread_exit(0);
  }
  
  
}
pthread_exit(0);
}

int main(){
  srand(time(NULL));
  num=rand()%100+1;
  pthread_t tree[num_of_threads];
  
  pthread_create(&tree[0],NULL,thread1,&num);
  pthread_create(&tree[1],NULL,thread2,&num);
  

  for(int i=0;i<num_of_threads;i++)
    pthread_join(tree[i],NULL);

return 0;
} 