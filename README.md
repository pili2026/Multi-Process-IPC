# Multi-Process-IPC
Implementation of Mean, Median, Mode Calculator using IPC

## Environment
* Ubuntu 18.04
* Python 3.10

## Execute service
Start the Mean, Median, Mode Calculator
### All service
`python app,py`

### Socket service(Mean Calculator)
`python app,py -c=Client1`

### Pipe service(Median Calculator)
`python app,py -c=Client2`

### Shared memory service(Mode Calculator)
`python app,py -c=Client3`

### How to quit a service in execution
Type `q` and click `[Enter]`

## TODO
* Unit test
* Dockerize