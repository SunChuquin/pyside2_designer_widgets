from typing import List, Any, AnyStr
from enum import Enum

from PySide2.QtCore import QAbstractListModel, QObject, QModelIndex, QSize, Signal, Slot, QEnum, Qt, QRect, QPointF
from PySide2.QtGui import QPainter, QFont, QColor, QFontDatabase, QPen
from PySide2.QtWidgets import QStyledItemDelegate, QListView, QStyleOptionViewItem, QWidget, QStyle

from custom_widgets.iconhelper.resource import *

class NavListView(QListView):
    """
    树状导航栏控件
    作者:feiyangqingyun(QQ:517216493) 2018-8-15
    译者:sunchuquin(QQ:1715216365) 2021-06-19
    1. 设置节点数据相当方便,按照对应格式填入即可,分隔符,
    2. 可设置提示信息 是否显示+宽度
    3. 可设置行分隔符 是否显示+高度+颜色
    4. 可设置选中节点线条突出显示+颜色+左侧右侧位置
    5. 可设置选中节点三角形突出显示+颜色+左侧右侧位置
    6. 可设置父节点的 选中颜色+悬停颜色+默认颜色
    7. 可设置子节点的 选中颜色+悬停颜色+默认颜色
    8. 可设置父节点文字的 图标边距+左侧距离+字体大小+高度
    9. 可设置子节点文字的 图标边距+左侧距离+字体大小+高度
    10. 可设置节点展开模式 单击+双击+禁用
    """

    @QEnum
    # 节点展开模式
    class ExpendMode(Enum):
        ExpendMode_SingleClick = 0  # 单击展开
        ExpendMode_DoubleClick = 1  # 双击展开
        ExpendMode_NoClick = 2      # 禁用单击

    pressed_curName: Signal = Signal(str, str)  # text, parentText

    pressed_curIndex: Signal = Signal(int, int)  # index, parentIndex

    pressed_allIndex: Signal = Signal(int)  # childIndex

    def __init__(self, parent: QWidget = None):
        super(NavListView, self).__init__(parent)
        self.__model: NavModel = NavModel(self)  # 数据模型
        self.__delegate: NavDelegate = NavDelegate(self)  # 数据委托
        self.parentItem: List[AnyStr] = []  # 父节点数据集合
        self.__childItem: List[List[AnyStr]] = []  # 子节点数据

        self.__items: str = ''  # 节点集合
        self.__rightIconVisible: bool = True  # 右侧图标是否显示
        self.__tipVisible: bool = True  # 是否显示提示信息
        self.__tipWidth: int = 40  # 提示信息宽度

        self.__separateVisible: bool = True  # 是否显示行分隔符
        self.__separateHeight: int = 1  # 行分隔符高度
        self.__separateColor: QColor = QColor(40, 43, 51)  # 行分隔符颜色

        self.__lineLeft: bool = True  # 是否显示在左侧
        self.__lineVisible: bool = True  # 是否显示线条
        self.__lineWidth: int = 6  # 线条宽度
        self.__lineColor: QColor = QColor(0, 187, 158)  # 线条颜色

        self.__triangleLeft: bool = False  # 是否显示在左侧
        self.__triangleVisible: bool = True  # 是否显示三角形
        self.__triangleWidth: int = 6  # 三角形宽度
        self.__triangleColor: QColor = QColor(250, 250, 250)  # 三角形颜色

        self.__parentIconMargin: int = 10  # 父节点图标边距
        self.__parentMargin: int = 30  # 父节点边距
        self.__parentFontSize: int = 12  # 父节点字体大小
        self.__parentHeight: int = 35  # 父节点高度
        self.__parentBgNormalColor: QColor = QColor(57, 61, 73)  # 父节点正常背景色
        self.__parentBgSelectedColor: QColor = QColor(78, 83, 102)  # 父节点选中背景色
        self.__parentBgHoverColor: QColor = QColor(78, 83, 102)  # 父节点悬停背景色
        self.__parentTextNormalColor: QColor = QColor(250, 250, 250)  # 父节点正常文字颜色
        self.__parentTextSelectedColor: QColor = QColor(250, 250, 250)  # 父节点选中文字颜色
        self.__parentTextHoverColor: QColor = QColor(250, 250, 250)  # 父节点悬停文字颜色

        self.__childIconMargin: int = 15  # 子节点图标边距
        self.__childMargin: int = 35  # 子节点边距
        self.__childFontSize: int = 12  # 子节点字体大小
        self.__childHeight: int = 30  # 子节点高度
        self.__childBgNormalColor: QColor = QColor(40, 43, 51)  # 子节点正常背景色
        self.__childBgSelectedColor: QColor = QColor(20, 20, 20)  # 子节点选中背景色
        self.__childBgHoverColor: QColor = QColor(20, 20, 20)  # 子节点悬停背景色
        self.__childTextNormalColor: QColor = QColor(180, 180, 180)  # 子节点正常文字颜色
        self.__childTextSelectedColor: QColor = QColor(250, 250, 250)  # 子节点选中文字颜色
        self.__childTextHoverColor: QColor = QColor(255, 255, 255)  # 子节点悬停文字颜色

        self.__expendMode: NavListView.ExpendMode = NavListView.ExpendMode.ExpendMode_SingleClick  # 节点展开模式 单击/双击/禁用

        self.setMouseTracking(True)
        self.pressed.connect(self.__pressed)
        self.clicked.connect(self.__model.expand)

        # 设置节点
        self.items = ','.join([
            "主界面||0|正常|",
            "地图监控|主界面|||0xf03e",
            "视频监控|主界面|||0xf03d",
            "设备监控|主界面|||0xf108",
            "系统设置||0||",
            "防区信息|系统设置|||0xf0e8",
            "位置调整|系统设置|||0xf060",
            "地图编辑|系统设置|||0xf03e"
        ])

    def __del__(self):
        del self.__model
        del self.__delegate

    @Slot()
    def __pressed(self, data: QModelIndex) -> None:
        node: NavModel.TreeNode = data.data(Qt.UserRole)
        text: AnyStr = node.text
        parentText: AnyStr = node.parentText
        parentIndex: int = self.parentItem.index(parentText)

        # 默认没有子节点则父节点为子节点
        index: int = self.__childItem[parentIndex].index(text) if parentIndex >= 0 else self.parentItem.index(text)

        # 找出子节点在子节点队列中的索引
        childIndex: int = -1
        for i in range(self.__childItem.__len__()):
            item: List[AnyStr] = self.__childItem[i]
            ok: bool = False
            for subItem in item:
                childIndex += 1

                # 找到了对应子节点
                if subItem == text:
                    ok = True
                    break

            if ok:
                break

        # 如果当前节点是父节点则将子节点索引置为-1
        if parentIndex == -1:
            childIndex = -1

        self.pressed_curName.emit(text, parentText)  # 当前节点名称+父节点名称
        self.pressed_curIndex.emit(index, parentIndex)  # 当前节点索引+父节点索引
        self.pressed_allIndex.emit(childIndex)  # 整个子节点中对应的索引

    @Slot()
    def __setData(self, list_items: List[AnyStr]) -> None:
        self.__model.setItems(list_items)
        self.setModel(self.__model)
        self.setItemDelegate(self.__delegate)

    @property
    def items(self) -> AnyStr: return self.__items
    @property
    def rightIconVisible(self) -> bool: return self.__rightIconVisible
    @property
    def tipVisible(self) -> bool: return self.__tipVisible
    @property
    def tipWidth(self) -> int: return self.__tipWidth
    @property
    def separateVisible(self) -> bool: return self.__separateVisible
    @property
    def separateHeight(self) -> int: return self.__separateHeight
    @property
    def separateColor(self) -> QColor: return self.__separateColor
    @property
    def lineLeft(self) -> bool: return self.__lineLeft
    @property
    def lineVisible(self) -> bool: return self.__lineVisible
    @property
    def lineWidth(self) -> int: return self.__lineWidth
    @property
    def lineColor(self) -> QColor: return self.__lineColor
    @property
    def triangleLeft(self) -> bool: return self.__triangleLeft
    @property
    def triangleVisible(self) -> bool: return self.__triangleVisible
    @property
    def triangleWidth(self) -> int: return self.__triangleWidth
    @property
    def triangleColor(self) -> QColor: return self.__triangleColor
    @property
    def parentIconMargin(self) -> int: return self.__parentIconMargin
    @property
    def parentMargin(self) -> int: return self.__parentMargin
    @property
    def parentFontSize(self) -> int: return self.__parentFontSize
    @property
    def parentHeight(self) -> int: return self.__parentHeight
    @property
    def parentBgNormalColor(self) -> QColor: return self.__parentBgNormalColor
    @property
    def parentBgSelectedColor(self) -> QColor: return self.__parentBgSelectedColor
    @property
    def parentBgHoverColor(self) -> QColor: return self.__parentBgHoverColor
    @property
    def parentTextNormalColor(self) -> QColor: return self.__parentTextNormalColor
    @property
    def parentTextSelectedColor(self) -> QColor: return self.__parentTextSelectedColor
    @property
    def parentTextHoverColor(self) -> QColor: return self.__parentTextHoverColor
    @property
    def childIconMargin(self) -> int: return self.__childIconMargin
    @property
    def childMargin(self) -> int: return self.__childMargin
    @property
    def childFontSize(self) -> int: return self.__childFontSize
    @property
    def childHeight(self) -> int: return self.__childHeight
    @property
    def childBgNormalColor(self) -> QColor: return self.__childBgNormalColor
    @property
    def childBgSelectedColor(self) -> QColor: return self.__childBgSelectedColor
    @property
    def childBgHoverColor(self) -> QColor: return self.__childBgHoverColor
    @property
    def childTextNormalColor(self) -> QColor: return self.__childTextNormalColor
    @property
    def childTextSelectedColor(self) -> QColor: return self.__childTextSelectedColor
    @property
    def childTextHoverColor(self) -> QColor: return self.__childTextHoverColor
    @property
    def expendMode(self) -> ExpendMode: return self.__expendMode
    @property
    def sizeHint(self) -> QSize: return QSize(200, 300)
    @property
    def minimumSizeHint(self) -> QSize: return QSize(20, 20)

    def setCurrentRow(self, row: int) -> None:
        """
        设置选中指定行
        """
        self.setCurrentIndex(self.__model.index(row, 0))

    @items.setter
    def items(self, itemsa: AnyStr) -> None:
        """
        设置节点数据
        """
        if self.__items == itemsa:
            return

        self.__items = itemsa
        item: List[AnyStr] = itemsa.split(",")
        self.__setData(item)

        # 将对应的父节点子节点转换为数组,以便用户按下鼠标时候判断
        self.parentItem.clear()
        self.__childItem.clear()
        count: int = len(item)

        for i in range(count):
            lists: List[AnyStr] = item[i].split("|")
            if len(lists) < 5:
                continue

            # 父节点名称为空则说明是父节点
            text: AnyStr = lists[0]
            parentText: AnyStr = lists[1]
            if parentText == '':
                # 找出该父节点下的所有子节点
                childs: List[AnyStr] = []
                for j in range(count):
                    childList: List[AnyStr] = item[j].split("|")
                    if len(childList) < 5:
                        continue

                    childText: AnyStr = childList[0]
                    childParentText: AnyStr = childList[1]

                    # 如果父节点的名称和上一个子节点的名称一致则说明当前节点为其子节点
                    if childParentText == text:
                        childs.append(childText)

                self.parentItem.append(text)
                self.__childItem.append(childs)
        # print(parentItem, childItem)

    @rightIconVisible.setter  # 设置父节点右侧图标是否显示
    def rightIconVisible(self, right_icon_visible: bool) -> None: self.__rightIconVisible = right_icon_visible
    @tipVisible.setter  # 设置提示信息是否显示
    def tipVisible(self, tip_visible: bool) -> None: self.__tipVisible = tip_visible
    @tipWidth.setter  # 设置提示信息的宽度
    def tipWidth(self, tip_width: int) -> None: self.__tipWidth = tip_width
    @separateVisible.setter  # 设置行分隔符是否显示
    def separateVisible(self, separate_visible: bool) -> None: self.__separateVisible = separate_visible
    @separateHeight.setter  # 设置行分隔符的高度
    def separateHeight(self, separate_height: int) -> None: self.__separateHeight = separate_height
    @separateColor.setter  # 设置行分隔符的颜色
    def separateColor(self, separate_color: QColor) -> None: self.__separateColor = separate_color
    @lineLeft.setter  # 设置线条的位置
    def lineLeft(self, line_left: bool) -> None: self.__lineLeft = line_left
    @lineVisible.setter  # 设置线条是否可见
    def lineVisible(self, line_visible: bool) -> None: self.__lineVisible = line_visible
    @lineWidth.setter  # 设置线条的宽度
    def lineWidth(self, line_width: int) -> None: self.__lineWidth = line_width
    @lineColor.setter  # 设置线条的颜色
    def lineColor(self, line_color: QColor) -> None: self.__lineColor = line_color
    @triangleLeft.setter  # 设置三角形的位置
    def triangleLeft(self, triangle_left: bool) -> None: self.__triangleLeft = triangle_left
    @triangleVisible.setter  # 设置三角形是否可见
    def triangleVisible(self, triangle_visible: bool) -> None: self.__triangleVisible = triangle_visible
    @triangleWidth.setter  # 设置三角形的宽度
    def triangleWidth(self, triangle_width: int) -> None: self.__triangleWidth = triangle_width
    @triangleColor.setter  # 设置三角形的颜色
    def triangleColor(self, triangle_color: QColor) -> None: self.__triangleColor = triangle_color
    @parentIconMargin.setter  # 设置父节点的图标边距
    def parentIconMargin(self, parent_icon_margin: int) -> None: self.__parentIconMargin = parent_icon_margin
    @parentMargin.setter  # 设置父节点的左侧边距
    def parentMargin(self, parent_margin: int) -> None: self.__parentMargin = parent_margin
    @parentFontSize.setter  # 设置父节点的字体大小
    def parentFontSize(self, parent_font_size: int) -> None: self.__parentFontSize = parent_font_size
    @parentHeight.setter  # 设置父节点的节点高度
    def parentHeight(self, parent_height: int) -> None: self.__parentHeight = parent_height
    @parentBgNormalColor.setter  # 设置父节点的正常背景色
    def parentBgNormalColor(self, parent_bg_normal_color: QColor) -> None: self.__parentBgNormalColor = parent_bg_normal_color
    @parentBgSelectedColor.setter  # 设置父节点的选中背景色
    def parentBgSelectedColor(self, parent_bg_selected_color: QColor) -> None: self.__parentBgSelectedColor = parent_bg_selected_color
    @parentBgHoverColor.setter  # 设置父节点的悬停背景色
    def parentBgHoverColor(self, parent_bg_hover_color: QColor) -> None: self.__parentBgHoverColor = parent_bg_hover_color
    @parentTextNormalColor.setter  # 设置父节点的正常文本色
    def parentTextNormalColor(self, parent_text_normal_color: QColor) -> None: self.__parentTextNormalColor = parent_text_normal_color
    @parentTextSelectedColor.setter  # 设置父节点的选中文本色
    def parentTextSelectedColor(self, parent_text_selected_color: QColor) -> None: self.__parentTextSelectedColor = parent_text_selected_color
    @parentTextHoverColor.setter  # 设置父节点的悬停文本色
    def parentTextHoverColor(self, parent_text_hover_color: QColor) -> None: self.__parentTextHoverColor = parent_text_hover_color
    @childIconMargin.setter  # 设置子节点的图标边距
    def childIconMargin(self, child_icon_margin: int) -> None: self.__childIconMargin = child_icon_margin
    @childMargin.setter  # 设置子节点的左侧边距
    def childMargin(self, child_margin: int) -> None: self.__childMargin = child_margin
    @childFontSize.setter  # 设置子节点的字体大小
    def childFontSize(self, child_font_size: int) -> None: self.__childFontSize = child_font_size
    @childHeight.setter  # 设置子节点的节点高度
    def childHeight(self, child_height: int) -> None: self.__childHeight = child_height
    @childBgNormalColor.setter  # 设置子节点的正常背景色
    def childBgNormalColor(self, child_bg_normal_color: QColor) -> None: self.__childBgNormalColor = child_bg_normal_color
    @childBgSelectedColor.setter  # 设置子节点的选中背景色
    def childBgSelectedColor(self, child_bg_selected_color: QColor) -> None: self.__childBgSelectedColor = child_bg_selected_color
    @childBgHoverColor.setter  # 设置子节点的悬停背景色
    def childBgHoverColor(self, child_bg_hover_color: QColor) -> None: self.__childBgHoverColor = child_bg_hover_color
    @childTextNormalColor.setter  # 设置子节点的正常文本色
    def childTextNormalColor(self, child_text_normal_color: QColor) -> None: self.__childTextNormalColor = child_text_normal_color
    @childTextSelectedColor.setter  # 设置子节点的选中文本色
    def childTextSelectedColor(self, child_text_selected_color: QColor) -> None: self.__childTextSelectedColor = child_text_selected_color
    @childTextHoverColor.setter  # 设置子节点的悬停文本色
    def childTextHoverColor(self, child_text_hover_color: QColor) -> None: self.__childTextHoverColor = child_text_hover_color

    @expendMode.setter  # 设置节点展开模式
    def expendMode(self, expend_mode: ExpendMode) -> None:
        if self.expendMode != expend_mode:
            self.__expendMode = expend_mode
            if expend_mode == NavListView.ExpendMode.ExpendMode_SingleClick:
                self.doubleClicked.disconnect(self.__model.expand)
                self.clicked.connect(self.__model.expand)
            elif expend_mode == NavListView.ExpendMode.ExpendMode_DoubleClick:
                self.clicked.disconnect(self.__model.expand)
                self.doubleClicked.connect(self.__model.expand)
            elif expend_mode == NavListView.ExpendMode.ExpendMode_NoClick:
                self.clicked.disconnect(self.__model.expand)
                self.doubleClicked.disconnect(self.__model.expand)
        self.__expendMode = expend_mode

