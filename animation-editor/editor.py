#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from os import listdir, walk
from os.path import isfile, isdir, join, relpath, abspath, basename
from configparser import ConfigParser
from EditorUI import Ui_MainWindow

app = QApplication(sys.argv)
app.setApplicationDisplayName("libsuperderpy animation editor")

order=Qt.DescendingOrder

class Progress(QDialog):
    def __init__(self, parent, title='Loading'):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 500, 25)
        self.progress.setMaximum(100)

    def setMax(self, val):
        self.progress.setMaximum(val)

    def setValue(self, val):
        self.progress.setValue(val)

def sort():
    global order, model
    if order==Qt.DescendingOrder:
        order=Qt.AscendingOrder
    else:
        order=Qt.DescendingOrder
    model.sort(0, order=order)

def addFrame():
    frames = ui.sourcesList.selectedIndexes()
    frames.sort(key=lambda frame: frame.row())
    ui.frameList.clearSelection()
    toselect = []
    for index in frames:
        if index.model():
            item = index.model().itemFromIndex(index)
            newItem = QStandardItem(item)
            if ui.frameList.currentIndex().model():
                frameModel.insertRow(ui.frameList.currentIndex().row() + 1, newItem)
            else:
                frameModel.appendRow(newItem)
            toselect.append(newItem)
            ui.frameList.setCurrentIndex(newItem.index())
            window.setWindowModified(True)
    for frame in toselect:
        ui.frameList.selectionModel().select(frame.index(), QItemSelectionModel.Select)

def addAll():
    count = model.rowCount()
    for i in range(count):
        item = model.item(i)
        frameModel.appendRow(QStandardItem(item))
    if count > 0:
        window.setWindowModified(True)

def moveFrameLeft():
    frames = ui.frameList.selectedIndexes()
    frames.sort(key=lambda frame: frame.row())
    ui.frameList.clearSelection()
    toselect = []
    for frame in frames:
        if not frame.model():
            continue
        newRow = frame.row() - 1
        if newRow < 0:
            continue
        rows = frameModel.takeRow(frame.row())
        frameModel.insertRow(newRow, rows)
        toselect.append(rows[0])
        ui.frameList.setCurrentIndex(rows[0].index())
        window.setWindowModified(True)
    for frame in toselect:
        ui.frameList.selectionModel().select(frame.index(), QItemSelectionModel.Select)

def moveFrameRight():
    frames = ui.frameList.selectedIndexes()
    frames.sort(key=lambda frame: frame.row())
    frames.reverse()
    ui.frameList.clearSelection()
    toselect = []
    for frame in frames:
        if not frame.model():
            continue
        newRow = frame.row() + 1
        if newRow >= frameModel.rowCount():
            continue
        rows = frameModel.takeRow(frame.row())
        frameModel.insertRow(newRow, rows)
        toselect.append(rows[0])
        ui.frameList.setCurrentIndex(rows[0].index())
        window.setWindowModified(True)
    toselect.reverse()
    for frame in toselect:
        ui.frameList.selectionModel().select(frame.index(), QItemSelectionModel.Select)

def duplicateFrame():
    frames = ui.frameList.selectedIndexes()
    frames.sort(key=lambda frame: frame.row())
    frames.reverse()
    toselect = []
    for index in frames:
        if index.model():
            item = index.model().itemFromIndex(index)
            newItem = QStandardItem(item)
            frameModel.insertRow(frames[0].row() + 1, newItem)
            toselect.append(newItem)
            ui.frameList.setCurrentIndex(newItem.index())
            window.setWindowModified(True)
    for frame in toselect:
        ui.frameList.selectionModel().select(frame.index(), QItemSelectionModel.Select)

def deleteFrame():
    frames = ui.frameList.selectedIndexes()
    frames.sort(key=lambda frame: frame.row())
    frames.reverse()
    for frame in frames:
        if not frame.model():
            return
        frameModel.removeRow(frame.row())
        ui.frameList.selectionModel().currentChanged.emit(ui.frameList.currentIndex(), ui.frameList.currentIndex())
        window.setWindowModified(True)
    ui.frameList.selectionModel().select(ui.frameList.currentIndex(), QItemSelectionModel.Select)

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

overrideLock = False

def readDir(override=None):
    global overrideLock
    if overrideLock:
        return
    overrideLock = True
    model.clear()
    p = animDir
    if override:
        p = override
    frames = [f for f in listdir(p) if (isfile(join(p, f)) and f.lower().endswith(('.png', '.webp', '.jpg', '.bmp')))]
    if not override:
        subdirs = list(dict.fromkeys([dp for dp, dn, fn in walk(p) for f in fn]))
        ui.subdirs.clear()
        ui.subdirs.addItems(subdirs)
    overrideLock = False

    dialog = Progress(window, "Reading working directory")
    dialog.setMax(len(frames))
    dialog.show()
    i = 0
    for frame in frames:
        print("Loading {}...".format(frame))
        dialog.setValue(i)
        item = QStandardItem(frame)
        pixmap = QPixmap(join(p, frame))
        if pixmap.width() > 1280:
            pixmap = pixmap.scaledToWidth(1280)
        item.setIcon(QIcon(pixmap))
        item.setToolTip(relpath(join(p,frame), animDir))
        item.setData(pixmap)
        item.setDropEnabled(False)

        model.appendRow(item)
        app.processEvents()
        i = i+1

    sort()
    dialog.hide()

