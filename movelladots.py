from xdpchandler import *
exit_flag=False

class movelladot():
    def initiate(self):
        self.xdpcHandler = XdpcHandler()

        if not self.xdpcHandler.initialize():
            self.xdpcHandler.cleanup()
            exit(-1)

        self.xdpcHandler.scanForDots()
        if len(self.xdpcHandler.detectedDots()) == 0:
            print("No Movella DOT device(s) found. Aborting.")
            self.xdpcHandler.cleanup()
            exit(-1)

        self.xdpcHandler.connectDots()

        if len(self.xdpcHandler.connectedDots()) == 0:
            print("Could not connect to any Movella DOT device(s). Aborting.")
            self.xdpcHandler.cleanup()
            exit(-1)

        for device in self.xdpcHandler.connectedDots():
            filterProfiles = device.getAvailableFilterProfiles()
            print("Available filter profiles:")
            for f in filterProfiles:
                print(f.label())

            print(f"Current profile: {device.onboardFilterProfile().label()}")
            if device.setOnboardFilterProfile("General"):
                print("Successfully set profile to General")
            else:
                print("Setting filter profile failed!")


            print("Putting device into measurement mode.")
            if not device.startMeasurement(movelladot_pc_sdk.XsPayloadMode_ExtendedQuaternion):
                print(f"Could not put device into measurement mode. Reason: {device.lastResultText()}")
                continue
    def start(self):
        print("\nMain loop. Recording data for 10 seconds.")
        print("-----------------------------------------")
        orientationResetDone = False
        startTime = movelladot_pc_sdk.XsTimeStamp_nowMs()
        # while movelladot_pc_sdk.XsTimeStamp_nowMs() - startTime <= 10000:
        from visualize import rotate
        trail=rotate()
        trail.startgame()
        while not exit_flag:
            if self.xdpcHandler.packetsAvailable():
                s = ""
                devicelist=self.xdpcHandler.connectedDots()
                for device in devicelist:
                    try:
                        packet1 = self.xdpcHandler.getNextPacket("D4:22:CD:00:39:41")
                        packet2 = self.xdpcHandler.getNextPacket("D4:22:CD:00:39:65")
                        packet3 = self.xdpcHandler.getNextPacket("D4:22:CD:00:39:40")
                        packet4 = self.xdpcHandler.getNextPacket("D4:22:CD:00:39:51")
                        packet5 = self.xdpcHandler.getNextPacket("D4:22:CD:00:39:4A")

                        if packet1.containsOrientation():
                            quaternion1 = packet1.orientationQuaternion(movelladot_pc_sdk.XDI_CoordSysEnu)
                            quatw1=float(f"{quaternion1[0]:7.4f}")
                            quatx1=float(f"{quaternion1[1]:7.4f}")
                            quaty1=float(f"{quaternion1[2]:7.4f}")
                            quatz1=float(f"{quaternion1[3]:7.4f}")
                        if packet2.containsOrientation():
                            quaternion2 = packet2.orientationQuaternion(movelladot_pc_sdk.XDI_CoordSysEnu)
                            quatw2=float(f"{quaternion2[0]:7.4f}")
                            quatx2=float(f"{quaternion2[1]:7.4f}")
                            quaty2=float(f"{quaternion2[2]:7.4f}")
                            quatz2=float(f"{quaternion2[3]:7.4f}")
                        if packet3.containsOrientation():
                            quaternion3 = packet3.orientationQuaternion(movelladot_pc_sdk.XDI_CoordSysEnu)
                            quatw3=float(f"{quaternion3[0]:7.4f}")
                            quatx3=float(f"{quaternion3[1]:7.4f}")
                            quaty3=float(f"{quaternion3[2]:7.4f}")
                            quatz3=float(f"{quaternion3[3]:7.4f}")
                        if packet4.containsOrientation():
                            quaternion4 = packet4.orientationQuaternion(movelladot_pc_sdk.XDI_CoordSysEnu)
                            quatw4=float(f"{quaternion4[0]:7.4f}")
                            quatx4=float(f"{quaternion4[1]:7.4f}")
                            quaty4=float(f"{quaternion4[2]:7.4f}")
                            quatz4=float(f"{quaternion4[3]:7.4f}")
                        if packet5.containsOrientation():
                            quaternion5 = packet5.orientationQuaternion(movelladot_pc_sdk.XDI_CoordSysEnu)
                            quatw5=float(f"{quaternion5[0]:7.4f}")
                            quatx5=float(f"{quaternion5[1]:7.4f}")
                            quaty5=float(f"{quaternion5[2]:7.4f}")
                            quatz5=float(f"{quaternion5[3]:7.4f}")
                            
                        trail.cube([quatw1,quatx1,quaty1,quatz1],[quatw2,quatx2,quaty2,quatz2],[quatw3,quatx3,quaty3,quatz3],[quatw4,quatx4,quaty4,quatz4],[quatw5,quatx5,quaty5,quatz5])
                    except:
                        pass
                print("%s\r" % s, end="", flush=True)

                if not orientationResetDone and movelladot_pc_sdk.XsTimeStamp_nowMs() - startTime > 6000:
                    for device in self.xdpcHandler.connectedDots():
                        print(f"\nResetting heading for device {device.portInfo().bluetoothAddress()}: ", end="", flush=True)
                        if device.resetOrientation(movelladot_pc_sdk.XRM_Heading):
                            print("OK", end="", flush=True)
                        else:
                            print(f"NOK: {device.lastResultText()}", end="", flush=True)
                    print("\n", end="", flush=True)
                    orientationResetDone = True
        print("\n-----------------------------------------", end="", flush=True)
        trail.endgame()

    def stopmeaurement(self):
        for device in self.xdpcHandler.connectedDots():
            print(f"\nResetting heading to default for device {device.portInfo().bluetoothAddress()}: ", end="", flush=True)
            if device.resetOrientation(movelladot_pc_sdk.XRM_DefaultAlignment):
                print("OK", end="", flush=True)
            else:
                print(f"NOK: {device.lastResultText()}", end="", flush=True)
        print("\n", end="", flush=True)

        print("\nStopping measurement...")
        for device in self.xdpcHandler.connectedDots():
            if not device.stopMeasurement():
                print("Failed to stop measurement.")

        self.xdpcHandler.cleanup()

if __name__ == "__main__":
    try:
        from pynput import keyboard as kb
        exit_flag=False
        def on_press(key):
            global exit_flag
            if key == kb.Key.esc:
                exit_flag = True
            
        listener = kb.Listener(on_press=on_press)
        listener.start()
        d=movelladot()
        d.initiate()
        d.start()
    finally:
        d.stopmeaurement()