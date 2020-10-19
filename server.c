#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <netdb.h>
 
int main(void)
{
  int listenfd = 0,connfd = 0;
  
  struct sockaddr_in serv_addr;
 
  char sendBuff[1025];  
  int numrv;  
 
  listenfd = socket(AF_INET, SOCK_STREAM, 0);
  printf("socket retrieve success\n");
  
  memset(&serv_addr, '0', sizeof(serv_addr));
  memset(sendBuff, '0', sizeof(sendBuff));

      
struct hostent *hp;
hp = gethostbyname("server.sarah.cs164");

  serv_addr.sin_family = AF_INET;    
  serv_addr.sin_addr.s_addr = htonl(INADDR_ANY); 
//serv_addr.sin_addr.s_addr = inet_ntoa(*(struct in_addr*)hp->h_addr_list[0]);  
serv_addr.sin_port = htons(5000);    
 
  bind(listenfd, (struct sockaddr*)&serv_addr,sizeof(serv_addr));
  
  if(listen(listenfd, 10) == -1){
      printf("Failed to listen\n");
      return -1;
  }
  
int readin;
char hi[4] = "Hi";
char bye[4] = "Bye";
int result;
char lookstr[4];
//char recvBuffer[100];
//char test[100] = "test from server";   
 
  while(1)
    {
      connfd = accept(listenfd, (struct sockaddr*)NULL ,NULL); // accept awaiting request
	printf("Connected to server\n");
  
//      strcpy(sendBuff, "Message from server33");
//      write(connfd, sendBuff, strlen(sendBuff));
 
	readin = read(connfd, sendBuff, strlen(sendBuff));
	//printf("successfully read: %s\n",(int) sendBuff); 
	if(sendBuff[2] =='0'){//means hi
		strcpy(lookstr, "Hi");
}
	else{//means bye
		strcpy(lookstr, "Bye");
}
	
        
	if(strcmp(lookstr, hi)==0){//match
		printf("Client says Hi\n");
		strcpy(sendBuff, "Server says Hi");
		write(connfd, sendBuff, strlen(sendBuff));
	}
	if(strcmp(lookstr, bye)==0){
		printf("Client says Bye\n");
		strcpy(sendBuff, "Server says Bye");
		write(connfd, sendBuff, strlen(sendBuff));
		
	}

      close(connfd);    
      sleep(1);
    }
 
 
  return 0;
}
