"""
This is a script to generate a YAML dictionary of
user names and hashed passwords for use in an Ansible playbook.

@author Gabriel Birke <gabriel.birke@wikimedia.de>
"""

import random, string, sys, getopt
from passlib.hash import sha512_crypt

YAML_PARENT_VARIABLE = 'user_passwords'
DEFAULT_PASSWORD_LENGTH = 12
# Unambigous chars
ALLOWED_PASSWORD_CHARS = 'abcdefghkmnoprstwxzABCDEFGHJKLMNPQRTWXY3468'
# More secure chars, but harder to type
# ALLOWED_PASSWORD_CHARS = string.ascii_letters + string.digits + '!@$%^&*+=/'

def generate_pw( length ):
    rnd = random.SystemRandom()
    return ''.join( rnd.choice(ALLOWED_PASSWORD_CHARS) for i in range(length) )

def get_username_and_password( username_str, password_length ):
    if ":" in username_str:
        username, password = username_str.split(":", 1)
    else:
        username = username_str
        password = generate_pw( password_length )
    return (username, password)

def get_users_from_stdin():
    users = []
    # TODO check if we have stdin input, otherwise return immediately
    for line in sys.stdin:
        if line.strip():
            users.append( line.strip() )
    return users

def usage():
    print("Usage: {} [-l <length>] USER1[:PASSWORD1] USER2[:PASSWORD2] USER3[:PASSWORD3] ...".format( sys.argv[0] ) )
    print "   User names can also be passed via stdin (each username:password on a separate line)"


def generate_yaml( usernames, password_length ):
    yml = "---\n{}:\n".format( YAML_PARENT_VARIABLE )
    for user in usernames:
         username, plaintext_pw = get_username_and_password( user, password_length )
         password_hash = sha512_crypt.encrypt( plaintext_pw )
         yml += "    {}: {} # {}\n".format( username, password_hash, plaintext_pw )
    return yml

def main(argv):
    try:
        opts, usernames = getopt.getopt( argv, "hl:", ["help", "length="] )
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # usernames += get_users_from_stdin()
    if len( usernames ) < 1:
        print( "You must at least give one username" )
        usage()
        sys.exit(2)

    password_length = DEFAULT_PASSWORD_LENGTH
    for opt, arg in opts:
        if (opt == '-h' or opt == '--help'):
            print( "Generate YAML file with encrypted passwords")
            usage()
            sys.exit(0)
        if (opt == '-l' or opt == '--length'):
           password_length = int(arg)
    print generate_yaml( usernames, password_length )

if __name__ == '__main__' :
    main(sys.argv[1:])
