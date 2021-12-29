import os
import time
from datetime import datetime

import random
from Crypto.Hash import SHA256

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

# generate random numbers
random_numbers_generated = []
def arbitrary() -> int:
  random_number = random.randint(1024, 2048)
  if random_number in random_numbers_generated:
    return arbitrary()
  else:
    random_numbers_generated.append(random_number)
    return random_number


class Block:   
  index = 0
  blocks = [] # will store the chain of blocks
    
  def __init__(self):
    Block.index += 1 # block's index will give us the length of the chain
    
    self.data = []
    self.date = datetime.now()    

    # each block must have a unique hash. Therefore, a unique number must be used to create the hash
    chance = arbitrary()
    self.block_hash = SHA256.new(str(chance).encode('utf-8')).hexdigest()

    if len(Block.blocks) == 0:
      self.prev_hash = None
    else:
      self.prev_hash = Block.blocks[-1].block_hash

    # a miner is randomly chosen
    miner = random.choice(Miners.miners_list)   
    print("the miner is {}".format(miner.name))
    
    special_hash = SHA256.new(str(chance+random.randint(2048, 6114)).encode('utf-8'))
    miner.mine_block(self, special_hash.hexdigest())


class Miners:
  miners_list = [] # will contain objects
  
  def __init__(self, miner_name:str):
    self.name = miner_name
    Miners.miners_list.append(self)

  def mine_block(self, the_block, special_hash, char_length:int=2) -> None:
    """
     - will be mined if the char_length of the hash being generated is the same as char_length of special_hash
     - this should be implemented using multi-threading if multiple people desire to do the mining
    """
    number = 0
    h = SHA256.new(str(number).encode('utf-8'))
    start_time = time.time()
    
    while h.hexdigest()[:char_length] != special_hash[0:char_length]:
      number += 1
      h = SHA256.new(str(number).encode('utf-8'))
    print("--- %s seconds ---" % (time.time() - start_time))
    Block.blocks.append(the_block)

    return None


class Ledger:
  index = 0  
  def __init__(self, sender:str, recipient:str, amount:float, sign):

      Ledger.index += 1
      self.position = Ledger.index
      
      self.amount, self.sign = amount, sign
      self.sender, self.recipient = sender, recipient
      
      # the data with the sender, reciever and the trasnsaction amount
      dictionary = {self.position:{'sender':self.sender, 'recipient':self.recipient, 'amount':self.amount, 'sign':self.sign}}

      Block()
      Block.blocks[-1].data.append(dictionary)


class User:
    users      = [] #contains name of every user
    all_public = dict() #contains public key of each user so that it can be shared
        
    def __init__(self, cust_name, password):      
      self.data = Block.blocks
      
      self.cust_name = cust_name
      self.password  = password

      try:
        os.makedirs(f'../keys/{self.cust_name}')
      except FileExistsError:
        pass

      key = RSA.generate(arbitrary())

      self.private_key = key.export_key('PEM')
      self.public_key  = key.publickey().exportKey('PEM')

      start_time = time.time()

      f = open(f'../keys/{self.cust_name}/private_keyfile.pem', 'wb')
      f.write(self.private_key) # private key generation and storation
      f.close()

      f = open(f'../keys/{self.cust_name}/public_keyfile.pem', 'wb')
      f.write(self.public_key) # public key generation and storation
      f.close()
      
      print("--- %s seconds ---" % (time.time() - start_time))

      # store the data in class-variable
      User.users.append(self.cust_name)
      User.all_public[cust_name]=self.public_key

    def add_ledger_request(self, obj_recipient:object, amount:float, key, message:bytes=b'To be signed') -> None: 
      if RSA.import_key(self.private_key) == key:     
        sign = self.generate_signature(message, key)
        
        if self.verify_request(obj_recipient, self.cust_name, message, sign, amount):
          Ledger(self.cust_name, obj_recipient.cust_name, amount, sign)
        else:
          print("Verification Error")
    
    def verify_request(self, obj_recipient:object, sender, message:bytes, sign:bytes, amount:float) -> bool:
      print("The amount sent is : {} and the sender is : {}".format(amount, sender))

      password = input("Enter your password : ")
      if password == obj_recipient.password:
      
        # this might be unnecessary
        try:
          key = RSA.import_key(obj_recipient.all_public[self.cust_name])
          h = SHA256.new(message)
          pkcs1_15.new(key).verify(h, sign)
          print ("The signature is valid.")
          return True
        except (ValueError, TypeError):
          print ("The signature is not valid.")
          return False
      
      else:
        print("Wrong Password")
          
    def generate_signature(self, message, key):
      h = SHA256.new(message)
      signature = pkcs1_15.new(key).sign(h)   
      return signature
