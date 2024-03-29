#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  
#  
#  Copyright 2021 mRuggi <mRuggi@PC>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from stellar_sdk import Keypair,Server,Network,TransactionBuilder
import base64
from math import ceil
import requests

data=open("nameoftheimage.png","rb").read() #open the file (binary read) the image should be of low dimension
b64=base64.b64encode(data) #encode it into base 64 string binary

b64str=str(b64)[2:] #convert into a normal string removing b'
print(b64str) #print it
numdivide=ceil((len(b64str))/128) #every manage data has 2 64bit entry
numop=numdivide+ceil(numdivide*2/128) #foreach manage data op we add 2 indexing chars

keypair=Keypair.from_secret("YOURSECRET")
print(keypair.public_key)
print()
server = Server(horizon_url="https://horizon-testnet.stellar.org")

#JUST TO SHOW OFF THE ACTUAL SPLIT
for i in range(numop):
	if(i>=0 and i<=9): print("0"+str(i)+b64str[i*62+i*64:(i+1)*62+i*64])
	else: print(str(i)+b64str[i*62+i*64:(i+1)*62+i*64])
	print(b64str[(i+1)*62+i*64:(i+1)*62+(i+1)*64])
	print()
	
tx= (
	TransactionBuilder(
		source_account = server.load_account(account_id=keypair.public_key), 
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=10000) 	
)

for i in range(numop):
	if(i>=0 and i<=9): tx.append_manage_data_op("0"+str(i)+b64str[i*62+i*64:(i+1)*62+i*64],b64str[(i+1)*62+i*64:(i+1)*62+(i+1)*64])
	else: tx.append_manage_data_op(str(i)+b64str[i*62+i*64:(i+1)*62+i*64],b64str[(i+1)*62+i*64:(i+1)*62+(i+1)*64])
	
txtosign=tx.build()
txtosign.sign(keypair)
response = server.submit_transaction(txtosign)
print("\nTransaction hash: {}".format(response["hash"]))
print("Premi un tasto per continuare")
input()
