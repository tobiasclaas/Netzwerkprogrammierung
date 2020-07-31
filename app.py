import sys
import time
import subprocess

from flask import Flask
from pip._vendor import requests
from threading import Thread
from pip._vendor.urllib3.exceptions import NewConnectionError

app = Flask(__name__)


controller_list = {     # dictionary of controllers, 4 in this case, all set inactive(False)
    'http://127.0.0.1:5000': (False, None),  # at the beginning, active is True
    'http://127.0.0.1:5001': (False, None),
    'http://127.0.0.1:5002': (False, None),
    'http://127.0.0.1:5003': (False, None),
    'http://127.0.0.1:5004': (False, None)
}
num_controllers_active = 0  # number of active controller
num_controllers = len(controller_list)


@app.route('/')
def print_controller():
    """
    This site is for debug only. It shows for each controller if it is active and what their master is.
    :return: the dictionary of controllers
    """
    return str(controller_list)


@app.route('/request')
def send_message():
    """
    All controller communicate with each other via this service.
    :return: current master of controller
    """
    return str(get_master())


def get_master():
    """
    Getter method of master
    :return: master address as string or None if controller has no master
    """
    return controller_list[my_address][1]


def set_master(address):
    """
    Setter method for master. The master is stored in controller_list dictionary
    :param address: The address, containing ip and port of the controller that shall be set
    :return: if master does not change
    """
    old_master = get_master()
    if old_master == address:
        return

    controller_list[my_address] = (True, address)

    if old_master == my_address:
        i_am_worker()
    if address == my_address:
        i_am_master()


# calculates the master according to lowest ip and port
def determine_master():
    """
    The function is called when a new master needs to be determined for a controller.
    First we check if there's already a controller with a quorum. If so that one is the new master.
    If not we determine a new master based on the ip and port number. The controller with lowest ip and port number
    is selected and set as master.
    :return:
    """
    # check if there's a master with quorum
    master_list = {}
    for controller in controller_list:  # calculate how many controllers voted for this controller as master
        if not controller_list[controller][0]:
            continue
        if controller_list[controller][1] in master_list:  # is master of this controller in controller-list
            master_list[str(controller_list[controller][1])] += 1
        else:
            master_list.update({controller: 1})

    for controller in master_list:
        if master_list[controller] > num_controllers / 2:
            set_master(controller)
            return

    # give tip otherwise
    master_ip = ""
    master_port = ""

    for controller in controller_list:
        # new master is controller with lowest ip and port (unique)
        temp, ip, port = controller.split(':')
        ip = ip.split('//')[1]

        if master_ip == "" and controller_list[controller][0]:     # For the first controller that is active
            master_ip = ip
            master_port = port

        if master_ip >= ip:
            if master_port > port and controller_list[controller][0]:  # must have lower ip and/or port and be active
                master_ip = ip
                master_port = port

    set_master("http://" + master_ip + ":" + master_port)


# script that controller executes when it becomes the master
def i_am_master():
    """
    Function that is called when a controller becomes master. It executes a certain script that can be stated in
    program args.
    :return:
    """
    if master_script != "":
        execute_script(master_script)
    else:
        print("I am master!")


# script that controller executes when it becomes a worker
def i_am_worker():
    """
    Function that is called when a controller becomes worker. It executes a certain script that can be stated in
    program args.
    :return:
    """
    if worker_script != "":
        execute_script(worker_script)
    else:
        print("I am worker!")


def execute_script(script):
    """
    A function that executes a script according to its type.
    :param script: The script file name.
    :return:
    """
    if script.endswith(".py"):  # if file is python file
        subprocess.call("python " + script, shell=True)
    elif script.endswith(".sh"):
        subprocess.call("sh " + script, shell=True)


# check what other controllers think who is master
def check_master():
    """
    Check whether there is a majority so a quorum can be made due to potentially new controllers.
    If more that half of all registered controllers are active determine master, e.g. at startup.
    If a master already exists check if it is available. If not determine new master.
    :return:
    """
    master = get_master()
    if num_controllers_active < num_controllers / 2:  # need quorum
        set_master(None)
        return

    if master == "None" or master is None:
        determine_master()
        return
    else:   # not enough controller for quorum
        if not controller_list[str(master)][0]:  # master not alive anymore
            determine_master()


# checks the status of other controllers and store it in controller_list
def check_other_controller_status():
    """
    The controller requests all other controllers and stores their availability and master. It also counts the number
    of active controllers, which is important for the quorum.
    :return:
    """
    global num_controllers_active
    num_controllers_active = 0

    for controller in controller_list:
        address_suffix = "/request"

        if controller == my_address:  # skip self
            num_controllers_active += 1
            continue

        try:
            response = requests.get(controller + address_suffix, timeout=0.2).text
            num_controllers_active += 1
            if response == "None":
                response = None  # controller has no master
            controller_list[controller] = (True, response)  # if the controller answered, set True
        except (ConnectionError, ConnectionRefusedError, NewConnectionError, Exception):
            # if request.get fails after 0.2 seconds exception is thrown
            controller_list[controller] = (False, None)


def scan():
    """
    The method is called at the start of a controller. It sets the controller as active and calls the function
    i_am_worker, because the new controller can not enter the environment as master.
    Then it basically starts an endless loop checking the other controllers and making sure the master is available in
    a 5 seconds rhythm.
    :return:
    """
    controller_list[my_address] = (True, None)  # set controller to alive
    i_am_worker()
    while running:  # go in infinite loop scanning
        check_other_controller_status()  # check other controllers status
        check_master()  # check if the master is the same
        time.sleep(5)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("give ip and port for initialization")
        exit(0)

    my_ip = sys.argv[1]
    my_port = sys.argv[2]
    my_address = "http://" + str(my_ip) + ":" + str(my_port)

    master_script = ""
    worker_script = ""
    if len(sys.argv) == 5:
        master_script = sys.argv[3]
        worker_script = sys.argv[4]

    running = True

    client = Thread(target=scan)
    client.start()
    app.run(host=my_ip, port=my_port)
    running = False
