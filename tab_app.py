import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class tabdemo(QTabWidget):
   def __init__(self, parent = None):
      super(tabdemo, self).__init__(parent)
      self.tab1 = QWidget()
      self.tab2 = QWidget()
      self.tab3 = QWidget()
		
      self.addTab(self.tab1,"Tab 1")
      self.addTab(self.tab2,"Tab 2")
      self.addTab(self.tab3,"Tab 3")
      self.tab1UI()
      self.tab2UI()
      self.tab3UI()
      self.setWindowTitle("tab demo")
		
   def tab1UI(self):
			self._processes = []
			self.resize(800, 600)
			self.terminal = QWidget(self)
			self.layout = QGridLayout(self)
			pixmap = QPixmap('sbgs_logo.png')
			logo = QLabel(self)
			logo.setPixmap(pixmap)
			self.layout.addWidget(logo, 1, 1)
			#logo.setMaximumWidth(120)
			self.layout.addWidget(self.terminal, 1,3)
			self.button1 = QPushButton('Restore RFS')
			self.button2 = QPushButton('Restart')
			self.button3 = QPushButton('Exit')
			self.button4 = QPushButton('Flash Uboot')
			self.elid = QLabel("ELID ID")
			self.elidEdit = QLineEdit()
			self.elidEdit.setMaxLength(4)
			self.layout.addWidget(self.button1,2,1)
			self.layout.addWidget(self.elid,2,2)
			self.layout.addWidget(self.elidEdit,2,3)
			self.layout.addWidget(self.button2,3,1)
			self.layout.addWidget(self.button3,5,1)
			self.layout.addWidget(self.button4,4,1)
			self.button1.clicked.connect(self._restore)
			self.button2.clicked.connect(self._restart)
			self.button3.clicked.connect(self._quit)
			self.button4.clicked.connect(self._flash)
			self._start_process(
            'xterm',
            ['-fa','10','-fg','green','-into', str(self.terminal.winId()),
             '-e', 'tmux', 'new', '-s', 'my_session'])

   def _start_process(self, prog, args):
			child = QProcess()
			self._processes.append(child)
			child.start(prog, args)

   def _restore(self):
			elid_id = self.elidEdit.text()
			self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', '/home/obs/sam/rootfs/tools/./rootfs_restore.sh ' + elid_id, 'Enter'])

   def _restart(self):
			self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', 'a', 'Enter'])
			os.system('killall minicom')
			self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', 'cd /home/obs/sam/rootfs/tools', 'Enter'])
			self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', 'clear', 'Enter'])
   def _quit(self):
			self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', 'a', 'Enter'])
			os.system('killall minicom')
			sys.exit(app.exec_())	
		
   def _flash(self):
			self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', './flash_uboot.sh -p ttyUSB0 u-boot-NAND_ais.bin', 'Enter'])
		
   def tab2UI(self):
      layout = QFormLayout()
      sex = QHBoxLayout()
      sex.addWidget(QRadioButton("Male"))
      sex.addWidget(QRadioButton("Female"))
      layout.addRow(QLabel("Sex"),sex)
      layout.addRow("Date of Birth",QLineEdit())
      self.setTabText(1,"Personal Details")
      self.tab2.setLayout(layout)
		
   def tab3UI(self):
      layout = QHBoxLayout()
      layout.addWidget(QLabel("subjects")) 
      layout.addWidget(QCheckBox("Physics"))
      layout.addWidget(QCheckBox("Maths"))
      self.setTabText(2,"Education Details")
      self.tab3.setLayout(layout)
		
def main():
   app = QApplication(sys.argv)
   ex = tabdemo()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
