from golang:alpine
copy . /go/src/app
workdir /go/src/app
run go build -o helloworld
expose 6111
cmd ["./helloworld"]