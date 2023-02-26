#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from os import listdir, walk
from os.path import isfile, isdir, join, relpath, abspath, basename
from configparser import ConfigParser
from EditorUI import Ui_MainWindow

app = QApplication(sys.argv)
app.setApplicationName("libsuperderpy-animation-editor")
app.setApplicationDisplayName("libsuperderpy animation editor")

order=Qt.AscendingOrder

def fitInView(self, rect, flags = Qt.IgnoreAspectRatio):
    if self.scene() is None or rect.isNull():
        return
    self.last_scene_roi = rect
    unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
    self.scale(1/unity.width(), 1/unity.height())
    viewRect = self.viewport().rect()
    sceneRect = self.transform().mapRect(rect)
    xratio = viewRect.width() / sceneRect.width()
    yratio = viewRect.height() / sceneRect.height()
    if flags == Qt.KeepAspectRatio:
        xratio = yratio = min(xratio, yratio)
    elif flags == Qt.KeepAspectRatioByExpanding:
        xratio = yratio = max(xratio, yratio)
    self.scale(xratio, yratio)
    self.centerOn(rect.center())

class AnimationFrameData:
    pixmap = None
    filename = None
    duration = -1

    def __init__(self, pixmap, filename, duration = -1):
        self.pixmap = pixmap
        self.filename = filename
        self.duration = duration

    def withDuration(self, duration):
        return AnimationFrameData(self.pixmap, self.filename, duration)

    def saveConfig(self, config, section):
        config.set(section, 'file', self.filename)
        if self.duration != -1:
            config.set(section, 'duration', str(self.duration))

class StateManager:
    state = None
    history = None
    redo = None
    stored = None
    comparator = None
    callback = None

    def __init__(self, comparator, callback = None):
        self.history = []
        self.redo = []
        self.comparator = comparator
        self.callback = callback

    def pushState(self, state):
        if self.comparator(self.state, state):
            self.state = state # for selection
            return
        if self.state:
            self.history.append(self.state)
        self.state = state
        self.redo = []
        if self.callback:
            self.callback(self.isStored())

    def undoState(self):
        if len(self.history) == 0:
            return
        self.redo.append(self.state)
        self.state = self.history.pop()
        if self.callback:
            self.callback(self.isStored())
        return self.state

    def redoState(self):
        if len(self.redo) == 0:
            return
        if self.state:
            self.history.append(self.state)
        self.state = self.redo.pop()
        if self.callback:
            self.callback(self.isStored())
        return self.state

    def clearState(self):
        self.stored = None
        self.state = None
        self.history = []
        self.redo = []

    def markAsStored(self):
        self.stored = self.state
        if self.callback:
            self.callback(self.isStored())

    def isStored(self):
        return self.comparator(self.stored, self.state)

class FrameCache:
    cache = None
    cachedir = None
    size = None
    quality = None

    def __init__(self, cachedir, size, quality = 80):
        self.cache = {}
        self.cachedir = cachedir
        self.size = size
        self.quality = quality
        QDir().mkpath(cachedir)

    def load(self, img):
        path = abspath(img)
        if self.cache.get(path):
            return self.cache[path]
        file = QFile(path)
        if file.open(QIODevice.ReadOnly):
            fileData = file.readAll()
            hash = bytes(QCryptographicHash.hash(fileData, QCryptographicHash.Md5)).hex()
            name, ext = os.path.splitext(path)
            cachepath = QDir(self.cachedir).absoluteFilePath(hash + ext)
            if QFileInfo(cachepath).exists():
                pixmap = QPixmap(cachepath)
            else:
                pixmap = QPixmap(path)
                if pixmap.width() > self.size:
                    pixmap = pixmap.scaledToWidth(self.size, mode=Qt.SmoothTransformation)
                    pixmap.save(cachepath, quality=self.quality)
            self.cache[path] = pixmap
        return pixmap

cache = FrameCache(QStandardPaths.writableLocation(QStandardPaths.CacheLocation), 1280)

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

class State(list):
    selection = None
    current = None
    duration = None
    reversible = None

