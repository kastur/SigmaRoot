adb $1 install -r out/production/sigma/sigma.apk &&
adb $1 logcat -c &&
adb $1 shell am start -n "edu.ucla.nesl.sigma/edu.ucla.nesl.sigma.samples.TestSuiteActivity" -a android.intent.action.MAIN -c android.intent.category.LAUNCHER  &&
adb $1 logcat
