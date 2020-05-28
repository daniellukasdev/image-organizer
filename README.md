# image-organizer
A simple image organizer app created using python 3.7 and pyqt5.


# Changelog:

**2020.05.26**
*version 0.1* 
- Initial release with core functionality.


# How To:
1. Click *Browse* to get the path to the image folder.
2. Click *Import* to load all supported images.
3. Create a new category by typing the desired name in the *Create New Category* input box, and click the *Create* button.
4. The new category is available as an option in the selection menu under the currently displayed image.
5. Add the currently selected image to a category by selecting it in the drop-down menu and clicking the *Add* button.
6. Once all images are organized click on the *Organize* button. This brings up a message for you to confirm the action or cancel and go back.
7. A folder is created in the working directory for every category you create and add an image to.
8. Confirming the action executes the operations.

# Todo:
- Fix OS Compatibility
- Compile into executable for Win, MacOS, ~~and Linux~~.
- Add the ability to simply press the enter button instead of having to click every button.
- Add the use of the keyboard to navigate through the thumbnails.
- Look into multiple image selection.
- Add a *Mark-Up* feature to draw on the images. (*maybe*)

# Known Bugs
- Once a directory is loaded, the first thumbnail does not get highlighted on the second import if the filename of the first image matches that of the filename of the first image currently loaded.