def getState():
    items = State()
    for i in range(frameModel.rowCount()):
        items.append(QStandardItem(frameModel.item(i)))
    items.selection = [index.row() for index in ui.frameList.selectedIndexes()]
    items.duration = ui.duration.value()
    items.reversible = ui.reversible.isChecked()
    items.current = ui.frameList.currentIndex().row()
    return items

def compareState(a, b):
    if a == b:
        return True

    if not a or not b:
        return False

    if a.duration != b.duration:
        return False

    if a.reversible != b.reversible:
        return False

    if len(a) != len(b):
        return False

    for i in range(len(a)):
        if a[i].data().filename != b[i].data().filename:
            return False

        if a[i].data().duration != b[i].data().duration:
            return False

    return True

def stateChanged(modified=True):
    window.setWindowModified(not modified)

state = StateManager(compareState, stateChanged)
clipboard = []

def applyState(state):
    if state:
        current = ui.frameList.currentIndex()
        frameModel.clear()
        for item in state:
            frame = QStandardItem(item)
            frameModel.appendRow(frame)

        ui.duration.setValue(state.duration)
        ui.reversible.setChecked(state.reversible)
        if state.current >= 0:
            ui.frameList.setCurrentIndex(frameModel.item(state.current).index())

        ui.frameList.clearSelection()
        for i in state.selection:
            ui.frameList.selectionModel().select(item.index(), QItemSelectionModel.Select)

        ui.frameList.selectionModel().currentChanged.emit(ui.frameList.currentIndex(), ui.frameList.currentIndex())

def undoState():
    newState = state.undoState()
    applyState(newState)

def redoState():
    newState = state.redoState()
    applyState(newState)

def copyFrames():
    global clipboard
    frames = ui.frameList.selectedIndexes()
    frames.sort(key=lambda frame: frame.row())
    clipboard = []
    for frame in frames:
        clipboard.append(QStandardItem(frameModel.item(frame.row())))

def cutFrames():
    copyFrames()
    deleteFrame()

def pasteFrames():
    state.pushState(getState()) # update selection
    ui.frameList.clearSelection()
    frames = [QStandardItem(item) for item in clipboard]
    i = 1
    for frame in frames:
        if ui.frameList.currentIndex().model():
            frameModel.insertRow(ui.frameList.currentIndex().row() + i, frame)
        else:
            frameModel.appendRow(frame)
        i += 1
    for frame in frames:
        ui.frameList.selectionModel().select(frame.index(), QItemSelectionModel.Select)
    state.pushState(getState())

def addFrame():
    state.pushState(getState()) # update selection
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
    for frame in toselect:
        ui.frameList.selectionModel().select(frame.index(), QItemSelectionModel.Select)
    state.pushState(getState())

def addAll():
    state.pushState(getState()) # update selection
    count = model.rowCount()
    for i in range(count):
        item = model.item(i)
        frameModel.appendRow(QStandardItem(item))
    state.pushState(getState())

def moveFrameLeft():
    state.pushState(getState()) # update selection
    frames = ui.frameList.selectedIndexes()
    frames.sort(key=lambda frame: frame.row())
    ui.frameList.clearSelection()
    toselect = []
    for frame in frames:
        if not frame.model():
            continue
        newRow = frame.row() - ui.moveNumber.value()
        if newRow < 0:
            continue
        rows = frameModel.takeRow(frame.row())
        frameModel.insertRow(newRow, rows)
        toselect.append(rows[0])
        ui.frameList.setCurrentIndex(rows[0].index())
    for frame in toselect:
        ui.frameList.selectionModel().select(frame.index(), QItemSelectionModel.Select)
    state.pushState(getState())

def moveFrameRight():
    state.pushState(getState()) # update selection
    frames = ui.frameList.selectedIndexes()
    frames.sort(key=lambda frame: frame.row())
    frames.reverse()
    ui.frameList.clearSelection()
    toselect = []
    for frame in frames:
        if not frame.model():
            continue
        newRow = frame.row() + ui.moveNumber.value()
        if newRow >= frameModel.rowCount():
            continue
        rows = frameModel.takeRow(frame.row())
        frameModel.insertRow(newRow, rows)
        toselect.append(rows[0])
        ui.frameList.setCurrentIndex(rows[0].index())
    toselect.reverse()
    for frame in toselect:
        ui.frameList.selectionModel().select(frame.index(), QItemSelectionModel.Select)
    state.pushState(getState())

