ADB="adb $1"
# Get all the debug traces from the sdcard, and output them as html for analysis.
mkdir traces
$ADB shell rm -rf /sdcard/tmpSigma
$ADB shell mkdir /sdcard/tmpSigma
$ADB shell mv /sdcard/*.trace /sdcard/tmpSigma
$ADB $1 pull /sdcard/tmpSigma traces
