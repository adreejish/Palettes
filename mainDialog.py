from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QApplication
from PyQt5 import  uic

import ast

import sqlite3
import sys

from os import path
def resource_path(relative_path):
	base_path=getattr(sys,'_MEIPASS',path.dirname(path.abspath(__file__)))
	return path.join(base_path,relative_path)

class MyWindow(QtWidgets.QMainWindow):
	def __init__(self):

		super(MyWindow, self).__init__()
		ui=uic.loadUi(resource_path("paletteui1.ui"),self)

		self.palette = ui.tableWidget
		self.palette.verticalHeader().setDefaultSectionSize(70)
		self.palette.horizontalHeader().setDefaultSectionSize(70)
		self.palette.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.palette.setSelectionMode(QAbstractItemView.NoSelection)

		self.palette_name=ui.plainTextEdit
		self.palette_name.setPlaceholderText("Name")

		self.palette_tags = ui.plainTextEdit_2
		self.palette_tags.setPlaceholderText("Tags")

		self.savebutton=ui.pushButton

		self.browse_area=ui.scrollArea
		self.browse_area.setWidgetResizable=True

		self.browse_area_contents=QtWidgets.QWidget()
		self.browse_area_contents.setGeometry(QtCore.QRect(0,0,411,321))
		self.grid_layout=QtWidgets.QGridLayout(self.browse_area_contents)

		self.refresh_btn=ui.RefreshButton

		self.palette_item={}
		self.palette_colors={}

		def getcell(item):

			row=item.row()
			column=item.column()
			color=QColorDialog.getColor()
			self.palette.setItem(row, column, QTableWidgetItem())
			self.palette.item(row, column).setBackground(QColor(color))
			self.palette_colors[row,column]=color.name()


		def savedata():
			db=sqlite3.connect(resource_path("PalleteDatabase"))
			cursor=db.cursor()
			command='''INSERT INTO PaletteCollection(NAME,TAGS,COLORSTRING) VALUES(?,?,?)'''
			colorstring=str(self.palette_colors)
			name=self.palette_name.toPlainText()
			tags = self.palette_tags.toPlainText()
			DataTuple=(name,tags,colorstring)
			cursor.execute(command,DataTuple)
			db.commit()
			cursor.close()
			self.palette_name.setPlainText("")
			self.palette_tags.setPlainText("")

		def populate_tables():
			db=sqlite3.connect(resource_path("PalleteDatabase"))
			cursor=db.cursor()
			command='''SELECT * FROM PaletteCollection'''
			cursor.execute(command)
			rows=cursor.fetchall()

			for i in range(len(rows)):
				row = int(i / 3)
				column = i % 3
				self.tablewidget = QtWidgets.QTableWidget()
				self.tablewidget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
				self.tablewidget.setMaximumSize(120, 120)
				self.tablewidget.setRowCount(4)
				self.tablewidget.setColumnCount(4)

				self.tablewidget.verticalHeader().setDefaultSectionSize(30)
				self.tablewidget.horizontalHeader().setDefaultSectionSize(30)
				self.tablewidget.horizontalHeader().setSectionResizeMode(2)
				self.tablewidget.verticallHeader().setSectionResizeMode(2)


				self.tablewidget.horizontalHeader().setVisible(False)
				self.tablewidget.verticalHeader().setVisible(False)

				self.tablewidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
				self.tablewidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

				self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
				self.tablewidget.setSelectionMode(QAbstractItemView.NoSelection)

				colours_to_populate = rows[i][2]
				colours_to_populate = ast.literal_eval(colours_to_populate)
				for colour in colours_to_populate.keys():
					sub_row = colour[0]
					sub_col = colour[1]
					color_to_set=colours_to_populate[colour]
					self.tablewidget.setItem(sub_row, sub_col, QTableWidgetItem())
					self.tablewidget.item(sub_row, sub_col).setBackground(QColor(color_to_set))

				self.grid_layout.addWidget(self.tablewidget, row, column)

				self.browse_area.setWidget(self.browse_area_contents)





		populate_tables()
		self.palette.clicked.connect(getcell)
		self.savebutton.clicked.connect(savedata)
		self.refresh_btn.clicked.connect(populate_tables)



		self.show()

if __name__=='__main__':
	app=QApplication(sys.argv)
	window= MyWindow()
	sys.exit(app.exec_())


