import hashlib
import time
import json

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # dict: can be message, room, notification, etc.
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Sort keys for consistent hashing
        block_string = f"{self.index}{self.timestamp}{json.dumps(self.data, sort_keys=True)}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Add a type for consistency
        return Block(0, time.time(), {"type": "genesis", "message": "Genesis Block"}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), data, previous_block.hash)
        self.chain.append(new_block)

    def to_list(self):
        # For displaying in templates
        return [
            {
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "previous_hash": block.previous_hash,
                "hash": block.hash,
            }
            for block in self.chain
        ]

    def validate_chain(self):
        """
        Returns a list of tuples (index, error_message) for each invalid block.
        """
        errors = []
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            # Check previous hash
            if current.previous_hash != previous.hash:
                errors.append((i, "Previous hash does not match"))
            # Check hash validity
            if current.hash != current.calculate_hash():
                errors.append((i, "Block hash is invalid (data may have been tampered)"))
        return errors

    def tamper_block(self, index, new_data):
        """
        For demonstration: Tamper with a block's data.
        """
        if 0 < index < len(self.chain):
            self.chain[index].data = new_data
            # Do NOT recalculate hash to simulate tampering

# Singleton instance for your app
blockchain_instance = Blockchain()
