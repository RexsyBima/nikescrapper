import os

#def get_files_in_folder(folder_path):
#    file_list = []
#
#    # List all files and directories in the given folder path
#    entries = os.listdir(folder_path)
#
#    for entry in entries:
#        # Check if the entry is a file (not a directory)
#        if os.path.isfile(os.path.join(folder_path, entry)):
#            full_path = os.path.join(folder_path, entry)
#            file_list.append("file://" + full_path)
#
#    return file_listp
#
#folder_path = "/home/rexsybimq12/python/scrapy/nike/nike/html_output"
#filenames_with_path = get_files_in_folder(folder_path)


#file:///home/rexsybimq12/python/scrapy/nike/nike/spiders/page.html
def get_html_folder_files():
    root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
    folder_path = os.path.join(root_folder, ".temp","html_output")
    return folder_path

x = "asd"
y = int(x)
print(y)