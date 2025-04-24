#include <stdio.h>

int maain(){
int num=rand()%100+1;
for(int i=0;i<100;i++){
  printf("the number is %d and the attempts num is %d \n",num,i);
if(i==num){
printf("I found the number it %d and the number of attempts %d" ,num,i);
break;
num=rand()%100+1;
}
}
return 0;
} 