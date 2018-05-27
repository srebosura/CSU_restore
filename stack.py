import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class stackedExample(QWidget):

   def __init__(self):
		super(stackedExample, self).__init__()
		self.leftw = QWidget(self)
		self.rightw = QWidget(self)
		#self.tab1 = QWidget()
		#self.tab2 = QWidget()	
		self.leftw_UI()
		self.rightw_UI()
		hbox = QHBoxLayout(self)
		#hbox.addWidget(self.leftw)
		#hbox.addWidget(self.rightw)
		hbox.addLayout(self.layout)
		hbox.addLayout(self.layout2)
		
		self.setLayout(hbox)
		self.leftw_UI()
		self.rightw_UI()
		#self.setGeometry(100, 100, 1024,768)
		self.setWindowTitle('CSU Tools')
		
		self.show()
		
   def leftw_UI(self):
		self.layout = QGridLayout(self)
		#self.move(20, 20)		
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
		
   def rightw_UI(self):
		self.layout2 = QGridLayout(self)
		self._processes = []
		self.resize(800, 600)
		self.terminal = QWidget(self)
		self.layout2.addWidget(self.terminal, 4,4)
		self._start_process(
            'xterm',
            ['-fa','10','-fg','green','-into', str(self.terminal.winId()),
             '-e', 'tmux', 'new', '-s', 'my_session'])
		
		
   def _start_process(self, prog, args):
			child = QProcess()
			self._processes.append(child)
			child.start(prog, args)

def main():
		app = QApplication(sys.argv)
		ex = stackedExample()
		sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
