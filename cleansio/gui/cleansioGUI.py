from appJar import gui # GUI
from platform import system # system

# Create the GUI
app = gui()

# Handles a button press
def press(button):
	app.infoBox("Test", "Hello world!")

# Sets up the GUI
def setupGUI():
	if system() == "Darwin": # Mac
		app.addButtons(["Censor File", "Realtime Censoring"], press)

	else: # Windows/Linux
		app.addButtons(["Censor File"], press)

setupGUI() # Set up the GUI
app.go() # Show the GUI
