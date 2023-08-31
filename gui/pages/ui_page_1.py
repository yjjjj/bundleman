""" from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore """

import os
import json
import gitlab
from core import gitclone
from core import db
from pathlib import Path
from gui.widgets import image_button
from gui.widgets import fade_label
from qt_core import *


GIT_URL = "http://192.168.1.102"
PRIVATE_TOKEN = "glpat-K-axpsEgfnfCcoHtLzhR"


PATH = Path(__file__).parent


try:
    LIB = Path(os.environ["PLE_LIB_PATH"])
    DBPATH = Path(os.environ["PLE_DIR"]).joinpath("PLE", "startup", "libdb")
except:
    LIB = Path("V:/PLE-Lib")
    DBPATH = Path("V:/PLE/startup/libdb")

gl = gitlab.Gitlab(GIT_URL, private_token=PRIVATE_TOKEN)

Groups = gl.groups.list(all=True)
extension = gl.groups.list(search="extension")[0]

Projects = extension.projects.list(all=True)


style_QSplitter = """
            QSplitter::handle{
                background-color: #272c36;
                }
            QSplitter::handle:horizontal {
                width: 3px;
                }
            QSplitter::handle:vertical {
                height: 3px;
                }
            """


class UI_application_page_1(QWidget):
    signal = Signal()
    def setupUi(self, application_pages):
        if not application_pages.objectName():
            application_pages.setObjectName(u"application_pages")
        self.label_warn = None

        self.page = QWidget()
        main_layout = QVBoxLayout(self.page)

        main_splitter = QSplitter()
        # main_splitter.setOrientation(Qt.Vertical)
        # main_splitter.setStyleSheet(style_QSplitter)

        left_widget = QWidget()
        left_widget.setMinimumWidth(300)
        right_widget = QWidget()
        right_widget.setStyleSheet("background-color: #2c313c;")

        # gitlab 所有组
        self.group_list_widget = QListWidget()
        for group in Groups:
            item = QListWidgetItem(group.name)
            self.group_list_widget.addItem(item)
            item.group = group

            group_path = LIB / group.name
            if not group_path.exists:
                group_path.mkdir()

        self.group_list_widget.itemClicked.connect(self.on_item_clicked)
        self.group_list_widget.setCurrentRow(0)
        #
        project_list_widget = QListWidget()

        for project in Projects:
            item = QListWidgetItem(project.name)
            project_list_widget.addItem(item)
            item.project = project

        self.left_layout = QVBoxLayout(left_widget)
        self.left_layout.addWidget(self.group_list_widget)

        self.right_layout = QVBoxLayout(right_widget)
        self.project_list_widget = ProjectWidget()
        self.right_layout.addWidget(self.project_list_widget)
        self.project_body()
        self.right_layout.addWidget(self.group_box)
        self.right_layout.setStretch(0, 1)
        self.right_layout.setStretch(1, 1)

        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(right_widget)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)

        main_layout.addWidget(main_splitter)
        application_pages.addWidget(self.page)

        self.on_item_clicked()

    def project_body(self):
        btn_layout = QHBoxLayout()
        add_lib_image = PATH.parent.joinpath("images", "icons", "add_lib.png")
        self.add_lib_btn = image_button.ImageButton(add_lib_image, (29, 29))
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.add_lib_btn)

        self.group_box = QGroupBox(self)
        self.group_box.setTitle("Default")

        lib_list_widget = QListWidget()

        line_frame = QFrame()
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)

        lib_version_layout = QHBoxLayout()
        self.lib_number_title = QLabel("Number Of Versions:")
        self.lib_number = QLabel("0")
        self.lib_number.setStyleSheet("color: rgb(147,190,255)")

        self.lib_version_title = QLabel("Version:")
        self.lib_version_combo = QComboBox()
        self.lib_version_combo.setFixedWidth(250)
        self.lib_version_combo.setStyleSheet("QComboBox{background: rgb(45, 55, 75); color: rgb(147, 190, 255)}")
        lib_version_layout.addWidget(self.lib_number_title)
        lib_version_layout.addWidget(self.lib_number)
        lib_version_layout.addStretch(1)
        lib_version_layout.addWidget(self.lib_version_title)
        lib_version_layout.addWidget(self.lib_version_combo)

        update_layout = QHBoxLayout()
        update_image = PATH.parent.joinpath("images", "icons", "update.png")
        self.update_btn = image_button.ImageButton(update_image, (80, 32))

        self.lib_comment = QTextEdit()
        self.lib_comment.setStyleSheet("""
                color: rgb(155, 190, 215);    
                font-size: 16px;            
                background-color: rgb(47, 54, 70);  
                border: 0px solid green;
                """)

        update_layout.addStretch(1)
        update_layout.addWidget(self.update_btn)

        layout = QVBoxLayout()
        layout.addLayout(btn_layout)
        layout.addWidget(line_frame)
        layout.addLayout(lib_version_layout)
        layout.addSpacing(20)
        layout.addWidget(self.lib_comment)
        layout.addSpacing(10)

        # layout.addStretch(1)
        layout.addLayout(update_layout)

        self.group_box.setLayout(layout)

        self.add_lib_btn.clicked.connect(self.add_lib_btn_cmd)
        self.update_btn.clicked.connect(self.update_btn_cmd)

        self.lib_version_combo.currentIndexChanged.connect(self.read_db_comment_text)

    def update_btn_cmd(self):
        version = self.lib_version_combo.currentText()
        update_lib_path = self.path / f"{self.project.name}_v{version}" / self.project.name
        db.run(DBPATH, "libdb.db", self.project.name, update_lib_path, version)

        main_window = self.sender().topLevelWidget()
        self.notification = fade_label.FadeLabel("Database Update Complete", (147, 190, 255), main_window)
        self.notification.message_show(self.sender().parent().parent())

        # 创建版本说明文件
        json_file = self.path / f"{self.project.name}_v{version}" / "{}.json".format(self.project.name)
        comment_text = dict()
        comment_text["comment"] = self.lib_comment.toPlainText()

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(comment_text, f, ensure_ascii=False, indent=4)

    def on_item_clicked(self):
        self.project_list_widget.clear()

        current_item = self.group_list_widget.currentItem()
        projects = current_item.group.projects.list(all=True)

        self.title_list = list()
        for project in projects:
            # item = QListWidgetItem(project.name)
            item = self.project_list_widget.make_item(project.name)
            item.project = project
            self.project_list_widget.project_btn.clicked.connect(self.on_project_clicked)
            self.title_list.append(self.project_list_widget.project_title)

    def on_project_clicked(self):
        current_item = self.sender().item
        self.project = current_item.project

        self.lib_number.setText("0")
        self.lib_version_combo.clear()

        self.group_box.setTitle(self.project.name)

        current_group = gl.groups.get(self.project.group_id)
        self.path = LIB / current_group.name / self.project.name

        if not self.path.exists():
            self.path.mkdir()
        else:
            project_list = os.listdir(self.path)
            sorted_project_list = sorted(project_list, reverse=True)
            self.lib_version_combo.addItems([x.split('_v')[-1] for x in sorted_project_list])
            self.lib_number.setText(str(len(project_list)))

            self.update_db_combo()

        # 设置项目字体颜色
        for i in self.title_list:
            if i.title == current_item.project.name:
                i.setStyleSheet("color: rgb(188, 178, 255); font-size: 8pt;")
            else:
                i.setStyleSheet("font-size: 8pt")

    def add_lib_btn_cmd(self):
        self.lib_version_combo.clear()
        project_list = os.listdir(self.path)

        if project_list:
            max_path = max(project_list)
            max_number = int(max_path.split('_v')[-1])
            new_number = "%03d" % (max_number + 1)
            new_path = self.path / "{}_v{}".format(self.project.name, str(new_number))
            new_path.mkdir()

        else:
            new_path = self.path / "{}_v001".format(self.project.name)
            new_path.mkdir()

        project_list = os.listdir(self.path)
        max_path = max(project_list)
        max_number = "%03d" % int(max_path.split('_v')[-1])
        sorted_project_list = sorted(project_list, reverse=True)

        # Clone Project
        update_lib_path = self.path / f"{self.project.name}_v{max_number}"
        gitclone.clone_project(self.project.name, GIT_URL, PRIVATE_TOKEN, update_lib_path.as_posix())

        self.lib_number.setText(str(len(project_list)))
        self.lib_version_combo.addItems([x.split('_v')[-1] for x in sorted_project_list])

        # 消息提示
        main_window = self.sender().topLevelWidget()
        self.notification = fade_label.FadeLabel("Add New Version Complete", (178, 163, 235), main_window)
        self.notification.message_show(self.sender().parent().parent())

    def update_db_combo(self, combo_set=True):
        # 根据数据库版本设置combo选框版本
        db_info = db.check(DBPATH / "libdb.db")
        lib_version = ""
        for i in db_info:
            if i[0] == self.project.name:
                lib_version = i[2]
                if combo_set:
                    self.lib_version_combo.setCurrentText(lib_version)
        return lib_version

    def read_db_comment_text(self):
        # 读取json文件，设置说明文本
        self.lib_comment.clear()

        version = self.lib_version_combo.currentText()
        json_path = self.path / f"{self.project.name}_v{version}" / f"{self.project.name}.json"
        # print(json_path)

        if json_path.exists():
            json_text = json.load(open(json_path, encoding='utf-8'))
            self.lib_comment.setText(json_text.get('comment'))


class ProjectWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.resize(400, 400)
        # 隐藏横向滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 不能编辑
        self.setEditTriggers(QListWidget.NoEditTriggers)
        # 开启拖功能
        self.setDragEnabled(True)
        # 只能往外拖
        self.setDragDropMode(QListWidget.DragOnly)
        # 忽略放
        self.setDefaultDropAction(Qt.IgnoreAction)
        # ****重要的一句（作用是可以单选，多选。Ctrl、Shift多选，可从空白位置框选）****
        # ****不能用ExtendedSelection,因为它可以在选中item后继续框选会和拖拽冲突****
        self.setSelectionMode(QListWidget.ContiguousSelection)
        # 设置从左到右、自动换行、依次排列
        self.setFlow(QListWidget.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(QListWidget.Adjust)
        # item的间隔
        self.setSpacing(5)
        # 橡皮筋(用于框选效果)
        self._rubberPos = None
        self._rubberBand = QRubberBand(QRubberBand.Rectangle, self)

    # 实现拖拽的时候预览效果图
    # 这里演示拼接所有的item截图(也可以自己写算法实现堆叠效果)
    def startDrag(self, supportedActions):
        items = self.selectedItems()
        drag = QDrag(self)
        mimeData = self.mimeData(items)
        # 由于QMimeData只能设置image、urls、str、bytes等等不方便
        # 这里添加一个额外的属性直接把item放进去,后面可以根据item取出数据
        mimeData.setProperty('myItems', items)
        drag.setMimeData(mimeData)
        pixmap = QPixmap(self.viewport().visibleRegion().boundingRect().size())
        pixmap.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        for item in items:
            rect = self.visualRect(self.indexFromItem(item))
            painter.drawPixmap(rect, self.viewport().grab(rect))
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(self.viewport().mapFromGlobal(QCursor.pos()))
        drag.exec(supportedActions)

    def mousePressEvent(self, event):
        # 列表框点击事件,用于设置框选工具的开始位置
        super().mousePressEvent(event)
        item_at_position = self.itemAt(event.position().toPoint())
        if event.buttons() != Qt.LeftButton or item_at_position:
            return
        self._rubberPos = event.pos()
        self._rubberBand.setGeometry(QRect(self._rubberPos, QSize()))
        self._rubberBand.show()

    def mouseReleaseEvent(self, event):
        # 列表框点击释放事件,用于隐藏框选工具
        super().mouseReleaseEvent(event)
        self._rubberPos = None
        self._rubberBand.hide()

    def mouseMoveEvent(self, event):
        # 列表框鼠标移动事件,用于设置框选工具的矩形范围
        super().mouseMoveEvent(event)
        if self._rubberPos:
            pos = event.pos()
            lx, ly = self._rubberPos.x(), self._rubberPos.y()
            rx, ry = pos.x(), pos.y()
            size = QSize(abs(rx - lx), abs(ry - ly))
            self._rubberBand.setGeometry(
                QRect(QPoint(min(lx, rx), min(ly, ry)), size))

    def make_item(self, title_text):
        size = QSize(110, 110)
        item = QListWidgetItem(self)
        item.setSizeHint(size)

        image = PATH.parent.joinpath("images", "icons", "code.png")
        self.project_btn = image_button.ImageButton(image, (75, 75))

        self.project_title = QLabel(title_text)
        # project_title.setAlignment(Qt.AlignCenter)
        self.project_title.setStyleSheet("font-size: 8pt")

        self.project_btn.item = item
        self.project_title.title = title_text

        item_widget = QWidget()
        layout = QVBoxLayout(item_widget)
        layout.addWidget(self.project_btn)
        layout.addWidget(self.project_title)
        self.setItemWidget(item, item_widget)

        return item

