import socket
import os
import time
from slackclient import SlackClient
import re

def print_next(command):
    return "Not implemented"


def print_help(command):
    return "try *" + "* or *".join(functions.keys()) + "*"


def skip_next(command):
    return "Not implemented"


def stop(command):
    return "Not implemented"


def pause(command):
    return "Not implemented"


def return_to_normal_operation(command):
    return "Not implemented"


def run_station(command):
    # If there is an event running, put it in the paused events list
    # then make a new one and put it to the current!
    return "Not implemented"


def print_current(command):
    return "Not Implemented"


def just(command):
    cmd_string = command.replace('just ', '')
    print(cmd_string)
    s.send((cmd_string + '\n').encode('utf-8'))
    return "I sent \"" + cmd_string + "\\n\""

functions = {"next" : print_next,
             "help" : print_help,
             "skip" : skip_next,
             "stop" : stop,
             "pause" : pause,
             "run": run_station,
             "continue": return_to_normal_operation,
             "state": print_current,
             "just": just}


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = None
    if AT_BOT in command:
        cmd = command.split(AT_BOT)[1].strip().lower()
        response = "Not sure what you mean. Try *help*"

        first_arg = cmd.split()[0]
        if first_arg in functions.keys():
            print(first_arg)
            response = functions[first_arg](cmd)

        if response is not None:
            slack_client.api_call("chat.postMessage", channel=channel,
               text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                # return text after the @ mention, whitespace removed
                return output['text'], output['channel']
    return None, None


def event_to_command(event):
    command = ""
    if 'username' in event and 'attachments' in event and len(event['attachments']) == 1 and 'title' in event['attachments'][0] and 'text' in event['attachments'][0]:
        if event['username'] == "Irrigation":
            zone = event['attachments'][0]['title']
            regexp = r'\^(\d*)\^'
            results = re.findall(regexp, event['attachments'][0]['text'])
            if len(results) == 2:
                on_time = int(results[1]) - int(results[0])
                if on_time <= 3600:
                    command = AT_BOT + "just on " + zone + " " + str(on_time)

    return command

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

TCP_IP = '10.9.95.141'
TCP_PORT = 5555
BUFFER_SIZE = 1024
MESSAGE = b"status\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose


def main():
    s.settimeout(READ_WEBSOCKET_DELAY)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    last_channel = None

    if slack_client.rtm_connect():
        print("Irrigation Controller connected and running!")
        while True:
            slack_event = slack_client.rtm_read()
            if len(slack_event) == 1:
                scheduled_command = event_to_command(slack_event[0])

                if len(scheduled_command) > 5:
                    last_channel = slack_event[0]['channel']
                    handle_command(scheduled_command, last_channel)
                else:
                    command, channel = parse_slack_output(slack_event)
                    if command and channel:
                        handle_command(command, channel)
                        last_channel = channel

                if slack_event[0]['type'] != 'reconnect_url':
                    print(slack_event)

            try:
                data = s.recv(BUFFER_SIZE)
                if last_channel is not None:
                    slack_client.api_call("chat.postMessage", channel=last_channel,
                                          text=data.decode("utf-8"), as_user=True)
                print("received data:", data.decode("utf-8"))
            except socket.timeout:
                pass

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

    s.close()

if __name__ == "__main__":
    main()
