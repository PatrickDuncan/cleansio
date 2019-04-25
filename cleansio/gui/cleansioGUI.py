from appJar import gui # Used to create the GUI
from platform import system # Used to determine which OS the script is running on
from os.path import expanduser # Used to find the user' s home dir.

# Create the GUI
app = gui()

# Handles a button press
def press(button):
	if button == "Censor File":
		app.infoBox("Test", "Hello world!")
	
	elif button == "Realtime Censoring": # Realtime
		app.infoBox("Info", "Only on Mac")

	elif button == "Add Song": # Add songs to the list using a file picker
		chosenFile = app.openBox("Choose a song", dirName=expanduser("~"), fileTypes=[("Audio files", "*.wav"), ("Audio Files", "*.mp3")])

	else: # Unknown
		app.infoBox("???", "How did this happen?")

# Sets up the GUI
def setupGUI():
	### Start the left frame
	app.startFrame("leftFrame", row=0, column=0)

	## Add a labelled box to contain the conversion inputs
	app.startLabelFrame("Songs to convert")
	app.startScrollPane("convListScrollPane")
	app.addListBox("convSongs", [])
	app.stopScrollPane()
	app.addButtons(["Add Song"], press)
	app.stopLabelFrame()

	app.stopFrame()

	if system() == "Darwin": # Mac
		app.addButtons(["Censor File", "Realtime Censoring"], press)

	else: # Windows/Linux
		app.addButtons(["Censor File"], press)

setupGUI() # Set up the GUI
app.go() # Show the GUI
