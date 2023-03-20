""" from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore """

import os
from ctypes import alignment
from copy import deepcopy

from gui.widgets.py_push_button import PyPushButton
from gui.widgets.my_widgets import MyScrollBar

from qt_core import *


current_path = os.path.dirname(os.path.dirname(__file__))
ico_path = os.path.join(current_path, "images", "icons")


class UI_application_page_3(object):
    
    object_list = []

    def setupUi(self, application_pages: QStackedWidget):
        if not application_pages.objectName():
            application_pages.setObjectName(u"application_pages")

        # PAGE
        self.page = QWidget()

        # PAGE LAYOUT
        self.page_layout = QVBoxLayout(self.page)
        self.page_layout.setContentsMargins(0,0,0,0)

        # SCROLL AREA
        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("border: none")
        self.scroll_area.setWidgetResizable(True)

        # CREATE CUSTOM SCROLL BAR
        self.scroll_bar = MyScrollBar()

        # SET CUSTOM SCROLL BAR
        self.scroll_area.setVerticalScrollBar(self.scroll_bar)

        # ADD SCROLL AREA TO PAGE LAYOUT
        self.page_layout.addWidget(self.scroll_area)

        # CONTENTS AREA
        self.contents_area = QWidget()
        self.contents_area_layout = QVBoxLayout(self.contents_area)
        self.contents_area_layout.setContentsMargins(10,10,5,10)
        
        # CONTENTS FRAME
        self.contents_frame = QFrame()
        # self.contents_frame.setStyleSheet("background-color: blue")
        self.contents_frame.setMinimumWidth(500)
        self.contents_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # CONTENTS FRAME LAYOUT
        self.contents_frame_layout = QVBoxLayout(self.contents_frame)
        self.contents_frame_layout.setContentsMargins(0,0,0,0)
        self.contents_frame_layout.setSpacing(10)

        # CENTRAL FRAME (MAIN WORKING AREA FRAME)
        self.central_frame = QFrame()
        # self.central_frame.setStyleSheet("background-color: red")

        # CENTRAL FRAME LAYOUT
        self.central_frame_layout = QVBoxLayout(self.central_frame)
        self.central_frame_layout.setContentsMargins(0,0,0,0)
        self.central_frame_layout.setSpacing(5)

        # BOTTOM FRAME
        self.bottom_frame = QFrame()
        # self.bottom_frame.setStyleSheet("background-color: green")
        self.bottom_frame.setMaximumHeight(40)

        # BOTTOM FRAME LAYOUT
        self.bottom_frame_layout = QHBoxLayout(self.bottom_frame)
        self.bottom_frame_layout.setContentsMargins(0,0,0,0)
        self.bottom_frame_layout.setSpacing(0)

        # Spacer
        self.spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Add btn frame
        self.add_btn_frame = QFrame()
        self.add_btn_frame.setStyleSheet("background-color: purple")
        self.add_btn_frame.setMaximumHeight(40)
        self.add_btn_frame.setMaximumWidth(120)

        # Add btn layout
        self.add_btn_layout = QHBoxLayout(self.add_btn_frame)
        self.add_btn_layout.setContentsMargins(0,0,0,0)
        self.add_btn_layout.setSpacing(0)

        # Add widget btn
        self.add_widget_btn = PyPushButton(
            text="",
            icon_path=f"{ico_path}/cil-add-2",
            minimum_width=120
        )

        # Add btn to layout
        self.add_btn_layout.addWidget(self.add_widget_btn)
        
        # ADD WIDGETS TO BOTTOM FRAME LAYOUT
        self.bottom_frame_layout.addSpacerItem(self.spacer)
        self.bottom_frame_layout.addWidget(self.add_btn_frame)
        self.bottom_frame_layout.addSpacerItem(self.spacer)

        # ADD WIDGETS TO CONTENTS FRAME
        self.contents_frame_layout.addWidget(self.central_frame)
        self.contents_frame_layout.addSpacerItem(self.spacer)
        self.contents_frame_layout.addWidget(self.bottom_frame)

        # ADD CONTENTS FRAME TO CONTENTS AREA
        self.contents_area_layout.addWidget(self.contents_frame)

        # ACTIVATE CONTENTS AREA INSIDE SCROLL AREA
        self.scroll_area.setWidget(self.contents_area)
        application_pages.addWidget(self.page)

        # CLICK EVENT
        self.add_widget_btn.clicked.connect(self.add_widget)

    def add_widget(self):
        picture = QFrame()
        picture.setMinimumHeight(500)
        picture.setMaximumHeight(500)
        picture.setStyleSheet("background-color: grey")

        picture_layout = QVBoxLayout(picture)
        picture_layout.setContentsMargins(0,0,0,0)

        top_frame = QFrame()
        top_frame.setMaximumHeight(30)
        top_frame.setStyleSheet("background-color: black")

        top_frame_layout = QHBoxLayout(top_frame)
        top_frame_layout.setContentsMargins(0,0,0,0)
        top_frame_layout.setSpacing(0)

        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        btn = QPushButton("X")
        btn.setStyleSheet("""
            QPushButton { background-color: transparent; font: 700 12pt 'Segoe UI'; }
            QPushButton:hover { background-color: #a9000f; }
            QPushButton:pressed { background-color: transparent; }
        """)
        btn.setMaximumSize(QSize(70, 25))
        btn.setMinimumSize(QSize(70, 25))

        top_frame_layout.addSpacerItem(spacer)
        top_frame_layout.addWidget(btn, 0, Qt.AlignTop)

        bottom_frame = QFrame()
        bottom_frame.setStyleSheet("background-color: grey")        

        picture_layout.addWidget(top_frame)
        picture_layout.addWidget(bottom_frame)   
        
        self.object_list.append(picture)
        self.central_frame_layout.addWidget(picture)
        self.scroll_area.verticalScrollBar().rangeChanged.connect(lambda: scroll_down())

        def scroll_down():
            self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().maximum()
            )

        btn.clicked.connect(lambda: remove_widget())

        def remove_widget():
            index = self.object_list.index(picture)
            self.object_list[index].deleteLater()
            self.object_list.remove(picture)

        