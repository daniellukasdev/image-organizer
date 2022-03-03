# image-organizer
A simple image organizer app created using python 3.7 and pyqt5.


![image-organizer-interface](https://user-images.githubusercontent.com/65349554/156636831-8a84e9aa-cd1b-48e3-9f65-db1674662c7d.png)

![image-organizer-interface-with-images](https://user-images.githubusercontent.com/65349554/156636674-58906f19-5b28-4e37-851c-1f5b7f9c8323.png)


_*On Windows you may need to whitelist image-organizer.exe to your antivirus settings_  

# Installation & Execution
## Install Dependencies
```shell
pip3 install pyqt5
pip3 install qtmodern
```
## Run From Terminal
```shell
cd image-organizer
python3 image-organizer.py
```

## Changelog

### Latest
**2022.02.28**
_version 0.2.1alpha_

- Added option to rename files based on category
- Option is currently presented as a pop-up

_See [changelog](./changelog.md) for full history_


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
- Add the ability to simply press the enter button instead of having to click every button.
- Add the use of the keyboard to navigate through the thumbnails.
- Look into multiple image selection.
- Rework selecting categories
- Add a *Mark-Up* feature to draw on the images. (*maybe*)

# Known Bugs
- If file extensions are uppercase the image files will be ignored. (Fix coming in next release)
- Category selection menu items not in alphabetical order.
- Once a directory is loaded, the first thumbnail does not get highlighted on the second import if the filename of the first image matches that of the filename of the first image currently loaded.
- Running app icon on Windows only shows generic system icon.
