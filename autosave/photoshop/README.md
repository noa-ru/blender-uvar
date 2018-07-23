draw in psd, will be autosaved in %psdpath%\%psdname%.PNG (by pressing ctrl+s)(1)

tested on:
* Photoshop CS5.1

# Installation steps
* File -> Scripts -> Script Events Manager
* Select "Photoshop Event" to "Save Document"(1)
* Browse "exportToPNG24.jsx" in "Script" section
* press add, press done

(1) - "Save Document" event fired by pressing (ctrl+s, or File -> Save)
If we select "All" event, everything works except for the "draw" event. Maybe it's something else ?

Unfortunately has not yet found a way to process it :(.

[Event codes](http://cssdk.s3-website-us-east-1.amazonaws.com/sdk/1.5/docs/WebHelp/app_notes/photoshop.htm)

