# Securely create multiple users with Ansible

 This Python script and Ansible playbook help you to create several user accounts on different servers, give each user a secure password and force the user to change the password on first login.

The Python script `generate_user_passwords.py` creates a YAML dictionary of user names and SHA512-hashed passwords that can be used in an Ansible Playbook.

The Ansible playbook `users.yml` demonstrates how to use the generated user dictionary.

## Installation

To use this script you need to install [Ansible](http://ansible.com/) and the `passlib` Python library.

The easiest way to install Ansible is by using the package manager of your operating system. Installation instructions for the package managers or installing from source are at http://docs.ansible.com/ansible/intro_installation.html

The Passlib library can be installed with

    pip install passlib

## Generate a list of user names and passwords
Use the provided Python script `generate_user_passwords.py` to generate a dictionary of user names and secure passwords. There are several ways to specify the user names.

### User names as parameters

    python generate_user_passwords.py alice bob carol dan

### User names from stdin
User names can be piped in from a file

    python generate_user_passwords.py < users.txt

or generated with a shell command

    awk -F ';' '{print $3}' users.csv | python generate_user_passwords.py

When the user names are piped in, the script expects each name to be a on a new line. Blank lines are ignored.

### Using your own passwords
If you want to specify the passwords yourself, you can use the pattern `username:password` for each user name. The user name  will be split at the first `:` character and the second half of this user name will be used as the password.

In the following example `alice` has the password `foo`, `bob` has the password `abc:xyz`

    python generate_user_passwords.py alice:foo bob:abc:xyz

### Generated password length

You can specify the length of the generated passwords like this:

    python generate_user_passwords.py -l 8 alice bob carol dan

Default password length is 12.

### Storing the output
By default the generated YAML is printed to stdout. The generated output contains the un-hashed generated passwords as comments so you can pass them on to the users.

Example output:

```YAML
---
user_passwords:
    alice: $6$rounds=656000$m/qpgaPV9nDhZA84$0Uz2fQ7PjnX.eMIDSlw0hUetHYat.VuxIzBNsbceZjg60XMe.0hrDekRybNAMe0fPqvczikY0Hdph8KMhcHct. # ws#P)Bg)l853
    bob: $6$rounds=656000$RhhaEkZK/60KAYDf$U/nsycrW2A4SAuhBbAW4na4OLunPrUfR31OU3ThY1ge3vc.RUfhyHTg5dShkTYFGB/455lv0vOWDAmbGiOI730 # qbbw8&OeZ1ql
    carol: $6$rounds=656000$aXLv86ermeammjFO$MooGjguTxUjhc2m6OefDddz0mszG/SprKiyTsND0lpT3f4.R7V5KucdK9JdLluOF.WnpGAz/GKy2umf5TPkPr. # zIPjxwCFm@ES
```    

You can store the output in a file like this:

    python generate_user_passwords.py alice bob carol > user_passwords.yml

### Securing the output file

The point of the Python script and the playbook is to generate a username and password file that is **only temporary, located on your deployment machine!** If you need to put the generated file into version control or store it for longer periods of time, you should encrypt the file with the [`ansible-vault`](http://docs.ansible.com/ansible/playbooks_vault.html) command:

    python generate_user_passwords.py alice bob carol | ansible-vault encrypt > user_passwords.yml

 To display the file again on the command line, use the command

    ansible-vault view
