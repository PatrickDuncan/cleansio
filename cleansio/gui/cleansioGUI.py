from appJar import gui # Used to create the GUI
from platform import system # Used to determine which OS the script is running on
from os.path import expanduser # Used to find the user' s home dir.

# Create the GUI
app = gui()

# Handles a button press
def press(button):
	if button == "Convert Songs":
	    songs = app.getAllListItems("convSongs") # Fetch the list of songs
	    #print(songs)
	
	elif button == "Realtime Censoring": # Realtime
	    app.infoBox("Info", "Only on Mac")

	elif button == "Add Song": # Add songs to the list using a file picker
	    chosenFile = app.openBox("Choose a song", dirName="{0}/School/Capstone/songs/old".format(expanduser("~")), fileTypes=[("Audio files", "*.wav"), ("Audio Files", "*.mp3")])
	    #print(chosenFile)
	    app.addListItem("convSongs", chosenFile)
	
	elif button == "Add a custom explicit word":
	    newWord = app.textBox("Add a word", "Please enter the word to be muted")
	    #print("Added word {0}".format(newWord))
	    app.addListItem("uExps", newWord)

	elif button == "Set output directory":
	   dirPath = app.directoryBox("Set directory", dirName=expanduser("~"))
	   print("dirPath = {0}".format(dirPath))

	elif button == "Set output file name":
	    app.infoBox("NOthing", "Sorry, this does nothing for now")

	else: # Unknown
	    app.infoBox("???", "How did this happen?")
	print("button = \"{0}\"".format(button))

# Sets up the GUI
def setupGUI():
	global app

	app.setTitle("Cleansio")

	### Start the left frame
	app.startFrame("leftFrame", row=0, column=0)
	
	## Add a labelled box to contain the conversion inputs
	app.startLabelFrame("Songs to convert")
	app.startScrollPane("convListScrollPane")
	app.addListBox("convSongs", [])
	app.stopScrollPane()
	app.addButtons(["Add Song", "Convert Songs"], press)
	app.stopLabelFrame()

	app.stopFrame()

	## Right frame
	app.startFrame("rightFrame", row=0, column=1)
	app.startLabelFrame("Custom explicit words")
	app.startScrollPane("userExpPane")
	app.addListBox("uExps", [])
	app.stopScrollPane()
	app.addButtons(["Add a custom explicit word"], press)
	app.stopLabelFrame()
	app.stopFrame()

	## Bottom left
	app.startFrame("bottomLeft", row=2, column=0)
	app.addLabelEntry("Output directory")
	app.addLabelEntry("Output file name")
	app.addButtons(["Set output directory", "Set output file name"], press)
	app.stopFrame()
	
	if system() == "Darwin": # Mac
	    app.addButtons(["Censor File", "Realtime Censoring"], press)
	
	else: # Windows/Linux
	    app.addButtons(["Censor File"], press)


def main():	
	setupGUI() # Set up the GUI
	app.go() # Show the GUI

if __name__ == "__main__":
	main()
