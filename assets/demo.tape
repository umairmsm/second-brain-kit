Output "assets/demo.gif"

Set Shell "bash"
Set FontSize 14
Set Width 860
Set Height 480
Set Padding 16
Set Theme "Catppuccin Mocha"
Set WindowBar Colorful
Set BorderRadius 8

Hide
Type "clear"
Enter
Show

Type "python3 scripts/generate-dashboard.py --vault ./vault"
Sleep 500ms
Enter
Sleep 3500ms
