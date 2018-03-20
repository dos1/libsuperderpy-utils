#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from os import listdir
from os.path import isfile, join
from configparser import ConfigParser
from EditorUI import Ui_MainWindow

app = QApplication(sys.argv)
app.setApplicationDisplayName("libsuperderpy animation editor")

order=Qt.DescendingOrder

def sort():
    global order, model
    if order==Qt.DescendingOrder:
        order=Qt.AscendingOrder
    else:
        order=Qt.DescendingOrder
    model.sort(0, order=order)

def addFrame():
    index = ui.sourcesList.currentIndex()
    if index.model():
        item = index.model().itemFromIndex(index)
        newItem = QStandardItem(item)
        if ui.frameList.currentIndex().model():
            frameModel.insertRow(ui.frameList.currentIndex().row() + 1, newItem)
        else:
            frameModel.appendRow(newItem)
        ui.frameList.setCurrentIndex(newItem.index())
        
        window.setWindowModified(True)
        
def addAll():
    count = model.rowCount()
    for i in range(count):
        item = model.item(i)
        frameModel.appendRow(QStandardItem(item))
    if count > 0:
        window.setWindowModified(True)

def moveFrameLeft():
    frame = ui.frameList.currentIndex()
    if not frame.model():
        return
    newRow = frame.row() - 1
    if newRow < 0:
        return
    rows = frameModel.takeRow(frame.row())
    frameModel.insertRow(newRow, rows)
    ui.frameList.setCurrentIndex(rows[0].index())
    window.setWindowModified(True)

def moveFrameRight():
    frame = ui.frameList.currentIndex()
    if not frame.model():
        return
    newRow = frame.row() + 1
    if newRow >= frameModel.rowCount():
        return
    rows = frameModel.takeRow(frame.row())
    frameModel.insertRow(newRow, rows)
    ui.frameList.setCurrentIndex(rows[0].index())
    window.setWindowModified(True)
    
def duplicateFrame():
    index = ui.frameList.currentIndex()
    if index.model():
        item = index.model().itemFromIndex(index)
        newItem = QStandardItem(item)
        frameModel.insertRow(index.row() + 1, newItem)
        ui.frameList.setCurrentIndex(newItem.index())
        window.setWindowModified(True)
    
def deleteFrame():
    frame = ui.frameList.currentIndex()
    if not frame.model():
        return
    frameModel.removeRow(frame.row())
    ui.frameList.selectionModel().currentChanged.emit(ui.frameList.currentIndex(), ui.frameList.currentIndex())
    window.setWindowModified(True)
    
playing = False
reversing = False
timer = QTimer()
    
def nextFrame():
    global reversing
    if playing and reversing:
        return prevFrame()
    frame = ui.frameList.currentIndex()
    item = frameModel.item(frame.row() + 1)
    if not item:
        if playing and ui.reversible.isChecked():
            reversing = True
            return prevFrame()
        item = frameModel.item(0)
        if not item:
            return
    ui.frameList.setCurrentIndex(item.index())        
    
def prevFrame():
    global reversing
    count = frameModel.rowCount()
    if count == 0:
        return
    frame = ui.frameList.currentIndex()
    if not frame.model():
        row = -1
    else:
        row = frame.row() - 1
    if row < 0:
        if playing and reversing:
            reversing = False
            return nextFrame()
        row = count - 1
        
    item = frameModel.item(row)
    if not item:
        return
    ui.frameList.setCurrentIndex(item.index())        
    
def playPause():
    global playing
    playing = not playing
    ui.sourcesGroup.setEnabled(not playing)
    ui.frameGroup2.setEnabled(not playing)
    ui.playPause.setIcon(QIcon.fromTheme("media-playback-pause" if playing else "media-playback-start"))
    ui.playPause.setText("Pause" if playing else "Play")
    
    timer.setInterval(ui.duration.value())
    if playing:
        timer.start()
    else:
        timer.stop()
        
def showFrame(current, previous):
    if not current.model():
        preview.setVisible(False)
        return
    preview.setVisible(True)
    pixmap = current.model().itemFromIndex(current).data()
    preview.setPixmap(pixmap)
    previewScene.setSceneRect(QRectF(pixmap.rect()))
    ui.preview.fitInView(previewScene.sceneRect(), mode=Qt.KeepAspectRatio)
        
def stop():
    global playing
    playing = True
    playPause()
    item = frameModel.item(0)
    if item:
        ui.frameList.setCurrentIndex(item.index())
        
def modify():
    window.setWindowModified(True)

timer.timeout.connect(nextFrame)

