package src

import (
	"errors"
	"log"
	"sync"
	"time"
)

var (
	ErrInvalidPoolCapacity = errors.New("invalid Pool Capacity")
	ErrPoolAlreadyClosed   = errors.New("pool Already Closed")
)

const (
	RUNNING = 1
	STOPPED = 0
)

type Task struct {
	Handler func(v ...interface{})
	Params  []interface{}
}

type Pool struct {
	capacity uint64
	workers  uint64
	status   int64
	tasks    chan *Task
	wg       sync.WaitGroup
	sync.Mutex
}

func NewPool(capacity uint64) (*Pool, error) {
	if capacity <= 0 {
		return nil, ErrInvalidPoolCapacity
	}
	p := &Pool{
		capacity: capacity,
		status:   RUNNING,
		tasks:    make(chan *Task, capacity),
	}
	// health check
	go func() {
		p.Lock()
		defer p.Unlock()
		if p.workers == 0 && len(p.tasks) > 0 {
			p.workers++
			p.run()
		}
	}()
	return p, nil
}

func (p *Pool) Close() {
	p.Lock()
	p.status = STOPPED
	p.Unlock()
	for len(p.tasks) > 0 {
		time.Sleep(1 * time.Millisecond)
	}
	close(p.tasks)
	p.wg.Wait()
}

func (p *Pool) Put(task *Task) error {
	p.Lock()
	defer p.Unlock()
	if p.status == STOPPED {
		return ErrPoolAlreadyClosed
	} else if p.workers < p.capacity {
		p.workers++
		p.run()
	}
	p.tasks <- task
	return nil
}

func (p *Pool) run() {
	p.wg.Add(1)
	go func() {
		defer func() {
			p.Lock()
			p.workers--
			p.Unlock()
			p.wg.Done()
			if r := recover(); r != nil {
				log.Printf("Worker panic: %s\n", r)
			}
		}()
		for {
			select {
			case task, ok := <-p.tasks:
				if ok {
					task.Handler(task.Params...)
				}
			}
		}
	}()
}