class NavModel(QAbstractListModel):

    class TreeNode:
        def __init__(self):
            self.level: int = 1  # 层级,父节点-1,子节点-2
            self.expand: bool = False  # 是否打开子节点
            self.last: bool = False  # 是否末尾元素
            self.icon: AnyStr = ''  # 左侧图标
            self.text: AnyStr = ''  # 显示的节点文字
            self.tip: AnyStr = ''  # 右侧描述文字
            self.parentText: AnyStr = ''  # 父节点名称
            self.children: List[NavModel.TreeNode] = []  # 子节点集合

    class ListNode:
        def __init__(self):
            self.text: AnyStr = ''  # 节点文字
            self.treeNode: NavModel.TreeNode = NavModel.TreeNode()  # 节点指针

    def __init__(self, parent: QObject):
        super(NavModel, self).__init__(parent)

        self.__treeNode: List[NavModel.TreeNode] = []
        self.__listNode: List[NavModel.ListNode] = []

    def __del__(self):
        """for (QList<TreeNode *>::iterator it = treeNode.begin(); it != treeNode.end();) {
            for (QList<TreeNode *>::iterator child = (*it)->children.begin(); child != (*it)->children.end();) {
                delete(*child);
                child = (*it)->children.erase(child);
            }

            delete(*it);
            it = treeNode.erase(it);
        }"""
        pass

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self.__listNode.__len__()

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        if not index.isValid():
            return None

        if index.row() >= self.__listNode.__len__() or index.row() < 0:
            return None

        if role == Qt.DisplayRole:
            return self.__listNode[index.row()].text
        elif role == Qt.UserRole:
            return self.__listNode[index.row()].treeNode

        return None

    @Slot()
    def setItems(self, items: List[AnyStr]) -> None:
        count: int = len(items)
        if count == 0:
            return

        self.__treeNode.clear()
        self.__listNode.clear()

        # listItem格式: 标题|父节点标题(父节点为空)|是否展开|提示信息|左侧图标
        for i in range(count):
            item: AnyStr = items[i]
            lists: List[AnyStr] = item.split("|")
            if len(lists) < 5:
                continue

            # 逐个取出字符串数据
            text: AnyStr = lists[0]
            parentText: AnyStr = lists[1]
            expand: AnyStr = lists[2]
            tip: AnyStr = lists[3]
            icon: AnyStr = lists[4]

            # 将父节点即父节点标题为空的元素加载完毕
            if parentText == '':
                node: NavModel.TreeNode = NavModel.TreeNode()

                # 设置父节点的level为1,是否要打开子节点从参数取
                node.level = 1
                node.expand = int(expand)
                node.last = False

                if icon != '':
                    node.icon = chr(int(icon, 16))

                node.text = text
                node.tip = tip
                node.parentText = parentText

                # 查找该父节点是否有对应子节点,有则加载
                for j in range(count):
                    childItem: AnyStr = items[j]
                    childList: List[AnyStr] = childItem.split("|")
                    if len(childList) < 5:
                        continue

                    childText: AnyStr = childList[0]
                    childParentText: AnyStr = childList[1]
                    childTip: AnyStr = childList[3]
                    childIcon: AnyStr = childList[4]

                    # 传过来的图标字符串可能以0x打头,要去掉
                    childIcon = childIcon.replace("0x", "")

                    # 如果当前子节点的父节点名称是上一个节点的名称则归属于该节点
                    if childParentText == text:
                        childNode: NavModel.TreeNode = NavModel.TreeNode()

                        # 设置子节点的level为2,是否要打开子节点设置false,可自行更改从参数取,如果有三级节点的话
                        childNode.level = 2
                        childNode.expand = False
                        childNode.last = j == count - 1

                        if childIcon != '':
                            childNode.icon = chr(int(childIcon, 16))

                        childNode.text = childText
                        childNode.tip = childTip
                        childNode.parentText = childParentText
                        node.children.append(childNode)
                self.__treeNode.append(node)
        self.__refreshList()
        self.beginResetModel()
        self.endResetModel()

    @Slot()
    def expand(self, index: QModelIndex):
        node: NavModel.TreeNode = self.__listNode[index.row()].treeNode
        if node.children.__len__() == 0:
            return

        node.expand = not node.expand
        self.__refreshList()

        last = 1 if node.expand else node.children.__len__()

        self.beginInsertRows(QModelIndex(), index.row() + 1, index.row() + last)
        self.endInsertRows()

    def __refreshList(self):
        self.__listNode.clear()
        for it in self.__treeNode:
            node: NavModel.ListNode = NavModel.ListNode()
            node.text = it.text
            node.treeNode = it

            self.__listNode.append(node)
            if it.expand:
                continue

            for child in it.children:
                node_2: NavModel.ListNode = NavModel.ListNode()
                node_2.text = child.text
                node_2.treeNode = child
                node_2.treeNode.last = False
                self.__listNode.append(node_2)

            if self.__listNode is not None:
                self.__listNode[-1].treeNode.last = True


