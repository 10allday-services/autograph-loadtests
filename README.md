# autograph-loadtests

## Description
Loadtests for Mozilla's autograph service


## Docker 

### Prerequisites
1. A working autograph server:  https://github.com/mozilla-services/autograph
1. HAWK credentials
1. docker installation
1. Set the following environment variables: HOST, PORT, HAWK_ID, HAWK_KEY, SIGNER

### Summary
To run the autograph loadtests first build the docker image:

```
docker build -t autograph-loadtest .
```

Then execute:

```
docker run -e "HOST=$HOST" -e "PORT=$PORT" -e "HAWK_ID=$HAWK_ID" -e "HAWK_KEY=$HAWK_KEY" -e "SIGNER=$SIGNER" autograph-loadtest
```