class MainWindow(QMainWindow):
    def closeEvent(self, event):
        if self.isWindowModified():
            val = QMessageBox.warning(self, animFile, "The animation has been changed. Do you want to save it?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if val == QMessageBox.Yes:
                saveFile()
                event.accept()
            elif val == QMessageBox.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

window = MainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
window.setWindowTitle("")

animDir = None
animFile = None

def readDir():
    model.clear()
    frames = [f for f in listdir(animDir) if (isfile(join(animDir, f)) and f.lower().endswith(('.png', '.webp', '.jpg', '.bmp')))]

    for frame in frames:
        item = QStandardItem(frame)
        pixmap = QPixmap(join(animDir, frame))
        item.setIcon(QIcon(pixmap))
        item.setToolTip(frame)
        item.setData(pixmap)
        item.setDropEnabled(False)
    
        model.appendRow(item)
    
    sort()

def openFile():
    global animFile, animDir
    animFile = QFileDialog.getOpenFileName(window, "Select an animation to open...", QDir.currentPath(), "libsuperderpy animation (*.ini)")
    animFile = animFile[0]
    if animFile=="":
        return
    d = QDir(animFile)
    d.cdUp()
    animDir = d.path()

    config = ConfigParser()
    config.read(animFile)
    ui.reversible.setChecked(config.getboolean('animation', 'bidir', fallback=False))
    ui.duration.setValue(config.getint('animation', 'duration', fallback=100))
    frames = config.getint('animation', 'frames')
    for i in range(frames):
        section = 'frame' + str(i)
        frame = config.get(section, 'file')
        item = QStandardItem(frame)
        pixmap = QPixmap(join(animDir, frame))
        item.setIcon(QIcon(pixmap))
        item.setToolTip(frame)
        item.setData(pixmap)
        item.setDropEnabled(False)
        frameModel.appendRow(item)
    readDir()
    window.setWindowFilePath(animFile)
    window.setWindowModified(False)
        
def newFile():
    global animDir, animFile
    animDir = QFileDialog.getExistingDirectory(window, "Select a directory with animation frames.", QDir.currentPath())
    
    if animDir=="":
        return
    
    readDir()
    
    frameModel.clear()
    
    window.setWindowFilePath("")
    
    animFile = None
    ui.counter.setText('-/-')
    window.setWindowModified(False)


def newOrOpen():
    val = QMessageBox.question(window, "libsuperderpy animation editor", "Do you want to open an existing animation?")
    if val == QMessageBox.Yes:
        openFile()
    else:
        newFile()
        
def saveFileAs():
    global animFile
    f = QFileDialog.getSaveFileName(window, "Save animation", animDir, "libsuperderpy animation (*.ini)")
    f = f[0]
    if f!="":
        animFile = f
        saveFile()
    
def saveFile():
    if not animFile:
        return saveFileAs()
    config = ConfigParser()
    #config.read(animFile)
    config.add_section('animation')
    config.set('animation', 'duration', str(ui.duration.value()))
    if ui.reversible.isChecked():
        config.set('animation', 'bidir', '1')
    config.set('animation', 'frames', str(frameModel.rowCount()))
    for i in range(frameModel.rowCount()):
        section = 'frame' + str(i)
        config.add_section(section)
        config.set(section, 'file', frameModel.item(i).text())

    with open(animFile, 'w') as configfile:
        config.write(configfile)
    window.setWindowModified(False)
    window.setWindowFilePath(animFile)
    
model = QStandardItemModel(ui.sourcesList)
frameModel = QStandardItemModel(ui.frameList)
newOrOpen()

previewScene = QGraphicsScene(window)
ui.preview.setScene(previewScene)
preview = previewScene.addPixmap(QPixmap())
    
def unreverse():
    global reversing
    reversing = False

ui.sort.pressed.connect(sort)
ui.addFrame.pressed.connect(addFrame)
ui.addAll.pressed.connect(addAll)
ui.moveLeft.pressed.connect(moveFrameLeft)
ui.moveRight.pressed.connect(moveFrameRight)
ui.copy.pressed.connect(duplicateFrame)
ui.deleteBtn.pressed.connect(deleteFrame)
ui.playPause.pressed.connect(playPause)
ui.stop.pressed.connect(stop)
ui.goLeft.pressed.connect(prevFrame)
ui.goRight.pressed.connect(nextFrame)
ui.reversible.stateChanged.connect(unreverse)
ui.reversible.stateChanged.connect(modify)
ui.duration.valueChanged.connect(lambda val: timer.setInterval(val))
ui.duration.valueChanged.connect(modify)
ui.actionNew.triggered.connect(newFile)
ui.actionOpen.triggered.connect(openFile)
ui.actionSave.triggered.connect(saveFile)
ui.actionSave_as.triggered.connect(saveFileAs)
ui.actionClose.triggered.connect(lambda: app.quit())
 
ui.sourcesList.itemSelected.connect(addFrame)
ui.frameList.itemRemoved.connect(deleteFrame)

frameModel.itemChanged.connect(lambda item: QTimer.singleShot(50, lambda: ui.frameList.setCurrentIndex(item.index())))
frameModel.itemChanged.connect(modify)
 
ui.frameList.setDragDropMode(QAbstractItemView.InternalMove)
ui.sourcesList.setDragDropMode(QAbstractItemView.DragOnly)
ui.sourcesList.setModel(model)
ui.frameList.setModel(frameModel)

ui.sourcesList.dragStarted.connect(lambda: ui.frameList.setDragDropMode(QAbstractItemView.DragDrop))
ui.frameList.dragStarted.connect(lambda: ui.frameList.setDragDropMode(QAbstractItemView.InternalMove))

ui.frameList.selectionModel().currentChanged.connect(lambda current, previous: ui.counter.setText((str(current.row() + 1) + '/' + str(current.model().rowCount())) if current.model() else '-/-'))

ui.frameList.selectionModel().currentChanged.connect(showFrame)

window.show()
app.exec_()
