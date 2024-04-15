ERC20_ABI = [
    {
        "name": "Uint256",
        "size": 2,
        "type": "struct",
        "members": [
        {
            "name": "low",
            "type": "felt",
            "offset": 0
        },
        {
            "name": "high",
            "type": "felt",
            "offset": 1
        }
        ]
    },
    {
        "name": "approve",
        "type": "function",
        "inputs": [
            {
            "name": "recipient",
            "type": "felt"
            },
            {
            "name": "amount",
            "type": "Uint256"
            }
        ],
        "outputs": [
            {
            "name": "success",
            "type": "felt"
            }
        ]
    },
    {
        "name": "balanceOf",
        "type": "function",
        "inputs": [
        {
            "name": "account",
            "type": "felt"
        }
        ],
        "outputs": [
        {
            "name": "balance",
            "type": "Uint256"
        }
        ],
        "stateMutability": "view"
    },
    {
        "name": "transfer",
        "type": "function",
        "inputs": [
            {
            "name": "recipient",
            "type": "felt"
            },
            {
            "name": "amount",
            "type": "Uint256"
            }
        ],
        "outputs": [
            {
            "name": "success",
            "type": "felt"
            }
        ]
    },
]

TEST_abi = [
    {
      "type": "constructor",
      "name": "constructor",
      "inputs": []
    },
    {
      "type": "function",
      "name": "test",
      "inputs": [],
      "outputs": [],
      "state_mutability": "view"
    },
    {
      "type": "event",
      "name": "argent::argent::ArgentAccount::Event",
      "kind": "enum",
      "variants": []
    }
]