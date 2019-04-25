from appJar import gui # Used to create the GUI
from platform import system # Used to determine which OS the script is running on
from os.path import expanduser # Used to find the user' s home dir.
from tempfile import NamedTemporaryFile

# Path to cleansio
CLEANSIO_PATH = "../cleansio.py"

# Create the GUI
app = gui()

# Handles a button press
def press(button):
	global app

	if button == "Censor File":
		## We need to build the command string here and call cleansio
		songs = app.getAllListItems("convSongs") # Fetch the list of songs
		#print(songs)
		uExps = app.getAllListItems("uExps")
		tempFile = None
		outDir = app.getEntry("Output directory")
		fName = app.getEntry("Output filename")
	
		if len(uExps) > 0: # The user provided a list of explicits
			tempFile = NamedTemporaryFile() # Create a temporary file
		
			for explicit in uExps: # For each explicit word
		 		tempFile.write("{0}\n".format(explicit))
	
		if len(songs) > 0:
		
			for song in songs: # For each path
				command = "python3.6 {0} {1}".format(CLEANSIO_PATH, song)
				
				if tempFile != None: # List of songs
					command = "{0} -u {1}".format(command, tempFile.name)
				
				if outDir != None and fName != None:
					command = "{0} -o {1}/{2}".format(command, outDir, fName)
				
				print("Conversion command = {0}".format(command))
	
		else:
			msg = "You must enter at least one song to convert"
			app.errorBox("No songs", msg)
	
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
		app.setEntry("Output directory", dirPath)
	
	elif button == "Set output filename":
		fileName = app.textBox("Set file name", "Please enter the output\
		file name")
		#print("Added word {0}".format(fileName))
		app.setEntry("Output filename", fileName)
	
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
	app.addLabelEntry("Output filename")
	app.addButtons(["Set output directory", "Set output filename"], press)
	app.stopFrame()
	
	if system() == "Darwin": # Mac
		app.addButtons(["Censor File", "Realtime Censoring"], press)
	
	else: # Windows/Linux
		app.addButtons(["Censor File"], press)


def main():
	setupGUI() # Set up the GUI
	#print(app.getAllEntries())
	app.go() # Show the GUI

if __name__ == "__main__":
	main()