def duplicateFrame():
    state.pushState(getState()) # update selection
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
    for frame in toselect:
        ui.frameList.selectionModel().select(frame.index(), QItemSelectionModel.Select)
    state.pushState(getState())

def reverseFrames():
    state.pushState(getState()) # update selection
    frames = ui.frameList.selectedIndexes()
    frames.sort(key=lambda frame: frame.row())
    frames.reverse()
    for i in range(len(frames) // 2):
        frame = frames[i]
        frame2 = frames[len(frames) - i - 1]
        row = frame.row()
        row2 = frame2.row()
        rows = frameModel.takeRow(row)
        rows2 = frameModel.takeRow(row2)
        frameModel.insertRow(row2, rows)
        frameModel.insertRow(row, rows2)
    ui.frameList.selectionModel().clearSelection()
    for frame in frames:
        ui.frameList.selectionModel().select(frame, QItemSelectionModel.Select)
    state.pushState(getState())

def exportFrames():
    frames = ui.frameList.selectedIndexes()
    frames.sort(key=lambda frame: frame.row())

    f = QFileDialog.getSaveFileName(window, "Export selected frames", animDir, "libsuperderpy animation (*.ini)")
    f = f[0]
    if f=="":
        return

    config = ConfigParser()
    #config.read(animFile)
    config.add_section('animation')
    config.set('animation', 'duration', str(ui.duration.value()))
    if ui.reversible.isChecked():
        config.set('animation', 'bidir', '1')
    i = 0
    for index in frames:
        if index.model():
            item = index.model().itemFromIndex(index)
            section = 'frame' + str(i)
            config.add_section(section)
            item.data().saveConfig(config, section)
            i = i + 1
    config.set('animation', 'frames', str(i))

    with open(f, 'w') as configfile:
        config.write(configfile)

def deleteFrame():
    state.pushState(getState()) # update selection
    frames = ui.frameList.selectedIndexes()
    frames.sort(key=lambda frame: frame.row())
    frames.reverse()
    for frame in frames:
        if not frame.model():
            return
        frameModel.removeRow(frame.row())
        ui.frameList.selectionModel().currentChanged.emit(ui.frameList.currentIndex(), ui.frameList.currentIndex())
    ui.frameList.selectionModel().select(ui.frameList.currentIndex(), QItemSelectionModel.Select)
    state.pushState(getState())

playing = False
reversing = False
timer = QTimer()

def setFrameDuration(value):
    frame = ui.frameList.currentIndex()
    item = frameModel.item(frame.row())
    if item:
        item.setData(item.data().setDuration(value))
        timer.setInterval(value if value >= 0 else ui.duration.value())
        font = QFont()
        font.setBold(value >= 0)
        item.setFont(font)

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
    data = item.data()
    timer.setInterval(data.duration if data.duration >= 0 else ui.duration.value())

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

    if playing:
        timer.start()
    else:
        timer.stop()

def showFrame(current = None, previous=None):
    if not current:
        current = ui.frameList.selectionModel().currentIndex()
    if not current.model():
        preview.setVisible(False)
        ui.frameDuration.setEnabled(False)
        return
    preview.setVisible(True)
    ui.frameDuration.setEnabled(True)

    item = current.model().itemFromIndex(current)
    data = item.data()
    timer.setInterval(data.duration if data.duration >= 0 else ui.duration.value())
    ui.frameDuration.setValue(data.duration)

    pixmap = data.pixmap
    preview.setPixmap(pixmap)
    previewScene.setSceneRect(QRectF(pixmap.rect()))
    fitInView(ui.preview, previewScene.sceneRect(), flags=Qt.KeepAspectRatio)
    mapped = ui.preview.mapToScene(ui.preview.rect()).boundingRect()
    previewBg.setRect(QRectF(ui.preview.rect()))
    previewBg.setPos(mapped.topLeft())

def stop():
    global playing
    playing = True
    playPause()
    item = frameModel.item(0)
    if item:
        ui.frameList.setCurrentIndex(item.index())

def modify():
    state.pushState(getState())

timer.timeout.connect(nextFrame)

def askSave():
    if window.isWindowModified():
        val = QMessageBox.warning(window, animFile, "The animation has been changed. Do you want to save it?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if val == QMessageBox.Yes:
            saveFile()
            return True
        elif val == QMessageBox.No:
            return True
        else:
            return False
    else:
        return True

def toggleLinear():
    if ui.actionUse_linear_filtering.isChecked():
        preview.setTransformationMode(Qt.SmoothTransformation)
    else:
        preview.setTransformationMode(Qt.FastTransformation)

class MainWindow(QMainWindow):

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().urls():
            url = event.mimeData().urls()[0].toLocalFile()
            if url.lower()[-4:] == '.ini':
                openFile(url)

    def closeEvent(self, event):
        if askSave():
            event.accept()
        else:
            event.ignore()

    def eventFilter(self, source, event):
        if playing and source != ui.playPause and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Space:
                playPause()
                return True
        if source == ui.preview and event.type() == QEvent.KeyPress and ui.preview.isFullScreen():
            if event.key() == Qt.Key_Escape:
                unfullscreen()
            if event.key() == Qt.Key_Space:
                playPause()
            if event.key() == Qt.Key_Left:
                prevFrame()
            if event.key() == Qt.Key_Right:
                nextFrame()
            if event.key() == Qt.Key_Down or event.key() == Qt.Key_Home:
                stop()
            return True
        if source == ui.preview and event.type() == QEvent.Resize or event.type() == QEvent.Show or event.type() == QEvent.FocusIn:
            showFrame()
        return super(MainWindow, self).eventFilter(source, event)

window = MainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
window.setWindowTitle("")

window.setAcceptDrops(True)

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
        filename = join(p, frame)
        pixmap = cache.load(filename)
        item.setIcon(QIcon(pixmap))
        item.setData(AnimationFrameData(pixmap, relpath(filename, animDir)))
        item.setToolTip(item.data().filename)
        item.setDropEnabled(False)

        model.appendRow(item)
        app.processEvents()
        i = i+1

    model.sort(0, order=order)
    dialog.hide()

def openFile(filename = None):
    global animFile, animDir, clipboard
    if not askSave():
        return
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
        duration = int(config.get(section, 'duration', fallback=-1))
        print("Loading {}...".format(frame))
        dialog.setValue(i)
        item = QStandardItem(basename(frame))
        filename = join(animDir, frame)
        pixmap = cache.load(filename)
        item.setIcon(QIcon(pixmap))
        item.setData(AnimationFrameData(pixmap, frame, duration=duration))
        item.setToolTip(item.data().filename)
        item.setDropEnabled(False)
        font = QFont()
        font.setBold(duration >= 0)
        item.setFont(font)
        frameModel.appendRow(item)
        app.processEvents()
    dialog.hide()
    if newDir:
        readDir()
    print("Finished.")
    window.setWindowFilePath(animFile)
    window.setWindowModified(False)
    state.clearState()
    state.pushState(getState())
    state.markAsStored()
    clipboard = []

def importFrames():
    state.pushState(getState()) # update selection
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
        filename = join(join(animDir, path), frame)
        pixmap = cache.load(filename)
        item.setIcon(QIcon(pixmap))
        item.setData(AnimationFrameData(pixmap, relpath(join(path, frame), animDir)))
        item.setToolTip(item.data().filename)
        item.setDropEnabled(False)
        frameModel.appendRow(item)
        app.processEvents()
    print("Import finished.")
    dialog.hide()
    window.setWindowModified(True)
    ui.frameList.selectionModel().currentChanged.emit(ui.frameList.currentIndex(), ui.frameList.currentIndex())
    state.pushState(getState())

def newFile(directory=None):
    global animDir, animFile, clipboard
    if not askSave():
        return
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
    state.clearState()
    clipboard = []

def unfullscreen():
    ui.preview.showNormal()
    ui.preview.setFrameShape(QFrame.StyledPanel)
    ui.verticalLayout_3.insertWidget(0, ui.preview)
    ui.preview.setCursor(Qt.ArrowCursor);
    ui.preview.setBackgroundBrush(QBrush(QColor("white")))
    previewBg.show()
    window.show()

def fullscreen():
    window.hide()
    ui.preview.setParent(None)
    ui.preview.setFrameShape(QFrame.NoFrame)
    ui.preview.setCursor(Qt.BlankCursor);
    ui.preview.setBackgroundBrush(QBrush(QColor("black")))
    previewBg.hide()
    ui.preview.showFullScreen()

def newOrOpen():
    val = QMessageBox.question(window, "libsuperderpy animation editor", "Do you want to open an existing animation?")
    if val == QMessageBox.Yes:
        openFile()
    else:
        newFile()

def saveFileAs():
    global animFile
    f = QFileDialog.getSaveFileName(window, "Save animation", animFile if animFile else animDir, "libsuperderpy animation (*.ini)")
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
        frameModel.item(i).data().saveConfig(config, section)

    with open(animFile, 'w') as configfile:
        config.write(configfile)

    state.markAsStored()
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
parser.add_argument('-f', '--fullscreen', action='store_true',
                    help='play the animation fullscreen (implies --play)')
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
ui.preview.setBackgroundBrush(QBrush(QColor("white")))
previewBg = previewScene.addRect(0, 0, 1, 1, pen = QPen(Qt.NoPen), brush = QBrush(QColor("grey"), Qt.Dense4Pattern))
previewBg.setFlag(QGraphicsItem.ItemIgnoresTransformations)
preview = previewScene.addPixmap(QPixmap())
preview.setTransformationMode(Qt.SmoothTransformation)
ui.preview.installEventFilter(window)

window.installEventFilter(window)

def unreverse():
    global reversing
    reversing = False

ui.sort.clicked.connect(sort)
ui.addFrame.clicked.connect(addFrame)
ui.addAll.clicked.connect(addAll)
ui.moveLeft.clicked.connect(moveFrameLeft)
ui.moveRight.clicked.connect(moveFrameRight)
ui.importBtn.clicked.connect(importFrames)
ui.reverseBtn.clicked.connect(reverseFrames)
ui.exportBtn.clicked.connect(exportFrames)
ui.copy.clicked.connect(duplicateFrame)
ui.deleteBtn.clicked.connect(deleteFrame)
ui.playPause.clicked.connect(playPause)
ui.stop.clicked.connect(stop)
ui.goLeft.clicked.connect(prevFrame)
ui.goRight.clicked.connect(nextFrame)
ui.reversible.stateChanged.connect(unreverse)
ui.reversible.stateChanged.connect(modify)
ui.duration.valueChanged.connect(lambda val: timer.setInterval(val))
ui.duration.valueChanged.connect(modify)
ui.frameDuration.valueChanged.connect(setFrameDuration)
ui.frameDuration.valueChanged.connect(modify)
ui.actionNew.triggered.connect(newFile)
ui.actionOpen.triggered.connect(openFile)
ui.actionSave.triggered.connect(saveFile)
ui.actionSave_as.triggered.connect(saveFileAs)
ui.actionClose.triggered.connect(lambda: app.quit())
ui.actionUndo.triggered.connect(undoState)
ui.actionRedo.triggered.connect(redoState)
ui.actionCut.triggered.connect(cutFrames)
ui.actionCopy.triggered.connect(copyFrames)
ui.actionPaste.triggered.connect(pasteFrames)
ui.actionUse_linear_filtering.triggered.connect(toggleLinear)
ui.subdirs.currentTextChanged.connect(readDir)
ui.refreshSources.clicked.connect(readDir)
ui.fullscreen.clicked.connect(fullscreen)

ui.sourcesList.itemSelected.connect(addFrame)
ui.frameList.itemRemoved.connect(deleteFrame)

frameModel.itemChanged.connect(lambda item: QTimer.singleShot(50, lambda: ui.frameList.setCurrentIndex(item.index())))
frameModel.itemChanged.connect(modify)

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
if args.play or args.fullscreen:
    playPause()

if args.maximize:
    window.showMaximized()
else:
    window.show()

if args.fullscreen:
    fullscreen()

app.exec_()
