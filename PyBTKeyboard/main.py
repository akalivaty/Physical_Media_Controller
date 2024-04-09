import bluetooth
import Custom_KeySet as CK


def DiscoverDevices(deviceName):
    print("Searching for devices...")

    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    for addr, name in nearby_devices:
        if name == deviceName:
            print(f"Found {deviceName}, MAC address: {addr}")
            return addr

    return None


def PostProcess(buffer):
    # [b'b', b'tn2']
    # [b'b', b'tn2']
    # [b'v', b'olume:\x00']
    # [b'v', b'olume:\x01']
    if len(buffer) == 1:
        return ["command", buffer[0].decode("utf-8")]
    else:
        if b":" in buffer[1]:
            magnitude = ord(buffer[1].split(b":")[1])
            return ["volume", magnitude]
        else:
            buffer = [string.decode("utf-8") for string in buffer]
            command = "".join(buffer)
            return ["command", command]


def main():
    ck = CK.Custom_KeySet()

    # with open("custom_key.json", "w") as file:
    #     json.dump(mappingKey, file, indent=4)

    # todo: for testing
    # deviceName = input("Enter the device name: ")
    # deviceAddr = DiscoverDevices(deviceName)
    deviceName = "HC-05-2"
    deviceAddr = "98:D3:31:80:67:5E"

    if deviceAddr is None:
        print(f"Could not find {deviceName}")
        return

    else:
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        socket.connect((deviceAddr, 1))

        print(f"Connected to {deviceName}")
        buffer = []
        while True:
            data = socket.recv(1024)  # .decode("utf-8")
            # print(data.split(b"\n"))
            if b"\n" in data:
                buffer.append(data[:-1])
                commandSet = PostProcess(buffer)
                print(commandSet)
                if commandSet[0] == "command":
                    ck.inputKey(commandSet[1])
                else:
                    # todo: volume
                    pass
                buffer.clear()
            else:
                buffer.append(data)

        socket.close()


if __name__ == "__main__":
    main()
