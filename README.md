# itachi-testing

## Test with Docker

### Start itachi in background before testing

```
cd /path/to/itachi
make reset && ./itachi
```

### Start testing

```
cd python
docker run --network=host -v "$(pwd)"/:/root -it python:3.12 bash
```

Then inside container:

```
cd /root
pip3 install -r requirements.txt
```

### Tests

1. Transfer funds between two accounts 10 times, with concurrent transactions (the final total balance remains the same).
   1. `multiple_trans.py`
2. One account transfers 1 ETH to another account 100 times, with the balance decreasing by 100 ETH in the end.
   1. `transfer_100_eth.py`
