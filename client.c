#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
 
int main(void)
{
  int sockfd = 0,n = 0;
  char recvBuff[1024];
  struct sockaddr_in serv_addr;

	struct hostent *hp;
	hp = gethostbyname("server.sarah.cs164");
	printf("IP for server.sarah.cs164: %s\n", inet_ntoa(*(struct in_addr*)hp->h_addr_list[0]));
//int	hp_addr = inet_ntoa(*(struct in_addr*)hp->h_addr_list[0]);
char inputstr[100];
printf("Enter 'Hi' or 'Bye' to send to the server:");
scanf("%s", inputstr);

 
  memset(recvBuff, '0' ,sizeof(recvBuff));
  if((sockfd = socket(AF_INET, SOCK_STREAM, 0))< 0)
    {
      printf("\n Error : Could not create socket \n");
      return 1;
    }
 


  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(5000);
//  serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
 serv_addr.sin_addr.s_addr = inet_addr(inet_ntoa(*(struct in_addr*)hp->h_addr));
  if(connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr))<0)
    {
      printf("\n Error : Connect Failed \n");
      return 1;
    }
 
printf("Sending: %s\n", inputstr);
send(sockfd, inputstr, strlen(inputstr),0);
printf("Sent.\n");

  while((n = read(sockfd, recvBuff, sizeof(recvBuff)-1)) > 0)
    {
      recvBuff[n] = 0;
      if(fputs(recvBuff, stdout) == EOF)
    {
      printf("\n Error : Fputs error");
    }
	
//	printf("From server: %s\n", recvBuff);
//printf("%s\n", recvBuff);
	//ADDED CODE
    //    char inputstr[10];
  //      int readin;
	
//	printf("Enter 'Hi' or 'Bye' to send to the server:\n");
    //    scanf("%s", inputstr);
        //now to send inputstr to server....
        //strcpy(recvBuff, inputstr);
  //      write(sockfd, inputstr, strlen(inputstr));
//	printf("Sent message to server\n");
//	readin = read(sockfd, recvBuff, strlen(recvBuff));
//	printf("Server says: %s\n", recvBuff);

	//read(sockfd, recvBuff, strlen(recvBuff));
	//printf("output from server: %s", recvBuff);
//char inputstr[100];
//printf("Enter 'Hi' or 'Bye' to send to the server:");
//scanf("%s\n", inputstr);
//printf("Sending: %s\n", inputstr);

      printf("\n");
    }
 
  if( n < 0)
    {
      printf("\n Read Error \n");
    }
 
/*
//ADDED CODE
	char inputstr[10];
	printf("Enter 'Hi' or 'Bye' to send to the server:\n");
	scanf("%s", inputstr);
	//now to send inputstr to server....	strcpy(recvBuff, inputstr);
 */
/*char inputstr[100];
printf("Enter 'Hi' or 'Bye' to send to the server:");
scanf("%s\n", inputstr);
printf("Sending: %s\n", inputstr);
 */ return 0;
}
