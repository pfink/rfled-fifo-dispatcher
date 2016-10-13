import os
import atexit
import milight

LED_PORT = 8899
FIFO = '/tmp/rfled-fifo'


@atexit.register
def cleanup():
    try:
        os.unlink(FIFO)
    except:
        pass


def main():
    os.mkfifo(FIFO)
    light = milight.LightBulb(['rgbw'])

    with open(FIFO) as fifo:
        while True:
            with open(FIFO) as fifo:
                while True:
                    args = {}
                    raw_command = fifo.read()
                    if raw_command == "":
                        break

                    raw_list = raw_command.split(" ")
                    for raw_element in raw_list:
                        arg = raw_element.split("=")
                        args[arg[0]] = arg[1]
                    args_keys = args.keys()

                    # Check command
                    if not {'CMD', 'IP', 'GROUP'}.issubset(set(args_keys)):
                        print("raw_command '" + raw_command + "' invalid. Skipped command.")
                        continue

                    print("Cmd: " + args['CMD'])
                    print("Group: " + args['GROUP'])
                    print("IP: " + args['IP'])
                    print("")

                    args['GROUP'] = int(args['GROUP'])

                    controller = milight.MiLight({'host': args['IP'], 'port': 8899})

                    if args['CMD'] in ["RGBON", "RGBWHITE"]:
                        command = light.on(args['GROUP'])
                    elif args['CMD'] == "RGBOFF":
                        command = light.off(args['GROUP'])
                    else:
                        print("raw_command '" + raw_command + "' invalid. Skipped command.")
                        continue

                    controller.send(command)


main()