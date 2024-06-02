from PySide2.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
                               QLabel, QSpacerItem, QSizePolicy, QStackedLayout,
                               QGridLayout
                               )
from PySide2.QtGui import QPixmap, QFont


class Header(QWidget):
    """Header class for collapsible group"""

    def __init__(self, name, content_widget):
        """Header Class Constructor to initialize the object.

        Args:
            name (str): Name for the header
            content_widget (QWidget): Widget containing child elements
        """
        super(Header, self).__init__()
        self.content = content_widget
        self.expand_ico = QPixmap(":teDownArrow.png")
        self.collapse_ico = QPixmap(":teRightArrow.png")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        stacked = QStackedLayout(self)
        stacked.setStackingMode(QStackedLayout.StackAll)
        background = QLabel()
        background.setStyleSheet("QLabel{ background-color: rgb(93, 93, 93); border-radius:2px}")

        widget = QWidget()
        layout = QHBoxLayout(widget)

        self.icon = QLabel()
        self.icon.setPixmap(self.expand_ico)
        layout.addWidget(self.icon)
        layout.setContentsMargins(11, 0, 11, 0)

        font = QFont()
        font.setBold(True)
        label = QLabel(name)
        label.setFont(font)

        layout.addWidget(label)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        stacked.addWidget(widget)
        stacked.addWidget(background)
        background.setMinimumHeight(layout.sizeHint().height() * 1.5)

    def mousePressEvent(self, *args):
        """Handle mouse events, call the function to toggle groups"""
        self.expand() if not self.content.isVisible() else self.collapse()

    def expand(self):
        self.content.setVisible(True)
        self.icon.setPixmap(self.expand_ico)

    def collapse(self):
        self.content.setVisible(False)
        self.icon.setPixmap(self.collapse_ico)


class Container(QWidget):
    """Class for creating a collapsible group similar to how it is implement in Maya

        Examples:
            Simple example of how to add a Container to a QVBoxLayout and attach a QGridLayout

            >>> layout = QVBoxLayout()
            >>> container = Container("Group")
            >>> layout.addWidget(container)
            >>> content_layout = QGridLayout(container.contentWidget)
            >>> content_layout.addWidget(QPushButton("Button"))
    """

    def __init__(self, name, color_background = False):
        """Container Class Constructor to initialize the object

        Args:
            name (str): Name for the header
            color_background (bool): whether or not to color the background lighter like in maya
        """
        super(Container, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._content_widget = QWidget()
        if color_background:
            self._content_widget.setStyleSheet(
                ".QWidget{background-color: rgb(73, 73, 73); "
                "margin-left: 2px; margin-right: 2px}"
                )
        header = Header(name, self._content_widget)
        layout.addWidget(header)
        layout.addWidget(self._content_widget)

        # assign header methods to instance attributes so they can be called outside of this class
        self.collapse = header.collapse
        self.expand = header.expand
        self.toggle = header.mousePressEvent

    @property
    def contentWidget(self):
        """Getter for the content widget

        Returns: Content widget
        """
        return self._content_widget


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
