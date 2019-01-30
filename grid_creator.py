# -*- coding: utf-8 -*-
#
# Form implementation generated from reading ui file 'Grid_Creator.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QListWidget, QListWidgetItem, QSpinBox, QTextEdit,
                             QVBoxLayout, QMessageBox, QMainWindow, QMouseEventTransition)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
import tkinter as tk
from tkinter import filedialog
import numpy as np
import sys
from os import rename
from PIL import Image, ImageDraw
import math
import pandas as pd
import cv2 as cv2
import getpass
from sys import platform


class Ui_MainWindow(object):

    def __init__(self):

        # set INIT values for fov cent, img, and pix2deg (DEFAULT MAIA)
        self.fov_cent_x = 245
        self.fov_cent_y = 241
        self.current_img = 'maia_od_r.png'
        self.pix2deg = .0356 * 2
        self.x_loc = []
        self.y_loc = []
        self.scotopic = 0

    def clear_gui(self):

        # Rerun init parameters
        self.fov_cent_x = 245
        self.fov_cent_y = 241
        self.current_img = 'maia_od_r.png'
        self.label_4.setPixmap(QtGui.QPixmap("maia_od_r.png"))
        self.pix2deg = .0356 * 2

        self.clear_table()
        self.radioButton_3.setChecked(True)# MAIA
        self.pushButton_7.setEnabled(False)
        self.pushButton_8.setEnabled(False)

        # Set Table back to '-' '-'

    def clear_table(self):
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setRowCount(1)

        item = QtWidgets.QTableWidgetItem('1')
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('X Degrees')
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('Y Degees')
        self.tableWidget_2.setHorizontalHeaderItem(1, item)

        self.temp_empt1 = QtWidgets.QTableWidgetItem('-')
        self.temp_empt2 = QtWidgets.QTableWidgetItem('-')

        self.tableWidget_2.setItem(0, 0, self.temp_empt1)
        self.tableWidget_2.setItem(0, 1, self.temp_empt2)

        # Disable 'Display Grid' button
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)

        # Set grid coords back to empty for diplay grid
        self.x_loc = []
        self.y_loc = []


    def my_error(self):  # Not currently working

        self.error_dialog = QtWidgets.QErrorMessage()
        self.error_dialog.showMessage(self.my_error_dlg)

    #OBTAIN CURRENT IMAGE ON GUI
    def get_curr_img(self):

        if self.radioButton_3.isChecked(): # MAIA
            if self.radioButton_2.isChecked():
                self.label_4.setPixmap(QtGui.QPixmap("maia_od_r.png"))
                self.current_img = "maia_od_r.png"
                self.fov_cent_x = 245
                self.fov_cent_y = 241
            elif self.radioButton.isChecked():
                self.label_4.setPixmap(QtGui.QPixmap("maia_os_r.png"))
                self.current_img = "maia_os_r.png"
                self.fov_cent_x = 254
                self.fov_cent_y = 237
            self.pix2deg = 0.0356 * 2.5
            try: # Try and Display the grid
                self.display_grid()
            except:
                print('doesnt exist yet')

        elif self.radioButton_4.isChecked():
            if self.radioButton_2.isChecked():
                self.label_4.setPixmap(QtGui.QPixmap("mp_od_r.png"))
                self.current_img = "mp_od_r.png"
                self.fov_cent_x = 237
                self.fov_cent_y = 262
            elif self.radioButton.isChecked():
                self.label_4.setPixmap(QtGui.QPixmap("mp_os_r.png"))
                self.current_img = "mp_os_r.png"
                self.fov_cent_x = 275
                self.fov_cent_y = 270
            self.pix2deg = 0.0356 * 3
            try:
                self.display_grid()
            except:
                print('doesnt exist yet')

        if self.checkBoxGrid.isChecked():
            self.grid_lines()

    def display_grid(self):

        self.myIm = cv2.imread(str(self.current_img))

        self.current_ind = 0
        self.my_rad = math.sqrt(.43 / math.pi)
        self.r = round(self.my_rad / self.pix2deg)

        self.x_pix = (self.x_loc[self.current_ind] / self.pix2deg) + self.fov_cent_x
        self.y_pix = (self.y_loc[self.current_ind] / self.pix2deg) + self.fov_cent_y
        self.x_pix = round(self.x_pix)
        self.y_pix = round(self.y_pix)

        self.x_pix = int(self.x_pix)  # gives you '5.6'
        self.y_pix = int(self.y_pix)  # gives you '5.6'
        #print(self.r, self.x_pix, self.y_pix)

        while self.current_ind < len(self.x_loc):
            #print('working on... {}'.format(self.current_ind))

            self.x = int((self.x_loc[self.current_ind] / self.pix2deg) + self.fov_cent_x)
            self.y = int((self.y_loc[self.current_ind] / self.pix2deg) + self.fov_cent_y)

            if self.radioButton_3.isChecked():
                cv2.circle(self.myIm, (self.x, self.y), self.r, (100, 255, 0), -1)
            elif self.radioButton_4.isChecked():

                self.sq_x_1 = int((self.x - (self.r/2)))
                self.sq_y_1 = int((self.y - (self.r/2)))
                self.sq_x_2 = int((self.x + (self.r/2)))
                self.sq_y_2 = int((self.y + (self.r/2)))

                cv2.rectangle(self.myIm, (self.sq_x_1, self.sq_y_1), (self.sq_x_2, self.sq_y_2), (170, 190, 0), -1)
            # except:
            #     print('Unable to print point {} Coord X: {} Coord Y: {}'.format(self.current_ind,
            #                                                                     self.x, self.y))
            # print('worked for {}'.format(self.current_ind))

            # self.draw.ellipse((self.x_pix-self.r, self.y_pix-self.r,
            #             self.x_pix+self.r, self.y_pix+self.r), fill=(0,255,0,250))
            self.current_ind += 1
        cv2.imwrite('disp_grid.png', self.myIm)
        self.current_img = 'disp_grid.png'
        self.label_4.setPixmap(QtGui.QPixmap('disp_grid.png'))

        if self.checkBoxGrid.isChecked():
            self.grid_lines()

    def open_excel(self):

        # This opens the excel document with X coordinates in column A and Y in column B
            # Must include Headers

        try:
            # Instantiate TK window to open .xlsx files
            self.root = tk.Tk()
            self.root.withdraw()
            self.excel_filename = filedialog.askopenfilename(filetypes=(("Excel files", "*.xlsx")
                                                                        , ("All files", "*.*")))
            self.excel_file = self.excel_filename

            # Clear GUI table
            self.clear_table()
            self.get_curr_img()

            # Tag to determine if the exam is scotopic
            self.scotopic = 0  # 0 = No / 1 = Yes

            # Get filename
            self.excel_split = self.excel_file.split('/')
            self.my_file_name = self.excel_split[-1]
            self.my_file_name = self.my_file_name[0:-5]

            print('Excel File: {}'.format(self.excel_file))

            # Open excel and convert to numpy array
            self.df = pd.read_excel(open(self.excel_file, 'rb'))
            self.arrays = np.array(self.df)

            # Move to specific X and Y coordinate arrays
            self.x_loc_numpy = self.arrays[:, 0]
            self.y_loc_numpy = self.arrays[:, 1]
            self.x_loc_raw = []
            self.y_loc_raw = []

            self.current_ind = 0

            # Put into normal python lists
            while self.current_ind < len(self.x_loc_numpy):
                self.x_loc_raw.append(float(self.x_loc_numpy[self.current_ind]))
                self.y_loc_raw.append(float(self.y_loc_numpy[self.current_ind]))
                self.current_ind += 1

            self.x_loc = []
            self.y_loc = []

            refine_ind = 0

            #Check values for bool, out of bounds (> ro < 20), or str
            while refine_ind < len(self.x_loc_raw):
                if isinstance(self.x_loc_raw[refine_ind], bool) or isinstance(self.y_loc_raw[refine_ind], bool):
                    print('Bool Present')
                    break
                elif isinstance(self.x_loc_raw[refine_ind], str) or isinstance(self.y_loc_raw[refine_ind], str):
                    print('String Present')
                    break
                elif isinstance(self.x_loc_raw[refine_ind], int) or isinstance(self.y_loc_raw[refine_ind], float):
                    if (self.x_loc_raw[refine_ind] > 20 or self.y_loc_raw[refine_ind] > 20 or
                    self.x_loc_raw[refine_ind] < -20 or self.y_loc_raw[refine_ind] < -20):
                        print('Value X: {} Values Y: {} OUT OF BOUNDS'.format(self.x_loc_raw[refine_ind],
                                                                              self.y_loc_raw[refine_ind]))
                        print('Number is out of bounds')
                        break
                    else:
                        self.x_loc.append(self.x_loc_raw[refine_ind])
                        self.y_loc.append((self.y_loc_raw[refine_ind]))
                refine_ind += 1

            self.coord_array = []
            self.ind_dup = []
            self.coord_ind = 0

            #Remove duplicaters to render final coordinates
            while self.coord_ind < len(self.x_loc):
                self.temp_x = self.x_loc[self.coord_ind]
                self.temp_y = self.y_loc[self.coord_ind]

                self.temp_x = round(self.temp_x, 2)
                self.temp_y = round(self.temp_y, 2) # To get Y axis correct
                self.new_val = [self.temp_x, self.temp_y]

                if self.new_val not in self.coord_array:
                    self.coord_array.append(self.new_val)
                self.coord_ind += 1

            # Enable write if textbox str exists
            # if len(self.textbox.text()) > 0:
            #     self.pushButton2.setEnabled(True)

            temp_ind = 0
            self.tableWidget_2.setRowCount(len(self.coord_array))

            # Update Table Widget with coordinates
            while temp_ind < len(self.coord_array):
                x = self.coord_array[temp_ind]
                self.temp_x = '%.1f' % round(x[0], 1) # gives you '5.6'
                self.temp_y = '%.1f' % round(x[1], 1) # gives you '5.6'

                self.temp_x = QtWidgets.QTableWidgetItem(str(self.temp_x))
                self.temp_y = QtWidgets.QTableWidgetItem(str(self.temp_y))

                self.tableWidget_2.setItem(temp_ind, 0, self.temp_x)
                self.tableWidget_2.setItem(temp_ind, 1, self.temp_y)
                temp_ind += 1

            try:
                self.display_grid()
                self.pushButton_3.setEnabled(True)
                self.pushButton_4.setEnabled(True)
                self.pushButton_7.setEnabled(True)
                self.pushButton_8.setEnabled(True)

            except:
                print('Clearing table...')
                self.clear_table()
                self.my_error_dlg = 'Unable to display grid'
                self.my_error()

        except:
            self.my_error_dlg = 'Unable to load grid information'
            self.my_error()

    def update_table(self):
        temp_ind = 0
        self.tableWidget_2.setRowCount(len(self.x_loc))

        # Update Table Widget with coordinates
        while temp_ind < len(self.x_loc):
            x = self.x_loc[temp_ind]
            y = self.y_loc[temp_ind]
            self.temp_x = '%.1f' % round(x, 1)  # gives you '5.6'
            self.temp_y = '%.1f' % round(y, 1)  # gives you '5.6'

            self.temp_x = QtWidgets.QTableWidgetItem(str(self.temp_x))
            self.temp_y = QtWidgets.QTableWidgetItem(str(self.temp_y))

            self.tableWidget_2.setItem(temp_ind, 0, self.temp_x)
            self.tableWidget_2.setItem(temp_ind, 1, self.temp_y)
            temp_ind += 1


    def getPos(self, event):

        self.x = int(event.pos().x())
        self.y = int(event.pos().y())
        print('X: {} Y: {}'.format(self.x, self.y))

        if self.checkBox.isChecked():
            self.my_rad = math.sqrt(.43 / math.pi)
            self.r = round(self.my_rad / self.pix2deg)

            self.myIm = cv2.imread(str(self.current_img))

            if self.radioButton_3.isChecked(): # MAIA
                cv2.circle(self.myIm, (self.x, self.y), self.r, (100, 255, 0), -1)
            elif self.radioButton_4.isChecked():
                self.sq_x_1 = int((self.x - (self.r / 2)))
                self.sq_y_1 = int((self.y - (self.r / 2)))
                self.sq_x_2 = int((self.x + (self.r / 2)))
                self.sq_y_2 = int((self.y + (self.r / 2)))

                cv2.rectangle(self.myIm, (self.sq_x_1, self.sq_y_1), (self.sq_x_2, self.sq_y_2), (170, 190, 0), -1)

            cv2.imwrite('disp_grid.png', self.myIm)
            self.label_4.setPixmap(QtGui.QPixmap('disp_grid.png'))
            self.current_img = 'disp_grid.png'

            self.x_add = round(((self.x - self.fov_cent_x) * self.pix2deg), 1)
            self.y_add = round(((self.y - self.fov_cent_y) * self.pix2deg), 1)# To get Y axis correct

            self.x_loc.append(self.x_add)
            self.y_loc.append(self.y_add)

            #self.y_add_table = self.y_add * - 1 # To get Y axis correct

            self.current_row_len = self.tableWidget_2.rowCount()
            print(self.current_row_len)

            self.temp_x = QtWidgets.QTableWidgetItem(str(self.x_add))
            self.temp_y = QtWidgets.QTableWidgetItem(str(self.y_add))

            # CURRENT ROW self.curr_item = self.tbl_anggota.currentRow()

            self.current_item = self.tableWidget_2.item(0, 0).text()
            print(self.current_item)

            if self.current_item == '-':
                self.tableWidget_2.setItem(0, 0, self.temp_x)
                self.tableWidget_2.setItem(0, 1, self.temp_y)
            else:
                self.tableWidget_2.setRowCount((self.current_row_len)+1)
                self.tableWidget_2.setItem(int(self.current_row_len), 0, self.temp_x)
                self.tableWidget_2.setItem(int(self.current_row_len), 1, self.temp_y)

            self.pushButton_4.setEnabled(True)
            self.pushButton_7.setEnabled(True)
            self.pushButton_8.setEnabled(True)

    def print_test(self):
        print(self.x_loc)

    def flip_x(self):
        if not self.x_loc:
            pass
        else:
            self.x_loc = [i * -1 for i in self.x_loc]
            self.get_curr_img()
            self.display_grid()
            self.update_table()
            print('Flip X')

    def flip_y(self):
        if not self.y_loc:
            pass
        else:
            self.y_loc = [i * -1 for i in self.y_loc]
            self.get_curr_img()
            self.display_grid()
            self.update_table()
            print('Flip Y')

    def grid_lines(self):

        self.myIm = cv2.imread(str(self.current_img))

        circle_ind = 2

        if self.radioButton_3.isChecked():
            self.grid_color = (255, 255, 255)
        else:
            self.grid_color = (40, 40, 150)

        while circle_ind < 22:

            self.r = int(circle_ind/self.pix2deg)
            cv2.circle(self.myIm, (self.fov_cent_x, self.fov_cent_y), self.r, self.grid_color)

            circle_ind += 2

        cv2.line(self.myIm, (0, self.fov_cent_y), (512, self.fov_cent_y), self.grid_color)
        cv2.line(self.myIm, (self.fov_cent_x, 0), (self.fov_cent_x, 512), self.grid_color)

        cv2.imwrite('with_grid.png', self.myIm)
        self.label_4.setPixmap(QtGui.QPixmap('with_grid.png'))
        self.current_img = 'with_grid.png'

    def new_table_value(self):
        print('working')

    def save_xml(self):
        self.username = getpass.getuser() # Get current username
        self.my_os = platform             # Get OS

        # Get desktop path
        if self.my_os == 'darwin':
            self.desk_path = r'/Users/' + self.username + '/Desktop/'
        elif self.my_os == 'win32':
            self.desk_path = r'C:/Users/' + self.username + '/Desktop/'

        # Gets name from GUI edit text field
        self.my_gridname = self.textEdit.toPlainText()

        # If no name in GUI edit text default to 'new_grid'
        if len(self.my_gridname) == 0:
            self.my_gridname = 'new_grid'

        # Full path of new file
        self.new_file = self.desk_path + self.my_gridname + '.txt'

        # Print to verify new file path exists
        print(self.new_file)
        print(isfile(self.new_file))

        # If the new file currently exists throw an error and break
        if isfile(self.new_file):

            self.my_error_dlg = 'File Already Exists!'
            self.my_error()


        else:
            # Open blank .txt and begin writing headers for MAIA .xml
            self.my_file = open(self.new_file, 'w', encoding='utf-8-sig')

            self.my_file.write('<?xml version="1.0"?>\n')
            self.my_file.write('<!DOCTYPE MitCustomerPatterns>\n')
            self.my_file.write('<patterns>\n')

            if self.scotopic == 0:
                self.my_file.write('    <pattern_expert>\n')
            else:
                self.my_file.write('    <pattern_scotopic>\n')

            self.my_file.write('        <Grid name="' + self.my_gridname + '">\n')

            self.current_ind = 0

            self.x_loc_refine = []
            self.y_loc_refine = []
            self.refiner = []

            # Check for duplicates in the excel X and Y coordinates
                # This removes duplicates
            while self.current_ind < len(self.x_loc):
                self.new_val = [self.x_loc[self.current_ind], self.y_loc[self.current_ind]]

                if self.new_val not in self.refiner:
                    self.x_loc_refine.append(self.x_loc[self.current_ind])
                    self.y_loc_refine.append(self.y_loc[self.current_ind])
                else:
                    print('Duplicate at X: {} Y: {} Ind: {}'.format(self.x_loc[self.current_ind],
                                                                    self.y_loc[self.current_ind],
                                                                    self.current_ind))
                self.refiner.append(self.new_val)
                self.current_ind += 1

            self.current_ind = 0

            # Write stimulus coordinate lines in correct .xml format
            while self.current_ind < len(self.x_loc_refine):
                self.x_loc_str = str(self.x_loc_refine[self.current_ind])
                self.y_loc_str = str(self.y_loc_refine[self.current_ind])
                self.current_ind_str = self.current_ind + 1
                self.current_ind_str = str(self.current_ind_str)

                self.data_write = '            <Stimulus id="' + self.current_ind_str + '" x_deg="' + self.x_loc_str + '" y_deg="' + self.y_loc_str + '"/>\n'
                self.my_file.write(self.data_write)

                self.current_ind += 1

            # All outro .xml tags to write
            self.my_file.write('        </Grid>\n')
            if self.scotopic == 0:
                self.my_file.write('    </pattern_expert>\n')
            else:
                self.my_file.write('    </pattern_scotopic>\n')
            self.my_file.write('</patterns>\n')

            # Close and rename the .txt -> to .xml
            self.my_file.close()
            self.my_file_name = self.desk_path + self.my_gridname + '.xml'
            rename(self.new_file, self.my_file_name)

    def add_stims(self):
        self.current_row_len = self.tableWidget_2.rowCount()

        self.temp_x = QtWidgets.QTableWidgetItem(str('-'))
        self.temp_y = QtWidgets.QTableWidgetItem(str('-'))

        self.tableWidget_2.setRowCount((self.current_row_len) + 1)
        self.tableWidget_2.setItem(int(self.current_row_len), 0, self.temp_x)
        self.tableWidget_2.setItem(int(self.current_row_len), 1, self.temp_y)

    def test(self):
        print('wroks')

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(790, 555)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(190, 380, 120, 80))
        self.widget.setObjectName("widget")
        #
        # self.tableWidget = QtWidgets.QTableWidget(self.tab)
        # self.tableWidget.setGeometry(QtCore.QRect(40, 125, 168, 225))
        # self.tableWidget.setObjectName("tableWidget")
        # self.tableWidget.setColumnCount(2)
        # self.tableWidget.setRowCount(1)
        #
        # self.temp_zero = QtWidgets.QTableWidgetItem(str(0))
        #
        # item = QtWidgets.QTableWidgetItem('1      ')
        # self.tableWidget.setVerticalHeaderItem(0, item)
        # item = QtWidgets.QTableWidgetItem('X Degrees')
        # self.tableWidget.setHorizontalHeaderItem(0, item)
        # item = QtWidgets.QTableWidgetItem('Y Degees')
        # self.tableWidget.setHorizontalHeaderItem(1, item)
        #
        # self.temp_empt1 = QtWidgets.QTableWidgetItem('-')
        # self.temp_empt2 = QtWidgets.QTableWidgetItem('-')
        #
        # self.tableWidget.setItem(0, 0, self.temp_empt1)
        # self.tableWidget.setItem(0, 1, self.temp_empt2)
        #
        # # self.tableWidget.resizeRowToContents(1)
        # self.tableWidget.resizeColumnsToContents()

        # Coordinate Table
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(10, 210, 251, 281))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setRowCount(1)

        item = QtWidgets.QTableWidgetItem('1')
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('X Degrees')
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('Y Degees')
        self.tableWidget_2.setHorizontalHeaderItem(1, item)

        self.temp_empt1 = QtWidgets.QTableWidgetItem('-')
        self.temp_empt2 = QtWidgets.QTableWidgetItem('-')

        self.tableWidget_2.setItem(0, 0, self.temp_empt1)
        self.tableWidget_2.setItem(0, 1, self.temp_empt2)
        # self.tableWidget_2.selectRow.connect(self.test)

        # self.tableWidget.resizeRowToContents(1)
        #self.tableWidget_2.resizeColumnsToContents()

        # Grid Name Editor
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 40, 251, 31))
        self.textEdit.setObjectName("textEdit")

        # Image
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(270, 10, 512, 512))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("maia_od_r.png"))
        self.label_4.setObjectName("label_4")
        self.label_4.mousePressEvent = self.getPos

        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(150, 80, 111, 83))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.open_excel)
        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.display_grid)
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_3.setEnabled(False)

        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton_4.clicked.connect(self.save_xml)
        self.pushButton_4.setEnabled(False)


        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 500, 251, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.add_stims)


        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setGeometry(QtCore.QRect(10, 525, 251, 23))
        self.pushButton_6.clicked.connect(self.clear_gui)

        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setObjectName("pushButton_6")
        self.pushButton_7.setGeometry(QtCore.QRect(269, 525, 100, 23))
        self.pushButton_7.setEnabled(False)
        self.pushButton_7.clicked.connect(self.flip_x)

        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setObjectName("pushButton_6")
        self.pushButton_8.setGeometry(QtCore.QRect(379, 525, 100, 23))
        self.pushButton_8.setEnabled(False)
        self.pushButton_8.clicked.connect(self.flip_y)

        # Label Grid Name
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 101, 21))
        self.label_3.setObjectName("label_3")

        # Check Box to add points
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(190, 187, 70, 17))
        self.checkBox.setObjectName("checkBox")

        # Label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 180, 71, 20))
        self.label.setObjectName("label")


        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(700, 530, 83, 19))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")


        self.radioButton_2 = QtWidgets.QRadioButton(self.widget1)
        self.radioButton_2.setChecked(True)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)
        self.radioButton_2.clicked.connect(self.get_curr_img)


        self.radioButton = QtWidgets.QRadioButton(self.widget1)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.radioButton.clicked.connect(self.get_curr_img)

        self.checkBoxGrid = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxGrid.setGeometry(QtCore.QRect(490, 530, 110, 17))
        self.checkBoxGrid.setObjectName("checkBox")
        self.checkBoxGrid.stateChanged.connect(self.get_curr_img)

        self.widget2 = QtWidgets.QWidget(self.centralwidget)
        self.widget2.setGeometry(QtCore.QRect(40, 100, 71, 41))
        self.widget2.setObjectName("widget2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")


        self.radioButton_3 = QtWidgets.QRadioButton(self.widget2)
        self.radioButton_3.setChecked(True)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout_2.addWidget(self.radioButton_3)
        self.radioButton_3.clicked.connect(self.get_curr_img)



        self.radioButton_4 = QtWidgets.QRadioButton(self.widget2)
        self.radioButton_4.setObjectName("radioButton_4")
        self.verticalLayout_2.addWidget(self.radioButton_4)
        self.radioButton_4.clicked.connect(self.get_curr_img)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 803, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)


        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Grid Creator"))
        self.pushButton.setText(_translate("MainWindow", "Open Excel"))
        self.pushButton_3.setText(_translate("MainWindow", "Display Grid"))
        self.pushButton_4.setText(_translate("MainWindow", "Create Grid"))
        self.pushButton_5.setText(_translate("MainWindow", "Add Point to Table"))
        self.pushButton_6.setText(_translate("MainWindow", "Clear"))
        self.pushButton_7.setText(_translate("MainWindow", "Flip X"))
        self.pushButton_8.setText(_translate("MainWindow", "Flip Y"))
        self.label_3.setText(_translate("MainWindow", "Grid Name"))
        self.checkBox.setText(_translate("MainWindow", "Add Points"))
        self.checkBoxGrid.setText(_translate("MainWindow", "Show Grid Lines"))
        self.label.setText(_translate("MainWindow", "Grid Points"))
        self.radioButton_2.setText(_translate("MainWindow", "OD"))
        self.radioButton.setText(_translate("MainWindow", "OS"))
        self.radioButton_3.setText(_translate("MainWindow", "Maia"))
        self.radioButton_4.setText(_translate("MainWindow", "MP1"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

