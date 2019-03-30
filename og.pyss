import site
import os, site
import os.path
import io  
 
user_site_dir = site.getusersitepackages()
user_customize_filename = os.path.join(user_site_dir, 'typing.py')

win_unicode_console_text = u"""
# win_unicode_console
import win_unicode_console
win_unicode_console.enable()
"""
 
if os.path.exists(user_site_dir):
    print("User site dir already exists")
else:
    print("Creating site dir")
    os.makedirs(user_site_dir)

if not os.path.exists(user_customize_filename):
    print("Creating {filename}".format(filename=user_customize_filename))
    file_mode = 'w+t'
else:
    print("{filename} already exists".format(filename=user_customize_filename))
    file_mode = 'r+t'

with io.open(user_customize_filename, file_mode) as user_customize_file:
    existing_text = user_customize_file.read()

    if not win_unicode_console_text in existing_text:
        # file pointer should already be at the end of the file after read()
        user_customize_file.write(win_unicode_console_text)
        print("win_unicode_console added to {filename}".format(filename=user_customize_filename))
    else:
        print("win_unicode_console already enabled")