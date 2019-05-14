from factom import Factomd, FactomWalletd, exceptions #python Factom API
import settings
import sys

# Specify RPC credentials so you can utilize Factom:
fct_address = settings.FCT_ADDRESS
ec_address = settings.EC_ADDRESS

factomd = Factomd(
    host='http://your_ip_address:8088',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
)

walletd = FactomWalletd(
    host='http://your_ip_address:8089',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
)
##### The Main function. The series of functions executed when you run the program from the command line
if __name__ == '__main__':

    USER_ID = sys.argv[1:] #the User Id for the twitter account you would like to follow, passed as argument from command line when you run the program
    user = USER_ID[0] #Takes the User ID you passed and isolates the variable so no longer a list variable

    resp = walletd.new_chain(factomd, 
                            [ 'TwitterBank Record',str(user)],
                            'This is the start of this users TwitterBank Records', 
                            ec_address=ec_address) # starts chain on the factom testnet
                    
    print('Chain Successfully Created for Twitter User ' + str(user) + '!' )
    print(resp)