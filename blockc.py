import hashlib
import time
import json

class Block:
    def __init__(self, index, transactions, previous_hash, difficulty=4):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = self.mine_block()
    
    def calculate_hash(self):
        block_content = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_content).hexdigest()
    
    def mine_block(self):
        """ Implements a simple Proof-of-Work by finding a hash with leading zeros based on difficulty """
        while True:
            hash_value = self.calculate_hash()
            if hash_value[:self.difficulty] == '0' * self.difficulty:
                return hash_value
            self.nonce += 1

class Blockchain:
    def __init__(self, difficulty=4):
        self.difficulty = difficulty  # Ensure difficulty is set before calling create_genesis_block
        self.chain = [self.create_genesis_block()]
    
    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0", self.difficulty)
    
    def add_block(self, transactions):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), transactions, previous_block.hash, self.difficulty)
        self.chain.append(new_block)
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def tamper_with_block(self, index, new_transactions):
        if 0 < index < len(self.chain):
            self.chain[index].transactions = new_transactions
            self.chain[index].hash = self.chain[index].calculate_hash()
        else:
            print("Invalid block index to tamper.")
    
    def print_chain(self):
        for block in self.chain:
            print(json.dumps({
                'index': block.index,
                'timestamp': block.timestamp,
                'transactions': block.transactions,
                'previous_hash': block.previous_hash,
                'hash': block.hash
            }, indent=4))
            print('-' * 50)

# Example Usage
blockchain = Blockchain(difficulty=3)
blockchain.add_block(["Alice pays Bob 10 BTC"])
blockchain.add_block(["Bob pays Charlie 5 BTC"])

print("Initial Blockchain:")
blockchain.print_chain()
print("Blockchain Validity:", blockchain.is_chain_valid())

# Tampering with a block
tamper_index = 1
blockchain.tamper_with_block(tamper_index, ["Alice pays Eve 100 BTC"])

print("\nTampered Blockchain:")
blockchain.print_chain()
print("Blockchain Validity After Tampering:", blockchain.is_chain_valid())
