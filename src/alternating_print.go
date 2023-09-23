package src

import (
	"fmt"
)

var (
	total int
	c     chan struct{}
	c1    chan struct{}
	c2    chan struct{}
)

func func1() {
	i := 1
	for {
		<-c1
		if i > total {
			c <- struct{}{}
			return
		}
		fmt.Println(fmt.Sprintf("gorountine-1: %d", i))
		i += 2
		c2 <- struct{}{}
	}
}

func func2() {
	i := 2
	for {
		<-c2
		fmt.Println(fmt.Sprintf("gorountine-2: %d", i))
		i += 2
		c1 <- struct{}{}
	}
}

func main() {
	total = 10
	c = make(chan struct{})
	c1 = make(chan struct{})
	c2 = make(chan struct{})
	go func1()
	go func2()
	c1 <- struct{}{}
	<-c
}