class NavDelegate(QStyledItemDelegate):
    def __init__(self, parent: QObject):
        super(NavDelegate, self).__init__()

        self.__nav: NavListView = parent
        self.__iconFont: QFont = QFont()

        # 判断图形字体是否存在，不存在则加入
        fontDb: QFontDatabase = QFontDatabase()
        if not fontDb.families().__contains__("FontAwesome"):
            fontId: int = fontDb.addApplicationFont(":/image/fontawesome-webfont.ttf")
            fontName: List[str] = fontDb.applicationFontFamilies(fontId)
            if len(fontName) == 0:
                print("load fontawesome-webfont.ttf error")

        if fontDb.families().__contains__("FontAwesome"):
            self.__iconFont: QFont = QFont("FontAwesome")
            self.__iconFont.setHintingPreference(QFont.PreferNoHinting)  # if Qt version >= 4.8.0

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        node: NavModel.TreeNode = index.data(Qt.UserRole)  # NavModel::TreeNode *node = (NavModel::TreeNode *)index.data(Qt::UserRole).toULongLong();
        # 设置最小的宽高
        parent: bool = node.level == 1
        size: QSize = QSize(50, self.__nav.parentHeight if parent else self.__nav.childHeight)
        return size

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        painter.setRenderHints(QPainter.Antialiasing)
        node: NavModel.TreeNode = index.data(Qt.UserRole)

        # 定义变量存储区域
        optionRect: QRect = option.rect
        x: int = optionRect.x()
        y: int = optionRect.y()
        width: int = optionRect.width()
        height: int = optionRect.height()

        fontSize: int = self.__nav.parentFontSize

        parent: bool = node.level == 1  # 父节点和子节点颜色分开设置

        # 根据不同的状态设置不同的颜色 bgColor-主背景色 textColor-主文字颜色 tipBgColor-提示信息背景颜色 tipTextColor-提示信息文字颜色
        if option.state & QStyle.State_Selected:
            bgColor = self.__nav.parentBgSelectedColor if parent else self.__nav.childBgSelectedColor
            textColor = self.__nav.parentTextSelectedColor if parent else self.__nav.childTextSelectedColor
            tipBgColor = self.__nav.parentTextSelectedColor if parent else self.__nav.childTextSelectedColor
            tipTextColor = self.__nav.parentBgSelectedColor if parent else self.__nav.childBgSelectedColor
            # iconColor = self.__nav.parentTextSelectedColor if parent else self.__nav.childTextSelectedColor
        elif option.state & QStyle.State_MouseOver:
            bgColor = self.__nav.parentBgHoverColor if parent else self.__nav.childBgHoverColor
            textColor = self.__nav.parentTextHoverColor if parent else self.__nav.childTextHoverColor
            tipBgColor = self.__nav.parentTextSelectedColor if parent else self.__nav.childTextSelectedColor
            tipTextColor = self.__nav.parentBgSelectedColor if parent else self.__nav.childBgSelectedColor
            # iconColor = self.__nav.parentTextHoverColor if parent else self.__nav.childTextHoverColor
        else:
            bgColor = self.__nav.parentBgNormalColor if parent else self.__nav.childBgNormalColor
            textColor = self.__nav.parentTextNormalColor if parent else self.__nav.childTextNormalColor
            tipBgColor = self.__nav.parentBgSelectedColor if parent else self.__nav.childBgSelectedColor
            tipTextColor = self.__nav.parentTextSelectedColor if parent else self.__nav.childTextSelectedColor
            # iconColor = self.__nav.parentTextNormalColor if parent else self.__nav.childTextNormalColor

        painter.fillRect(optionRect, bgColor)  # 绘制背景

        # 绘制线条,目前限定子节点绘制,如果需要父节点也绘制则取消parent判断即可
        lineWidth: int = self.__nav.lineWidth
        if not parent and self.__nav.lineVisible and lineWidth > 0:
            if (option.state & QStyle.State_Selected) or (option.state & QStyle.State_MouseOver):
                offset: float = lineWidth / 2  # 设置偏移量,不然上下部分会有点偏移

                # 计算上下两个坐标点
                pointTop = QPointF(x, y + offset)
                pointBottom = QPointF(x, height + y - offset)
                if not self.__nav.lineLeft:
                    pointTop.setX(width)
                    pointBottom.setX(width)

                # 设置线条颜色和宽度
                painter.setPen(QPen(self.__nav.lineColor, lineWidth))
                painter.drawLine(pointTop, pointBottom)

        # 绘制三角形,目前限定子节点绘制,如果需要父节点也绘制则取消parent判断即可
        triangleWidth: int = self.__nav.triangleWidth
        if not parent and self.__nav.triangleVisible and triangleWidth > 0:
            if (option.state & QStyle.State_Selected) or (option.state & QStyle.State_MouseOver):
                font: QFont = self.__iconFont
                font.setPixelSize(fontSize + triangleWidth)
                painter.setFont(font)
                painter.setPen(self.__nav.triangleColor)

                # 采用图形字体中的三角形绘制
                if self.__nav.triangleLeft:
                    painter.drawText(optionRect, Qt.AlignLeft | Qt.AlignVCenter, chr(0xf0da))
                else:
                    painter.drawText(optionRect, Qt.AlignRight | Qt.AlignVCenter, chr(0xf0d9))

        # 绘制行分隔符
        if self.__nav.separateVisible:
            if node.level == 1 or node.level == 2 and node.last:
                painter.setPen(QPen(self.__nav.separateColor, self.__nav.separateHeight))
                painter.drawLine(QPointF(x, y + height), QPointF(x + width, y + height))

        # 绘制文字,如果文字为空则不绘制
        text: str = node.text
        if text != '':
            # 文字离左边的距离+字体大小
            margin: int = self.__nav.parentMargin
            if node.level == 2:
                margin = self.__nav.childMargin
                fontSize = self.__nav.childFontSize

            # 计算文字区域
            textRect: QRect = optionRect.__copy__()
            textRect.setWidth(width - margin)
            textRect.setX(x + margin)

            font: QFont = QFont()
            font.setPixelSize(fontSize)
            painter.setFont(font)
            painter.setPen(textColor)
            painter.drawText(textRect, Qt.AlignLeft | Qt.AlignVCenter, text)

        # 绘制提示信息,如果不需要显示提示信息或者提示信息为空则不绘制
        tip: str = node.tip

        if self.__nav.tipVisible and tip != '':
            # 如果是数字则将超过999的数字显示成 999+
            # 如果显示的提示信息长度过长则将多余显示成省略号.
            try:
                if int(tip) > 0:
                    tip = "999+" if int(tip) > 999 else tip
            except ValueError:
                if len(tip) > 2:
                    tip = tip[:2] + " ."

            # 计算绘制区域,半径取高度的四分之一
            radius: int = height // 4
            tipRect: QRect = optionRect.__copy__()
            tipRect.setHeight(radius * 2)
            tipRect.moveCenter(optionRect.center())
            tipRect.setLeft(optionRect.right() - self.__nav.tipWidth - 5)
            tipRect.setRight(optionRect.right() - 5)

            # 设置字体大小
            font: QFont = QFont()
            font.setPixelSize(fontSize - 2)
            painter.setFont(font)

            # 绘制提示文字的背景
            painter.setPen(Qt.NoPen)
            painter.setBrush(tipBgColor)
            painter.drawRoundedRect(tipRect, radius, radius)

            # 绘制提示文字
            painter.setPen(tipTextColor)
            painter.setBrush(Qt.NoBrush)
            painter.drawText(tipRect, Qt.AlignCenter, tip)

        # 计算绘制图标区域
        iconRect: QRect = optionRect.__copy__()
        iconRect.setLeft(self.__nav.parentIconMargin if parent else self.__nav.childIconMargin)

        # 设置图形字体和画笔颜色
        font: QFont = self.__iconFont
        font.setPixelSize(fontSize)
        painter.setFont(font)
        painter.setPen(textColor)

        # 绘制左侧图标,有图标则绘制图标,没有的话父窗体取 + -
        if node.icon != '':
            painter.drawText(iconRect, Qt.AlignLeft | Qt.AlignVCenter, node.icon)
        elif parent:
            if node.expand:
                painter.drawText(iconRect, Qt.AlignLeft | Qt.AlignVCenter, chr(0xf067))
            else:
                painter.drawText(iconRect, Qt.AlignLeft | Qt.AlignVCenter, chr(0xf068))

        # 绘制父节点右侧图标
        iconRect.setRight(optionRect.width() - 10)
        if not (self.__nav.tipVisible and node.tip != '') and self.__nav.rightIconVisible and parent:
            if node.expand:
                painter.drawText(iconRect, Qt.AlignRight | Qt.AlignVCenter, chr(0xf054))
            else:
                painter.drawText(iconRect, Qt.AlignRight | Qt.AlignVCenter, chr(0xf078))


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication, QHBoxLayout
    import sys

    class FrmNavListView(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmNavListView, self).__init__(parent)
            self.navListView = NavListView()
            layout = QHBoxLayout()
            layout.addWidget(self.navListView)
            self.setLayout(layout)
            self.__initForm()

        @Slot()
        def __initForm(self):
            # 设置节点数据,格式 标题|父节点标题(父节点为空)|是否展开|提示信息|左侧图标
            items: List[AnyStr] = [
                "主界面||0|3|",
                "地图监控|主界面|||0xf03e",
                "视频监控|主界面|||0xf03d",
                "设备监控|主界面|||0xf108",

                "系统设置||0|3|",
                "防区信息|系统设置|||0xf0e8",
                "位置调整|系统设置|||0xf060",
                "地图编辑|系统设置|||0xf03e",

                "警情查询||0|3|",
                "记录查询|警情查询|||0xf073",
                "图像查询|警情查询|||0xf03e",
                "视频查询|警情查询|||0xf03d",
                "数据回放|警情查询|||0xf080",

                "帮助文档||1|0|"
            ]

            self.navListView.items = ",".join(items)

            self.navListView.tipVisible = True

            self.navListView.separateColor = QColor(193, 193, 193)
            self.navListView.childBgNormalColor = QColor(255, 255, 255)
            self.navListView.childBgSelectedColor = QColor(230, 230, 230)
            self.navListView.childBgHoverColor = QColor(240, 240, 240)
            self.navListView.childTextNormalColor = QColor(19, 36, 62)
            self.navListView.childTextSelectedColor = QColor(19, 36, 62)
            self.navListView.childTextHoverColor = QColor(19, 36, 62)
            self.navListView.parentBgNormalColor = QColor(255, 255, 255)
            self.navListView.parentBgSelectedColor = QColor(230, 230, 230)
            self.navListView.parentBgHoverColor = QColor(240, 240, 240)
            self.navListView.parentTextNormalColor = QColor(19, 36, 62)
            self.navListView.parentTextSelectedColor = QColor(19, 36, 62)
            self.navListView.parentTextHoverColor = QColor(19, 36, 62)

            self.navListView.expendMode = NavListView.ExpendMode.ExpendMode_DoubleClick

    app = QApplication()
    window = FrmNavListView()
    window.show()
    sys.exit(app.exec_())
