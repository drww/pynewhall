from Tkinter import Tk, Menu

def dummy():
	print "Got event."

# Build and launch a populated Frame.
def build_root():

	ui_root = Tk()

	# Build root drop-down menu and immediate child menus.
	main_menu = Menu(ui_root)
	file_submenu = Menu(main_menu, title="File")
	settings_submenu = Menu(main_menu, title="Settings")
	help_submenu = Menu(main_menu, title="Help")

	# File
	file_submenu.add_command(label="New Dataset...", command=dummy)
	file_submenu.add_command(label="Open...", command=dummy)
	file_submenu.add_command(label="Export...", command=dummy)
	file_submenu.add_separator()
	file_submenu.add_command(label="Quit", command=dummy)

	# Settings
	settings_submenu.add_command(label="PyNewhall Settings...", command=dummy)

	# Help
	help_submenu.add_command(label="About...", command=dummy)
	help_submenu.add_command(label="Documentation...", command=dummy)

	# Wrap up building main drop down menubar.
	main_menu.add_cascade(label="File", menu=file_submenu)
	main_menu.add_cascade(label="Settings", menu=settings_submenu)
	main_menu.add_cascade(label="Help", menu=help_submenu)
	ui_root.config(menu=main_menu)

	ui_root.mainloop()