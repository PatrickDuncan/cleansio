from appJar import gui

app = gui()
app.addLabel("title", "File Picker Test")
app.setLabelBg("title", "red")
fObj = app.openBox(title="Choose a song", fileTypes=[("Audio Files", "*.wav")], asFile=True)
print(fObj)
app.go()