def openFile(filename = None):
    global animFile, animDir
    if not filename:
        animFile = QFileDialog.getOpenFileName(window, "Select an animation to open...", animDir if animDir else QDir.currentPath(), "libsuperderpy animation (*.ini)")
        animFile = animFile[0]
    else:
        animFile = filename

    if animFile=="":
        return
    d = QDir(animFile)
    d.cdUp()
    newDir = False
    if not animDir or abspath(animDir) != abspath(d.path()):
        newDir = True
        animDir = d.path()

    frameModel.clear()

    config = ConfigParser()
    config.read(animFile)
    ui.reversible.setChecked(config.getboolean('animation', 'bidir', fallback=False))
    ui.duration.setValue(config.getint('animation', 'duration', fallback=100))
    frames = config.getint('animation', 'frames')
    dialog = Progress(window, "Loading animation frames")
    dialog.setMax(frames)
    dialog.show()
    for i in range(frames):
        section = 'frame' + str(i)
        frame = config.get(section, 'file')
        print("Loading {}...".format(frame))
        dialog.setValue(i)
        item = QStandardItem(basename(frame))
        pixmap = QPixmap(join(animDir, frame))
        if pixmap.width() > 1280:
            pixmap = pixmap.scaledToWidth(1280)
        item.setIcon(QIcon(pixmap))
        item.setToolTip(frame)
        item.setData(pixmap)
        item.setDropEnabled(False)
        frameModel.appendRow(item)
        app.processEvents()
    dialog.hide()
    if newDir:
        readDir()
    window.setWindowFilePath(animFile)
    window.setWindowModified(False)


def importFrames():
    filename = QFileDialog.getOpenFileName(window, "Select an animation to import...", animDir, "libsuperderpy animation (*.ini)")
    filename = filename[0]

    if filename=="":
        return

    d = QDir(relpath(filename, animDir))
    d.cdUp()
    path = d.path()

    config = ConfigParser()
    config.read(filename)
    frames = config.getint('animation', 'frames')
    dialog = Progress(window, "Importing animation frames")
    dialog.setMax(frames)
    dialog.show()
    for i in range(frames):
        section = 'frame' + str(i)
        frame = config.get(section, 'file')
        print("Loading {}...".format(frame))
        dialog.setValue(i)
        item = QStandardItem(basename(frame))
        pixmap = QPixmap(join(join(animDir, path), frame))
        if pixmap.width() > 1280:
            pixmap = pixmap.scaledToWidth(1280)
        item.setIcon(QIcon(pixmap))
        item.setToolTip(relpath(join(path, frame), animDir))
        item.setData(pixmap)
        item.setDropEnabled(False)
        frameModel.appendRow(item)
        app.processEvents()
    dialog.hide()
    window.setWindowModified(True)
    ui.frameList.selectionModel().currentChanged.emit(ui.frameList.currentIndex(), ui.frameList.currentIndex())

def newFile(directory=None):
    global animDir, animFile
    animDir = directory

    if not animDir:
        animDir = QFileDialog.getExistingDirectory(window, "Select a directory with animation frames.", QDir.currentPath())

    if not animDir:
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
        config.set(section, 'file', frameModel.item(i).toolTip())

    with open(animFile, 'w') as configfile:
        config.write(configfile)
    window.setWindowModified(False)
    window.setWindowFilePath(animFile)

model = QStandardItemModel(ui.sourcesList)
frameModel = QStandardItemModel(ui.frameList)

parser = argparse.ArgumentParser(description='Animation editor for libsuperderpy game engine.')
parser.add_argument('path', type=str, nargs='?',
                    help='existing animation or directory to open')
parser.add_argument('-a', '--add', action='store_true',
                    help='pre-add all available images to the animation')
parser.add_argument('-d', '--duration', metavar='ms', type=int,
                    help='set the global frame duration in miliseconds')
parser.add_argument('-m', '--maximize', action='store_true',
                    help='start maximized')
parser.add_argument('-p', '--play', action='store_true',
                    help='automatically start playing the animation')
parser.add_argument('-s', '--save', metavar='path', type=str,
                    help='pre-save the animation to the specified path')

args = parser.parse_args()

if args.path and isdir(args.path):
    newFile(args.path)
elif args.path:
    openFile(args.path)
else:
    newOrOpen()

previewScene = QGraphicsScene(window)
ui.preview.setScene(previewScene)
ui.preview.setBackgroundBrush(QBrush(QColor("grey"), Qt.Dense3Pattern))
preview = previewScene.addPixmap(QPixmap())

def unreverse():
    global reversing
    reversing = False

ui.sort.pressed.connect(sort)
ui.addFrame.pressed.connect(addFrame)
ui.addAll.pressed.connect(addAll)
ui.moveLeft.pressed.connect(moveFrameLeft)
ui.moveRight.pressed.connect(moveFrameRight)
ui.importBtn.pressed.connect(importFrames)
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
ui.subdirs.currentTextChanged.connect(readDir)

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

if args.add:
    addAll()
if args.duration:
    ui.duration.setValue(args.duration)
if args.save:
    animFile = args.save
    saveFile()
if args.play:
    playPause()

if args.maximize:
    window.showMaximized()
else:
    window.show()

app.exec_()
