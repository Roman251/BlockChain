from block_chain import *

if __name__=='__main__':
    # generate miners
    jack = Miners('Jack')
    jill = Miners('Jill')

    # generate users and privateKey & publicKey for each user
    alice = User('Alice', 'root')
    sam   = User('Sam',   'root')
    
    # load private keys of the users to make transfers
    sam_key_private   = RSA.import_key(open('../keys/sam/private_keyfile.pem').read()) 
    alice_key_private = RSA.import_key(open('../keys/alice/private_keyfile.pem').read())  

    # add ledgers
    sam.add_ledger_request(alice, 135, sam_key_private, message=b'To be signed')
    alice.add_ledger_request(sam, 300, alice_key_private, message=b'To be signed')

    # every user has the same data
    print(alice.data[0].data, sam.data[0].data)
    print(alice.data[1].data, sam.data[1].data)

    # print block hash
    print(Block.blocks[0].prev_hash, Block.blocks[0].block_hash)
    print(Block.blocks[1].prev_hash, Block.blocks[1].block_hash)

    # delete objects
    del alice, sam
    del jack, jill