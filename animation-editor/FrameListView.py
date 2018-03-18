from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class FrameDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return super(FrameDelegate, self).createEditor(parent, option, index)

class FrameListView(QListView):
    
    dragStarted = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super(FrameListView, self).__init__(*args, **kwargs)
        self.setViewMode(QListView.ListMode)
        self.setMovement(QListView.Snap)
        #self.setGridSize(QSize(256,256))
        self.setFlow(QListView.LeftToRight)
        self.setResizeMode(QListView.Adjust)
        self.setIconSize(QSize(256, 256))
        self.setWrapping(False)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.setAlternatingRowColors(True)
        self.setAutoScroll(True)
        self.setItemDelegate(FrameDelegate())
        #self.setDragEnabled(True)
        #self.setAcceptDrops(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setUniformItemSizes(True)
        
    def startDrag(self, *args, **kwargs):
        self.dragStarted.emit()
        super(FrameListView, self).startDrag(*args, **kwargs)
        
    def resizeEvent(self, event):
        self.setIconSize(QSize(event.size().height() - 16, event.size().height() - 16))
        super(FrameListView, self).resizeEvent(event)

    def viewOptions(self):
        ret = super(FrameListView, self).viewOptions()
        ret.decorationPosition = QStyleOptionViewItem.Top
        ret.displayAlignment = Qt.AlignCenter
        ret.decorationAlignment = Qt.AlignCenter
        return ret
