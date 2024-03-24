# Custom Recording Length for Instant Replay

## Why?
NVIDIA GeForce Experience does not allow you set any value smaller than 15 seconds or larger than 20 minutes. But if you want to record a different interval than this it is still possible by manually editing the registry by putting the time you want in seconds as small endian hex in the value "DVRBufferLen" of Computer\HKEY_CURRENT_USER\Software\NVIDIA Corporation\Global\ShadowPlay\NVSPCAPS.

This script makes the process trivial. Just put the time you want in seconds and run it, then restart PC.
