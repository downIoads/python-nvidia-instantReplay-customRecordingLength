import winreg as wrg 
import struct


def getCurrentLength():
    # registry root of interest is HKEY_CURRENT_USER 
    location = wrg.HKEY_CURRENT_USER 

    # folder of interest: HKEY_CURRENT_USER\Software\NVIDIA Corporation\Global\ShadowPlay\NVSPCAPS
    try:
        folder = wrg.OpenKeyEx(location, "Software\\NVIDIA Corporation\\Global\\ShadowPlay\\NVSPCAPS\\")
    except:
        print("Failed to find folder Software\\NVIDIA Corporation\\Global\\ShadowPlay\\NVSPCAPS.\nAborting..")
        return

    # value of interest: DVRBufferLen
    curRecordingLengthTuple = wrg.QueryValueEx(folder,"DVRBufferLen") 

    # convert to big endian decimal (time in seconds)
    curRecordingLength = str(struct.unpack('<I', curRecordingLengthTuple[0])[0])

    # close registry
    if folder: 
        wrg.CloseKey(folder) 

    # return currently set recording length in seconds as string
    return curRecordingLength


def setNewLength(newRecordingLength):
    # registry root of interest is HKEY_CURRENT_USER 
    location = wrg.HKEY_CURRENT_USER 

    # folder of interest: HKEY_CURRENT_USER\Software\NVIDIA Corporation\Global\ShadowPlay\NVSPCAPS
    try:
        # 0, wrg.KEY_SET_VALUE gives permission to write
        folder = wrg.OpenKeyEx(location, "Software\\NVIDIA Corporation\\Global\\ShadowPlay\\NVSPCAPS\\", 0, wrg.KEY_SET_VALUE)
    except Exception as e:
        print("Failed to find folder Software\\NVIDIA Corporation\\Global\\ShadowPlay\\NVSPCAPS.\nAborting..")
        return False, e
    
    # write new binary value to DVRBufferLen (will create key if it does not exist already), 0 is just reserved without meaning
    try:
        wrg.SetValueEx(folder, "DVRBufferLen", 0, wrg.REG_BINARY, newRecordingLength) 
    except Exception as e:
        return False, e
        
    if folder: 
        wrg.CloseKey(folder)

    return True, None

def main():
    # enter the length you want in SECONDS (e.g. 420 is 7 min, 3600 is 60 min, ...)
    iWantThisRecordingLength = 3600

    # -------------------------- DON'T CHANGE ANYTHING BELOW --------------------------

    # ---- Check if user value is valid (larger than 0 and smaller than 4294967296)
    if iWantThisRecordingLength < 1 or iWantThisRecordingLength > 4294967295:
        print("Recording length of " + str(iWantThisRecordingLength) + " is not allowed.. Aborting.")
        return

    # ---- Convert user value to small endian hex binary string ----
    newRecordingLength = struct.pack('<I', iWantThisRecordingLength)

    # ---- Determine current recording length ----
    curRecordingLength = getCurrentLength()
    # if something went wrong abort
    if not curRecordingLength:
        return 
    print("Old NVIDIA InstantReplay Recording Length: " + curRecordingLength + " sec")

    # ---- Set new recording length ----
    print("Writing new value..")
    successBool, err = setNewLength(newRecordingLength)
    if not successBool:
        print("Failed to set new recording length: " + str(err))
        return
    print("Successfully set new recording length: " + str(iWantThisRecordingLength) + " seconds.\n\nPlease restart your PC for the changes to take effect.")


main()
