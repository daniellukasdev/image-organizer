from PyQt6 import QtCore, QtGui, QtWidgets
# from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QFrame, QFileDialog, QGraphicsPixmapItem, QGraphicsScene,\
    QGraphicsView, QGridLayout,QLineEdit, QLabel, QMessageBox, QSizePolicy, QSplitter, QWidget
from PyQt6.QtGui import QImage, QPixmap
import sys, os, platform, shutil
# qtmodern.styles


class ClickFrame(QtWidgets.QFrame):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QtWidgets.QFrame.mousePressEvent(self, event)

class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        '''MainWindow Constructor'''
        super().__init__(*args, **kwargs)
        self.title = 'Image Organizer'
        self.width = 1280
        self.height = 960
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        # Create Font Style Options
        self.itallic_font = QtGui.QFont()
        self.itallic_font.setItalic(True)
        self.big_font = QtGui.QFont()
        self.big_font.setPointSize(16)
        self.big_font.setBold(True)

        # Browse Directory Button
        self.browse_button = QtWidgets.QPushButton('Browse', self)
        self.browse_button.setMaximumWidth(75)
        self.browse_button.clicked.connect(self.folder_select)

        # Select Directory and input
        self.selection_input = QtWidgets.QLineEdit(self)
        self.selection_input.setPlaceholderText("Path to Folder")
        self.selection_input.setFont(self.itallic_font)
        self.selection_input.resize(350,33)
        self.selection_input.textChanged[str].connect(self.load_btn_status)
        # Select Button
        self.import_button =  QtWidgets.QPushButton('Import', self)
        self.import_button.clicked.connect(self.create_working_directory)
        self.import_button.setDisabled(True)

        # new category input
        self.new_category_input = QtWidgets.QLineEdit(self)
        self.new_category_input.setPlaceholderText("Create New Category...")
        self.new_category_input.setFont(self.itallic_font)
        self.new_category_input.resize(350,33)
        self.new_category_input.textChanged[str].connect(self.create_btn_status)
        self.new_category_input.setDisabled(True)
        # Create Button
        self.create_button =  QtWidgets.QPushButton('Create', self)
        self.create_button.setDisabled(True)
        self.create_button.clicked.connect(self.create_new_category)

        # Category Tree View
        self.category_view = QtWidgets.QTreeWidget(self)
        self.category_view.setHeaderLabel('Categories')
        self.category_view.setSortingEnabled(True)
        self.category_view.sortByColumn(0,QtCore.Qt.SortOrder.AscendingOrder)
        self.category_view.setAlternatingRowColors(True)
        self.category_view.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred)

        # Organize button and label
        self.organization_label = QtWidgets.QLabel('This operation cannot be undone!')
        self.organization_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.organization_label.setFont(self.itallic_font)
        self.organization_label.setWordWrap(True)
        self.organization_label.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding)
        self.organize_button = QtWidgets.QPushButton('Organize', self)
        self.organize_button.setFont(self.big_font)
        self.organize_button.setFixedWidth(125)
        self.organize_button.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Preferred)
        self.organize_button.clicked.connect(self.organize_warning_popup)
        self.organize_button.setDisabled(True)


        # Image Viewer Label and Scroll Area
        self.scrolling_display_area = QtWidgets.QScrollArea(self)
        self.scrolling_display_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrolling_display_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrolling_display_area.setWidgetResizable(True)

        self.image_display = QLabel(self)
        self.image_display.setScaledContents(False)
        self.image_display.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.scrolling_display_area.setWidget(self.image_display)

        # Image Navigation Buttons
        self.previous_button = QtWidgets.QPushButton("<", self)
        self.previous_button.setFont(self.big_font)
        self.previous_button.setMaximumWidth(25)
        self.previous_button.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Preferred)
        self.previous_button.clicked.connect(self.previous_image)
        self.previous_button.setDisabled(True)

        self.next_button = QtWidgets.QPushButton(">", self)
        self.next_button.setFont(self.big_font)
        self.next_button.setMaximumWidth(25)
        self.next_button.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Preferred)
        self.next_button.clicked.connect(self.next_image)
        self.next_button.setDisabled(True)

        # status bar
        self.loading_msg_label = QLineEdit(self)
        self.loading_msg_label.setStyleSheet(
            "border: 1px solid rgb(42,42,42); background-color:transparent; color: rgb(127,127,127);")
        self.loading_msg_label.setText("")
        self.loading_msg_label.setDisabled(True)
        self.loading_msg_label.setFont(self.itallic_font)
        self.loading_msg_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed)
        self.loading_msg_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.loading_msg_label.textChanged[str].connect(self.loading_msg_check)

        # version number
        self.version_label = QLineEdit(self)
        self.version_label.setStyleSheet(
            "border: 1px solid rgb(42,42,42); background-color:transparent; color: rgb(127,127,127);")
        self.version_label.setText('Created by: Daniel Lukas v0.3.2alpha')
        self.version_label.setDisabled(True)
        self.version_label.setFont(self.itallic_font)
        self.version_label.setFixedWidth(225)
        self.version_label.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed)
        self.version_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

    #######################################################################
    ##############################  Layout  ###############################
    #######################################################################

        # creates the main layout
        self.main_layout = QtWidgets.QVBoxLayout()

        # creates the right_layout and adds objects
        self.right_frame = QtWidgets.QFrame(self)
        self.right_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.right_frame.setSizePolicy(
                QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Preferred)
        self.right_layout = QtWidgets.QVBoxLayout(self.right_frame)

        # selection Layout
        self.top_frame = QtWidgets.QFrame(self)
        self.top_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.top_frame.setSizePolicy(
                QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Fixed)
        self.path_selection_layout = QtWidgets.QHBoxLayout(self.top_frame)
        self.path_selection_layout.addWidget(self.browse_button)
        self.path_selection_layout.addWidget(self.selection_input)
        self.path_selection_layout.addWidget(self.import_button)

        # Create the main Display and Navigation Layout
        self.image_nav_layout = QtWidgets.QHBoxLayout()
        self.image_nav_layout.addWidget(self.previous_button, 0)
        self.image_nav_layout.addWidget(self.scrolling_display_area, 4)
        self.image_nav_layout.addWidget(self.next_button, 0)

        # add selection layout to right_layout
        self.right_layout.addLayout(self.image_nav_layout)

        # Category Layout
        self.left_frame = QtWidgets.QFrame(self)
        self.left_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.left_layout = QtWidgets.QVBoxLayout(self.left_frame)

        # creates category_new layout
        self.category_create_new_layout = QtWidgets.QHBoxLayout()
        self.category_create_new_layout.addWidget(self.new_category_input)
        self.category_create_new_layout.addWidget(self.create_button)

        self.left_layout.addLayout(self.category_create_new_layout, 0)
        self.left_layout.addWidget(self.category_view, 1)
        self.left_layout.addWidget(self.organize_button,0, QtCore.Qt.AlignmentFlag.AlignCenter)

        # Creates the horizontal splitter
        self.horizontal_splitter = QSplitter(QtCore.Qt.Orientation.Horizontal)
        self.horizontal_splitter.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred)
        self.horizontal_splitter.addWidget(self.left_frame)
        self.horizontal_splitter.addWidget(self.right_frame)
        self.horizontal_splitter.setStretchFactor(1,5)
        self.horizontal_splitter.setSizes([300,960])
        self.horizontal_splitter.setCollapsible(0, False)
        self.horizontal_splitter.setCollapsible(1, False)

        # Grid View Scroll Area
        self.scrolling_grid_area = QtWidgets.QScrollArea(self)
        self.scrolling_grid_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrolling_grid_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrolling_grid_area.setWidgetResizable(True)

        self.bottom_frame = QtWidgets.QFrame(self)
        self.bottom_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.bottom_frame.setSizePolicy(
                QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Minimum)
        self.bottom_layout = QtWidgets.QHBoxLayout(self.bottom_frame)
        self.bottom_layout.setSpacing(10)
        self.scrolling_grid_area.setWidget(self.bottom_frame)

        # Creates the vertical splitter
        self.vertical_splitter = QSplitter(QtCore.Qt.Orientation.Vertical)
        self.vertical_splitter.addWidget(self.horizontal_splitter)
        self.vertical_splitter.addWidget(self.scrolling_grid_area)
        self.vertical_splitter.setStretchFactor(10,1)
        self.vertical_splitter.setSizes([635,210])
        self.vertical_splitter.setCollapsible(0, False)
        self.vertical_splitter.setCollapsible(1, False)

        # status area
        self.status_layout = QtWidgets.QHBoxLayout()
        self.status_layout.addWidget(self.loading_msg_label,3)
        self.status_layout.addWidget(self.version_label,1)
        # add sub_layouts to main layout
        self.main_layout.addWidget(self.top_frame)
        self.main_layout.addWidget(self.vertical_splitter)
        self.main_layout.addLayout(self.status_layout)
        # sets the parent/main layout
        self.setLayout(self.main_layout)

        self.build_selector()

    def load_btn_status(self):
        ''' Disables and enables the load button when the conditions are met '''
        if self.selection_input.text() != "":
            self.import_button.setDisabled(False)
        elif self.selection_input.text() == "":
            self.import_button.setDisabled(True)

    def folder_select(self):
        ''' Assignes the selected path to the input box '''
        self.chosen_directory = QFileDialog.getExistingDirectory(self)
        if self.chosen_directory != "":
            self.selection_input.clear()
        self.selection_input.insert(self.chosen_directory)
        self.input_text = self.selection_input.text()

    def loading_msg_check(self):
        ''' Clears all images and executes the build dictionary function when the status bar reads "Importing Images... '''
        if "Importing Images . . ." in self.loading_msg_label.text():
            QApplication.processEvents()
            if self.bottom_layout.count() != 0:
                self.clear_thumbnails()
                self.clear_img_display()
            self.build_dict()

    def create_working_directory(self):
        ''' Assigns the input path to the current working directory '''
        if os.path.exists(self.selection_input.text()) and self.selection_input.text() != "":
            self.input_text = self.selection_input.text()
            self.working_directory = self.input_text
            os.chdir(self.working_directory)
            self.clear_categories_tree()
            self.clear_cat_selector()
            self.loading_msg_label.setText("Importing Images . . .")
        else:
            self.invalid_path = QMessageBox(self)
            self.invalid_path.warning(self, "Attention", "Invalid file path!")

    def add_wd_to_tree(self):
        ''' Adds the working directory as the root item in the category view '''
        self.current_os = platform.system()

        if "/" in self.working_directory:
            self.clear_categories_tree()
            self.image_folder = self.working_directory.split("/")[-1]
            self.WD_item = QtWidgets.QTreeWidgetItem(self.category_view, [self.image_folder])
            self.WD_item.setExpanded(True)
            self.category_view.addTopLevelItem(self.WD_item)
            self.new_category_input.setDisabled(False)
        elif "\\" in self.working_directory:
            self.clear_categories_tree()
            self.image_folder = self.working_directory.split("\\")[-1]
            self.WD_item = QtWidgets.QTreeWidgetItem(self.category_view, [self.image_folder])
            self.category_view.addTopLevelItem(self.WD_item)

    def create_new_category(self):
        ''' Adds a new category to the category_view and category_selector widgets '''

        if self.new_category_input.text() != "":
            self.category = QtWidgets.QTreeWidgetItem(self.WD_item,[self.new_category_input.text()])
            self.category_view.addTopLevelItem(self.category)
            self.category_selector.addItem(self.new_category_input.text())
            self.category_selector.model().sort(0, QtCore.Qt.SortOrder.AscendingOrder)
            self.new_category_input.clear()
            QApplication.processEvents()
            self.interactive_widgets_status()

    def create_btn_status(self):
        ''' Disables and enables the create button when the conditions are met '''

        if self.new_category_input.text() != "":
            self.create_button.setDisabled(False)
        elif self.new_category_input.text() == "":
            self.create_button.setDisabled(True)

    def build_dict(self):
        ''' Creates all the dictionaries, lists, and sets to be used,
        then populates lists with names of supported image files in the working directory '''

        # creates a list that will get populated with filenames
        self.image_files = []
        self.sorted_image_files = []
        self.image_index_list = []
        self.thumb_list = []
        self.file_operation_dict = {}
        self.category_folder_set = set()

        self.reset_image_list()

        # populates lists with the names of all supported images files in the working directory
        for self.file_name in os.listdir():
            self.img_extention_check()
            if self.img_extention_check() == False: continue
            self.image_files.append(self.file_name)
            self.sorted_image_files = sorted(self.image_files, key=str.lower,)
        if self.sorted_image_files != []:
            self.populate_grid_view()
            self.display_images()
            self.add_wd_to_tree()
        elif self.sorted_image_files == []:
            self.loading_msg_label.setText("No valid image files found. Please choose a different folder.")

        self.cat_sel_func()

    def display_images(self):
        ''' Displays the first image in the directory '''

        self.import_button.setDisabled(True)
        self.interactive_widgets_status()
        self.image_index = 0
        self.image = QImage(self.thumb_list[self.image_index])
        self.image_display.setPixmap(QPixmap(self.image).scaled(
            700, 700, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.get_current_image()
        self.highlight_selected()


    def img_extention_check(self):
        ''' Checks all files in the working directory for supported image formats '''

        self.img_extentions = ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'pbm', 'pgm', 'ppm', 'tif', 'xbm', 'xpm']
        self.three_char_extention = self.file_name[-3:]
        self.four_char_extention = self.file_name[-4:]
        if self.three_char_extention in self.img_extentions or self.four_char_extention in self.img_extentions:
            return True
        elif self.three_char_extention not in self.img_extentions or self.four_char_extention not in self.img_extentions:
            return False

    def previous_image(self):
        ''' Allows for backward navigation '''

        if self.image_index != 0:
            self.image_index = self.image_index-1
            self.image = QImage(self.thumb_list[self.image_index])
            self.image_display.setPixmap(QPixmap(self.image).scaled(
                700, 700, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            self.unhighlight_all()
            self.highlight_selected()
        self.get_current_image()
        self.show_category_if_categorized()

    def next_image(self):
        ''' Allows for forward navigation '''

        if self.image_index < len(self.sorted_image_files)-1:
            self.image_index = self.image_index+1
            self.image = QImage(self.thumb_list[self.image_index])
            self.image_display.setPixmap(QPixmap(self.image).scaled(
                700, 700, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            self.unhighlight_all()
            self.highlight_selected()
        self.get_current_image()
        self.show_category_if_categorized()

    def build_selector(self):
        ''' Creates the selection menu for the categories '''

        # Category Selector
        self.category_selector = QtWidgets.QComboBox(self)
        self.category_selector.setDisabled(True)
        self.category_selector.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed)
        # Add Button
        self.add_button =  QtWidgets.QPushButton('Add', self)
        self.add_button.setSizePolicy(
            QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Fixed)
        self.add_button.clicked.connect(self.build_file_operation_dict)
        self.add_button.setDisabled(True)
        # Creates the category selector layout
        self.cat_frame = QtWidgets.QFrame(self)
        self.cat_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.cat_frame.setSizePolicy(
                QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Fixed)
        self.cat_sel_layout = QtWidgets.QHBoxLayout(self.cat_frame)
        self.cat_sel_layout.addWidget(self.category_selector)
        self.cat_sel_layout.addWidget(self.add_button)
        # Adds the selector to right layout
        self.right_layout.addWidget(self.cat_frame)

    def cat_sel_func(self):
        ''' runs the funtion when the category selection changes '''
        self.category_selector.currentIndexChanged.connect(self.interactive_widgets_status)

    def set_category_index(self):
        ''' finds the index of the selected category item '''
        self.category_name = self.category_selector.currentText()
        self.category_index = self.category_selector.findText(self.category_name, QtCore.Qt.MatchFlag.MatchFixedString)
        self.category_selector.setCurrentIndex(self.category_index)

    def add_btn_status(self):
        ''' Disables and enables the add button when the conditions are met '''

        if self.category_index != 0:
            self.add_button.setDisabled(False)
        elif self.category_index == 0:
            self.add_button.setDisabled(True)

    def interactive_widgets_status(self):
        ''' Enables or disables all widgets with conditional dependencies '''

        self.set_category_index()
        self.add_btn_status()
        if self.sorted_image_files != []:
            self.previous_button.setDisabled(False)
            self.next_button.setDisabled(False)
            self.category_selector.setDisabled(False)
        else:
            self.previous_button.setDisabled(True)
            self.next_button.setDisabled(True)
            self.add_button.setDisabled(True)
            self.category_selector.setDisabled(True)

    def get_current_image(self):
        ''' Adds the current image file to a variable'''
        self.current_image = self.sorted_image_files[self.image_index]

    def populate_grid_view(self):
        ''' creates the thumbnails of every supported image in the working directory '''

        for self.image_index, self.file_name in enumerate(self.sorted_image_files):
            self.thumb_main_img = QImage(self.sorted_image_files[self.image_index])
            self.thumb_img = QLabel(self)
            self.thumb_txt = QLabel(self.file_name, self)
            self.image_index_list.append(self.image_index)
            self.thumb_txt.setSizePolicy(
                QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.MinimumExpanding)
            self.thumb_txt.setWordWrap(True)
            self.thumb_img.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.thumb_txt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.thumb_img.setPixmap(QPixmap(self.thumb_main_img).scaled(
                125, 125, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            self.thumb_frame = ClickFrame(self)
            self.thumb_frame.clicked.connect(self.thumbnail_click)
            self.thumb_frame.setSizePolicy(
                QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Fixed)
            # assigns a name to every frame created so that they are directly accessible
            self.thumb_frame.setObjectName(self.file_name)
            self.thumb_list.append(self.thumb_frame.objectName())
            self.thumb_layout = QtWidgets.QVBoxLayout(self.thumb_frame)
            self.thumb_layout.addWidget(self.thumb_img)
            self.thumb_layout.addWidget(self.thumb_txt)
            self.bottom_layout.addWidget(self.thumb_frame)
            self.thumb_dict = dict(zip(self.thumb_list, self.image_index_list))
            QApplication.processEvents()
        self.loading_msg_label.setText("Import complete")

    def unhighlight_all(self):
        ''' sets style of unselected thumbnails '''
        for i in range(len(self.bottom_layout)):
            self.thumb = self.bottom_layout.itemAt(i).widget()
            self.thumb.setStyleSheet("border: none;")

    def highlight_selected(self):
        ''' sets the style of the selected thumbnail '''
        self.thumb_selected = self.findChild(ClickFrame, self.thumb_list[self.image_index])
        self.thumb_selected.setStyleSheet("border: 1px solid rgb(42, 130, 218); background-color: rgb(42, 130, 218); color: white;")
        print(self.thumb_list[self.image_index])

    def thumbnail_click(self):
        ''' Get thumbnail that was clicked '''

        self.clicked = self.sender()
        self.image_index = self.thumb_dict[self.clicked.objectName()]
        self.image = QImage(self.thumb_list[self.image_index])
        self.image_display.setPixmap(QPixmap(self.image).scaled(
                700, 700, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        print(self.clicked.objectName())
        self.unhighlight_all()
        self.show_category_if_categorized()
        #sets the style of the selected thumbnail
        self.clicked.setStyleSheet("border: 1px solid rgb(42, 130, 218); background-color: rgb(42, 130, 218); color: white;")

    def build_file_operation_dict(self):
        ''' Populates the dictionary that all file operations reference '''

        self.get_current_image()
        if self.file_operation_dict == {}:
            self.file_operation_dict = {self.current_image : self.category_name}
        else:
            self.file_operation_dict[self.current_image] = self.category_name
        self.loading_msg_label.setText(f"{self.current_image} added to {self.category_name}")
        print(self.file_operation_dict)
        self.organization_btn_status()

    def show_category_if_categorized(self):
        ''' If an image has been added to a category,
        that category becomes the current item in the selector when the image is selected '''

        self.get_current_image()
        if self.current_image in self.file_operation_dict.keys():
            self.category_index = self.category_selector.findText(self.file_operation_dict[self.current_image], QtCore.Qt.MatchFlag.MatchFixedString)
            self.category_selector.setCurrentIndex(self.category_index)
        else:
            self.category_selector.setCurrentIndex(0)

    def organization_btn_status(self):
        ''' Disables and enables the organize button when the conditions are met '''
        if len(self.file_operation_dict) != 0:
            self.organize_button.setDisabled(False)
        else:
            self.organize_button.setDisabled(True)

    def organize_warning_popup(self):
        ''' Displays a popup message to make sure user wants to execute file operations '''
        self.last_chance_message_box = QMessageBox(self)
        self.last_chance_message_box.setWindowTitle("WARNING!")
        self.last_chance_message_box.setIcon(QMessageBox.Icon.Warning)
        self.last_chance_message_box.setText("This operation cannot be undone! Do you wish to continue?")
        self.last_chance_message_box.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
        self.yes_button = self.last_chance_message_box.button(QMessageBox.StandardButton.Yes)
        self.no_button = self.last_chance_message_box.button(QMessageBox.StandardButton.No)
        self.no_button.setText("Cancel")

        self.last_chance_message_box.exec()

        if self.last_chance_message_box.clickedButton() == self.yes_button:
            self.organize_images()

    def warning_button_clicked(self):
        ''' If the user clicks the yes button, the file operations are executed '''
        if self.warning_popup == QMessageBox.StandardButton.Yes:
            self.organize_images()
        elif self.warning_popup == QMessageBox.Cancel:
            self.last_chance_message_box.Ignore()

    def organize_images(self):
        ''' Creates a folder in the working directory for every category,
        and the moves all images to the folder of the category they're added to. '''
        rename = self.rename_popup()
        
        for self.current_image, self.category_name in self.file_operation_dict.items():
                self.category_folder_set.add(self.category_name)

        for self.category_name in self.category_folder_set:
            os.mkdir(f"{self.category_name}")
        
        for self.current_image, self.category_name in self.file_operation_dict.items():
            if self.current_os == "Linux" or self.current_os == "Darwin":
                shutil.move(self.current_image, f"{self.working_directory}/{self.category_name}")
            else:
                shutil.move(self.current_image, f"{self.working_directory}\\{self.category_name}")
        
        if rename:
            for folder in self.category_folder_set:

                if self.current_os == "Linux" or self.current_os == "Darwin":
                    os.chdir(f"{self.working_directory}/{folder}")
                else:
                    os.chdir(f"{self.working_directory}\\{folder}")
      
                index = 0
                for f in os.listdir():
                    f_name, f_ext = os.path.splitext(f)
                    new_name = "{}{}{}{}".format(folder, "0", index, f_ext)
                    os.rename(f, new_name)
                    index += 1
            os.chdir(self.working_directory)

################################  Rename Files  ###################################

    def rename_popup(self):
        ''' Displays a popup message to ask if files should be renamed by category '''
        self.rename_message_box = QMessageBox(self)
        self.rename_message_box.setWindowTitle("WARNING!")
        self.rename_message_box.setIcon(QMessageBox.Icon.Warning)
        self.rename_message_box.setText("Would you like to rename files by category?")
        self.rename_message_box.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
        self.rename_yes_button = self.rename_message_box.button(QMessageBox.StandardButton.Yes)
        self.no_button = self.rename_message_box.button(QMessageBox.StandardButton.No)
        self.no_button.setText("No")

        self.rename_message_box.exec()

        if self.rename_message_box.clickedButton() == self.rename_yes_button:
            return True
        else: return False



#######################################################################
#############  Functions that remove and delete things   ##############
#######################################################################

    def reset_image_list(self):
        ''' Clears the list of image file names '''
        if self.image_files != []:
            self.selection_input.setText("")
            self.image_files.clear()

    def clear_thumbnails(self):
        ''' Removes all thumbnails that have previously been created. '''
        for i in reversed(range(self.bottom_layout.count())):
            self.bottom_layout.itemAt(i).widget().deleteLater()
            QApplication.processEvents()

    def clear_img_display(self):
        ''' Removes the image in the main display '''
        self.image_display.clear()

    def clear_categories_tree(self):
        ''' Removes all items from the category view widget '''
        self.category_view.clear()

    def clear_cat_selector(self):
        ''' Removes all items from the selection menu '''
        self.category_selector.clear()
        QApplication.processEvents()
        self.category_selector.addItem("--Select Category--")
        self.set_category_index()

if __name__ == '__main__':
    # Translate asset paths to useable format for PyInstaller
    def resource_path(relative_path):
        ''' This is a workaround by Aaron Tan
        from his blog https://blog.aaronhktan.com/posts/2018/05/14/pyqt5-pyinstaller-executable '''
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(resource_path('image-organizer-icon.png')))
    win = MainWindow()
    # qtmodern.styles.dark(app)
    win.show()
    sys.exit(app.exec())
