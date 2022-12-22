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
Type `q` or `Q` then click `[Enter]`


## Docker
### Build image

`docker build -t {image_name} .`

### Run container
#### Run service
`docker run -it --rm --name {app_name} {image_name}`

#### Run socket service
`docker run -it --rm --name {app_name} {image_name} --c=Client1`
#### Run pipe service
`docker run -it --rm --name {app_name} {image_name} --c=Client2`
#### Run shared memory service
`docker run -it --rm --name {app_name} {image_name} --c=Client1`

### How to quit a service in docker
Type `q` or `Q` then click `[Enter]`

## TODO
* Unit test

## Pending
The order of log generation is inconsistent, causing the input message to be disrupted by the log.