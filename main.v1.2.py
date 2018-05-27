#!/usr/bin/env python
#-*- coding:utf-8 -*-
## Need to install tmux utility to run the app
## Sam 09.05.18

import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class embeddedTerminal(QWidget):

    def __init__(self, parent=None):
		super(embeddedTerminal, self).__init__(parent)
		self._processes = []		
		self.hlayout = QHBoxLayout()
		pixmap = QPixmap('sbgs_logo.png')
		logo = QLabel(self)
		logo.setPixmap(pixmap)
		self.hlayout.addWidget(logo)
		logo.setMaximumWidth(150)
		self.terminal = QWidget(self)
		#self.terminal.resize(800,800)
		self.hlayout.addWidget(self.terminal)
		#logo.resize(800,800)
		##labels
		self.button1 = QPushButton('Restore RFS')
		self.button1.setFont(QFont("Arial",14))
		self.button2 = QPushButton('Restart')
		self.button3 = QPushButton('Flash U-Boot')
		self.button4 = QPushButton('Exit')
		self.button5 = QPushButton('Set Housing')
		self.button5.setFont(QFont("Arial",14))
		self.button6 = QPushButton('Start Serial Comm')
		self.button7 = QPushButton('Taptest')
		self.button8 = QPushButton()
		self.button9 = QPushButton('Help')
		self.button10 = QPushButton()
		
		
		self.elid = QLabel("ELID   ")
		self.elid.setFont(QFont("Arial",16))
		self.elidEdit = QLineEdit()
		self.elidEdit.setFont(QFont("Arial",14))
		self.housing = QLabel("HOUSING NO")
		self.housing.setFont(QFont("Arial",16))
		self.separator = QLabel("                        ")
		self.housingEdit = QLineEdit()
		self.housingEdit.setFont(QFont("Arial",14))
		self.elidEdit.setMaxLength(4)
		self.housingEdit.setMaxLength(4)
		##layout
		self.elayout = QHBoxLayout()
		self.vlayout = QVBoxLayout()
		self.flayout = QHBoxLayout()
		self.tlayout = QHBoxLayout()
		self.button_style1 = ("background-color:#00b2ff; color: white;")
		self.button_style2 = ("background-color:#3c84b0; color: white;")
		self.button_style3 = ("background-color:#cc1800; color: white;")
		
		self.elayout.addWidget(self.elid)
		self.elayout.addWidget(self.elidEdit)
		self.elayout.addWidget(self.button1)
		self.button1.setStyleSheet(self.button_style1)
		self.elayout.addWidget(self.separator)
		self.elayout.addWidget(self.housing)
		self.elayout.addWidget(self.housingEdit)
		self.elayout.addWidget(self.button5)
		self.button5.setStyleSheet(self.button_style1)
		
		self.flayout.addWidget(self.button3)
		self.button3.setStyleSheet(self.button_style2)
		self.flayout.addWidget(self.button6)
		self.button6.setStyleSheet(self.button_style2)		
		self.flayout.addWidget(self.button7)
		self.button7.setStyleSheet(self.button_style2)
		
		self.tlayout.addWidget(self.button2)
		self.button2.setStyleSheet(self.button_style2)
		self.tlayout.addWidget(self.button8)
		self.button8.setStyleSheet(self.button_style2)
		self.tlayout.addWidget(self.button9)
		self.button9.setStyleSheet(self.button_style2)
		
		self.vlayout.addLayout(self.hlayout)
		self.vlayout.addLayout(self.elayout)
			
		self.vlayout.addLayout(self.flayout)	
		self.vlayout.addLayout(self.tlayout)	
		
		self.vlayout.addWidget(self.button4)
		self.button4.setStyleSheet(self.button_style3)
		
		self.setLayout(self.vlayout)
		self.setGeometry( 20, 20, 985, 600)
		##signals
		self.button1.clicked.connect(self._restore)
		self.button2.clicked.connect(self._restart)
		self.button3.clicked.connect(self._flash)
		self.button4.clicked.connect(self._quit)
		self.button5.clicked.connect(self._set_housing)	
		self.button6.clicked.connect(self._get_serial)
		self.button7.clicked.connect(self._taptest)
		self.button8.clicked.connect(self._aboutme)
		self.button9.clicked.connect(self._showdialog)
		self._start_process(
            'xterm',
            ['-fa','-12','-s','-fg','green','-into', str(self.terminal.winId()),
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
		self.housingEdit.clear()
		self.elidEdit.clear()
			
    def _quit(self):
		self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', 'a', 'Enter'])
		os.system('killall minicom')
		sys.exit(app.exec_())	
		
    def _flash(self):
		self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', './flash_uboot.sh -p ttyUSB0 u-boot-NAND_ais.bin', 'Enter'])

    def _get_serial(self):
		self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', '/home/obs/sam/rootfs/tools/./get_serial.sh', 'Enter'])
			
    def _set_housing(self):
		housing_id = self.housingEdit.text()
		self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', 'sq_set_housing ' + housing_id, 'Enter'])

    def _taptest(self):
    	self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', '/home/obs/sam/rootfs/tools/scripts/taptest/./taptest.sh', 'Enter'])
	
    def _showdialog(self):
		d = QDialog()
		self.dlayout = QVBoxLayout()
		msg1 = QLabel("(1) Enter CSU ELID number, hit Restore RFS button then boot or apply power to the CSU.")
		msg1.setFont(QFont("Arial",12))
		msg2 = QLabel("(2) Watch the restore process on the terminal, Press Y when ask to reboot CSU in terminal.")
		msg2.setFont(QFont("Arial",12))
		msg3 = QLabel("(3) After the reboot, the CSU might be in modem mode, click Start Serial Comm button to connect.")
		msg3.setFont(QFont("Arial",12))
		msg4 = QLabel("(4) Enter Housing number, click Set Housing.....Restore done!")
		msg4.setFont(QFont("Arial",12))
		self.dlayout.addWidget(msg1)
		self.dlayout.addWidget(msg2)
		self.dlayout.addWidget(msg3)
		self.dlayout.addWidget(msg4)
		
		b1 = QPushButton("ok",d)
		self.dlayout.addWidget(b1)
		b1.move(620,80)
		d.setLayout(self.dlayout)
		d.setWindowTitle("Help")
		d.setWindowModality(Qt.ApplicationModal)
		b1.clicked.connect(d.close)
		d.exec_()
		
    def _aboutme(self):
		d = QDialog()
		self.dlayout = QVBoxLayout()
		msg1 = QLabel("CSU Restore Application v1.2")
		msg1.setFont(QFont("Arial",12))
		msg2 = QLabel("Build from : ")
		msg2.setFont(QFont("Arial",12))
		msg3 = QLabel("Python 2.7.3, PyQt4, Tmux")
		msg3.setFont(QFont("Arial",12))
		msg4 = QLabel("by SR 15.05.18")
		msg4.setFont(QFont("Arial",12))
		self.dlayout.addWidget(msg1)
		self.dlayout.addWidget(msg2)
		self.dlayout.addWidget(msg3)
		self.dlayout.addWidget(msg4)
		
		b1 = QPushButton("ok",d)
		self.dlayout.addWidget(b1)
		b1.move(620,80)
		d.setLayout(self.dlayout)
		d.setWindowTitle("About Me")
		d.setWindowModality(Qt.ApplicationModal)
		b1.clicked.connect(d.close)
		d.exec_()
   	
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = embeddedTerminal()
    main.setWindowTitle("CSU Restore v1.2                                                           Case Abyss 3                                                            SeaBed GeoSolutions")
    main.setStyleSheet("background-color:#d7de73;")
    main.setStyleSheet("background-color:#c4c545;")
    main.setWindowIcon(QIcon('ca3.png'))
    os.system("killall tmux")
    #os.system("sudo rm /var/lib/dhcp/dhcpd.leases;sudo service isc-dhcp-server restart;rm /home/obs/.ssh/known_hosts")
    main.show()
    sys.exit(app.exec_())
