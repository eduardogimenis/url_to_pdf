import dearpygui.dearpygui as dpg
import pdfkit
import os
# Dictionary to store file names and URLs
links = {}
# Variable to store the chosen directory
save_directory = ""
# Function to check if wkhtmltopdf is installed
def check_wkhtmltopdf_installed():
    if not pdfkit.configuration().wkhtmltopdf:
        dpg.add_text("wkhtmltopdf not found. Please ensure it is installed and in your PATH.", parent="log_window")
        return False
    return True
# Function to add user input to the dictionary and update the list
def add_link():
    file_name = dpg.get_value("file_name_input")
    url = dpg.get_value("url_input")
    
    if not check_wkhtmltopdf_installed():
        return
    
    if file_name and url:
        links[file_name] = url
        dpg.add_text(f"{file_name} -> {url}", parent="link_list")
        dpg.set_value("file_name_input", "")
        dpg.set_value("url_input", "")
    else:
        dpg.add_text("Please fill both fields.", parent="log_window")
# Function to handle directory selection
def select_directory(sender, app_data):
    global save_directory
    save_directory = app_data["file_path_name"]
    dpg.set_value("directory_display", save_directory)
    dpg.add_text(f"Save directory set to: {save_directory}", parent="log_window")
# Function to generate PDFs from the dictionary
def generate_pdfs():
    global save_directory
    if not check_wkhtmltopdf_installed():
        return
    
    if not save_directory:
        dpg.add_text("Please select a save directory.", parent="log_window")
        return
    
    if links:
        dpg.set_value("status_bar", "Generating PDFs...") 
        for file_name, url in links.items():
            try:
                file_path = os.path.join(save_directory, file_name + ".pdf")
                pdfkit.from_url(url, file_path)
                dpg.add_text(f"Generated PDF: {file_path}", parent="log_window")
            except Exception as e:
                dpg.add_text(f"Error generating PDF for {file_name}: {e}", parent="log_window")
        links.clear()
        dpg.delete_item("link_list", children_only=True)
        dpg.set_value("file_name_input", "") 
        dpg.set_value("url_input", "") 
        dpg.set_value("status_bar", "Ready") 
    else:
        dpg.add_text("No links added yet.", parent="log_window")
# Function to clear the log window
def clear_log():
    dpg.delete_item("log_window", children_only=True)
# Function to clear the link list
def clear_links():
    links.clear()
    dpg.delete_item("link_list", children_only=True)
    dpg.add_text("Cleared all links.", parent="log_window")
# Create DearPyGui context
dpg.create_context()
# Adjusted viewport size to reduce unnecessary space
viewport_width = 800
viewport_height = 600
dpg.create_viewport(title='Webpage to PDF Converter', width=viewport_width, height=viewport_height)
dpg.setup_dearpygui()
dpg.show_viewport()
# Main window with adjusted size to fit the viewport properly
with dpg.window(label="Webpage to PDF Converter", tag="Main Window", width=viewport_width - 20, height=viewport_height - 40):

    # Input fields
    dpg.add_input_text(label="File Name", tag="file_name_input", hint="Enter desired PDF file name")
    dpg.add_input_text(label="URL", tag="url_input", hint="Enter webpage URL")
    
    # Button to open directory selection dialog
    dpg.add_button(label="Select Save Directory", callback=lambda: dpg.show_item("directory_dialog"))

    # Display selected directory
    dpg.add_text("No directory selected", tag="directory_display")
    
    # Buttons
    with dpg.group(horizontal=True):
        dpg.add_button(label="Add Link", tag="add_link_button", callback=add_link)
        dpg.add_button(label="Generate PDFs", tag="generate_pdfs_button", callback=generate_pdfs)
        dpg.add_button(label="Clear Links", callback=clear_links)

    # Group to arrange links and log side-by-side
    dpg.add_spacing(count=10)
    with dpg.group(horizontal=True):
        with dpg.child_window(label="Links", tag="link_list", width=350, height=300):
            with dpg.group(horizontal=False): 
                pass

        dpg.add_spacing(count=5) 

        with dpg.child_window(label="Log", tag="log_window", width=350, height=300):
            with dpg.group(horizontal=False): 
                pass

    # Button to clear log and status bar
    dpg.add_spacing(count=10)
    with dpg.group(horizontal=True):
        dpg.add_button(label="Clear Log", callback=clear_log)

    # Status bar
    dpg.add_text("Ready", tag="status_bar")
# Directory selection dialog
with dpg.file_dialog(directory_selector=True, show=False, callback=select_directory, tag="directory_dialog", height=400, width=600):
    dpg.add_file_extension(".*", color=(150, 255, 150, 255))  # Show all directories
# Set the primary window (after window creation)
dpg.set_primary_window("Main Window", True)
# Start DearPyGui
dpg.start_dearpygui()
dpg.destroy_context()