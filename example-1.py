import hashlib

class ExampleCoinBlock:
	def __init__(self, previous_block_hash, transaction_list):
		self.previous_block_hash = previous_block_hash
		self.transaction_list = transaction_list
		self.block_data = f"{'-'.join(transaction_list)}-{previous_block_hash}"
		self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

t1 = "Mekan 2 EC Arzuwa iberdi"
t2 = "Selbi 1.2 EC Mekana iberdi"
t3 = "Arzuw 5 EC Mekana iberdi"
t4 = "Mekan 4.2 EC Selba iberdi"

initial_block = ExampleCoinBlock("Intial Data", [t1,t2])
print(initial_block.block_data)
print(initial_block.block_hash)