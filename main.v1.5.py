#!/usr/bin/env python
#-*- coding:utf-8 -*-
## Need to install tmux utility to run the app
## Sam 09.05.18

import sys
import os
import io
import time
import subprocess
import serial
from cStringIO import StringIO
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
		self.terminal.resize(800,800)
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
		self.button8 = QPushButton('Calibrate Batt')
		self.button9 = QPushButton('Help')
		self.button10 = QPushButton('Get Info')
		self.button11 = QPushButton('')
		
		self.label_style1 = ("background-color: #605e5e; color: #39ff14;")
		self.label_style2 = ("background-color: #c4c545; color: white;")
		
		self.elid = QLabel("ELID   ")
		self.elid.setFont(QFont("Arial",16))
		self.elid.setStyleSheet(self.label_style2)
		self.elidEdit = QLineEdit()
		self.elidEdit.setFont(QFont("Arial",14))
		self.elidEdit.setStyleSheet(self.label_style1)
		self.housing = QLabel("HOUSING No")
		self.housing.setFont(QFont("Arial",16))
		self.housing.setStyleSheet(self.label_style2)
		self.housingEdit = QLineEdit()
		self.housingEdit.setFont(QFont("Arial",14))
		self.housingEdit.setStyleSheet(self.label_style1)
		self.elidEdit.setMaxLength(4)
		self.housingEdit.setMaxLength(4)
		
		self.tty_port = QLabel("CommPort")
		self.tty_port.setFont(QFont("Arial",14))
		self.tty_port.setStyleSheet(self.label_style2)
		self.tty_portEdit = QLineEdit()
		self.tty_portEdit.setFont(QFont("Arial",12))
		self.tty_portEdit.setStyleSheet(self.label_style1)
		self.tty_portEdit.setMaxLength(7)
		
		self.csac_status = QLabel("CSAC Status")
		self.csac_status.setFont(QFont("Arial",16))
		self.csac_status.setStyleSheet(self.label_style2)
		self.csac_statusEdit = QLineEdit()
		self.csac_statusEdit.setFont(QFont("Arial",14))
		self.csac_statusEdit.setStyleSheet(self.label_style1)
		self.csac_heatp = QLabel("HeatP")
		self.csac_heatp.setFont(QFont("Arial",16))
		self.csac_heatp.setStyleSheet(self.label_style2)
		self.csac_heatpEdit = QLineEdit()
		self.csac_heatpEdit.setFont(QFont("Arial",14))
		self.csac_heatpEdit.setStyleSheet(self.label_style1)
		self.csac_contrast = QLabel("Contrast")
		self.csac_contrast.setFont(QFont("Arial",16))
		self.csac_contrast.setStyleSheet(self.label_style2)
		self.csac_contrastEdit = QLineEdit()
		self.csac_contrastEdit.setFont(QFont("Arial",14))
		self.csac_contrastEdit.setStyleSheet(self.label_style1)
		self.csac_serial = QLabel("Serial #")
		self.csac_serial.setFont(QFont("Arial",16))
		self.csac_serial.setStyleSheet(self.label_style2)
		self.csac_serialEdit = QLineEdit()
		self.csac_serialEdit.setFont(QFont("Arial",14))
		self.csac_serialEdit.setStyleSheet(self.label_style1)
		
		self.bat1 = QLabel("Vbat1")
		self.bat1.setFont(QFont("Arial",16))
		self.bat1.setStyleSheet(self.label_style2)
		self.bat1Edit = QLineEdit()
		self.bat1Edit.setFont(QFont("Arial",14))
		self.bat1Edit.setStyleSheet(self.label_style1)
		self.bat2 = QLabel("Vbat2")
		self.bat2.setFont(QFont("Arial",16))
		self.bat2.setStyleSheet(self.label_style2)
		self.bat2Edit = QLineEdit()
		self.bat2Edit.setFont(QFont("Arial",14))
		self.bat2Edit.setStyleSheet(self.label_style1)
		self.batv = QLabel("Vbat")
		self.batv.setFont(QFont("Arial",16))
		self.batv.setStyleSheet(self.label_style2)
		self.batvEdit = QLineEdit()
		self.batvEdit.setFont(QFont("Arial",14))
		self.batvEdit.setStyleSheet(self.label_style1)
		self.ibat = QLabel("Ibat")
		self.ibat.setFont(QFont("Arial",16))
		self.ibat.setStyleSheet(self.label_style2)
		self.ibatEdit = QLineEdit()
		self.ibatEdit.setFont(QFont("Arial",14))
		self.ibatEdit.setStyleSheet(self.label_style1)
		self.bsel = QLabel("BatSel")
		self.bsel.setFont(QFont("Arial",16))
		self.bsel.setStyleSheet(self.label_style2)
		self.bselEdit = QLineEdit()
		self.bselEdit.setFont(QFont("Arial",14))
		self.bselEdit.setStyleSheet(self.label_style1)
		
		##layout
		self.elayout = QHBoxLayout()
		self.vlayout = QVBoxLayout()
		self.flayout = QHBoxLayout()
		self.tlayout = QHBoxLayout()
		self.clayout = QHBoxLayout()
		self.blayout = QHBoxLayout()
		self.button_style1 = ("background-color:#00b2ff; color: white;")
		self.button_style2 = ("background-color:#3c84b0; color: white;")
		#self.button_style3 = ("background-color:#cc1800; color: white;")
		self.button_style3 = ("background-color:#af473c; color: white;")
		
		self.elayout.addWidget(self.elid)
		self.elayout.addWidget(self.elidEdit)
		self.elayout.addWidget(self.button1)
		self.button1.setStyleSheet(self.button_style1)
		self.elayout.addWidget(self.housing)
		self.elayout.addWidget(self.housingEdit)
		self.elayout.addWidget(self.button5)
		self.button5.setStyleSheet(self.button_style1)
		self.elayout.addWidget(self.tty_port)
		self.elayout.addWidget(self.tty_portEdit)
		
		self.flayout.addWidget(self.button3)
		self.button3.setStyleSheet(self.button_style2)
		self.flayout.addWidget(self.button6)
		self.button6.setStyleSheet(self.button_style2)		
		self.flayout.addWidget(self.button7)
		self.button7.setStyleSheet(self.button_style2)
		self.flayout.addWidget(self.button10)
		self.button10.setStyleSheet(self.button_style2)
		
		self.tlayout.addWidget(self.button2)
		self.button2.setStyleSheet(self.button_style2)
		self.tlayout.addWidget(self.button8)
		self.button8.setStyleSheet(self.button_style2)
		self.tlayout.addWidget(self.button9)
		self.button9.setStyleSheet(self.button_style2)
		self.tlayout.addWidget(self.button11)
		self.button11.setStyleSheet(self.button_style2)
		
		self.clayout.addWidget(self.csac_status)
		self.clayout.addWidget(self.csac_statusEdit)
		self.clayout.addWidget(self.csac_heatp)
		self.clayout.addWidget(self.csac_heatpEdit)
		self.clayout.addWidget(self.csac_contrast)
		self.clayout.addWidget(self.csac_contrastEdit)
		self.clayout.addWidget(self.csac_serial)
		self.clayout.addWidget(self.csac_serialEdit)
		
		self.blayout.addWidget(self.bat1)
		self.blayout.addWidget(self.bat1Edit)
		self.blayout.addWidget(self.bat2)
		self.blayout.addWidget(self.bat2Edit)
		self.blayout.addWidget(self.batv)
		self.blayout.addWidget(self.batvEdit)
		self.blayout.addWidget(self.ibat)
		self.blayout.addWidget(self.ibatEdit)
		self.blayout.addWidget(self.bsel)
		self.blayout.addWidget(self.bselEdit)
		
		self.vlayout.addLayout(self.hlayout)
		self.vlayout.addLayout(self.elayout)
			
		self.vlayout.addLayout(self.flayout)	
		self.vlayout.addLayout(self.tlayout)
		self.vlayout.addLayout(self.clayout)
		self.vlayout.addLayout(self.blayout)
		
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
		self.button8.clicked.connect(self._batt_calib)
		self.button9.clicked.connect(self._showdialog)
		self.button10.clicked.connect(self._read_info)
		self.button11.clicked.connect(self._aboutme)
		self._find_active_tty()
		
		self._start_process(
            'xterm',
            ['-fa','-12','-s','-fg','green','-into', str(self.terminal.winId()),
             '-e', 'tmux', 'new', '-s', 'my_session'])

    def _start_process(self, prog, args):
		child = QProcess()
		self._processes.append(child)
		child.start(prog, args)

    def _restore(self):
		self.elid_id = self.elidEdit.text()
		self.tty_read = self.tty_portEdit.text()
		
		print self.elid_id
		self.cmd0 = '/home/obs/sam/rootfs/tools/./rootfs_restore.sh /dev/%s %s'% (self.tty_read,self.elid_id)
		self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', self.cmd0, 'Enter'])

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
		self.csac_statusEdit.clear()
		self.csac_serialEdit.clear()
		self.csac_contrastEdit.clear()
		self.csac_heatpEdit.clear()
		self.bat1Edit.clear()
		self.bat2Edit.clear()
		self.batvEdit.clear()
		self.ibatEdit.clear()
		self.bselEdit.clear()
		
			
    def _quit(self):
		self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', 'a', 'Enter'])
		os.system('killall minicom')
		sys.exit(app.exec_())	
		
    def _flash(self):
		self.tty_read = self.tty_portEdit.text()
		self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', './flash_uboot.sh -p %s u-boot-NAND_ais.bin'%(self.tty_read), 'Enter'])

    def _get_serial(self):
		self.tty= self.tty_portEdit.text()
		tty = "/dev/%s"%(self.tty)
		ser = serial.Serial(tty,9600)
		ser.write("(console)")
		ser.close()
		time.sleep(2)
		self._start_process(
			'tmux', ['send-keys', '-t', 'my_session:0', 'minicom -D '+ tty, 'Enter'])
			
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
		msg1 = QLabel("(*) Enter CSU ELID number, hit Restore RFS button then boot or apply power to the CSU.")
		msg1.setFont(QFont("Arial",12))
		msg2 = QLabel("(*) Watch the restore process on the terminal, Press Y when ask to reboot CSU in terminal.")
		msg2.setFont(QFont("Arial",12))
		msg3 = QLabel("(*) After the reboot, the CSU might be in modem mode, click Start Serial Comm button to connect.")
		msg3.setFont(QFont("Arial",12))
		msg4 = QLabel("(*) Enter Housing number, click Set Housing.....Restore done!")
		msg4.setFont(QFont("Arial",12))
		msg5 = QLabel(".................... Battery Calibration ....................")
		msg5.setFont(QFont("Arial",12))
		msg6 = QLabel("(*) Default Input(Reference/Power Supply Voltage) is set to 25V ")
		msg6.setFont(QFont("Arial",12))
		msg7 = QLabel("(*) Click Auto Calibrate button until you reach the acceptable battery reading.")
		msg7.setFont(QFont("Arial",12))
		msg8 = QLabel("(*) You can also enter and trim/adjust the calibration gains (Recommended)....")
		msg8.setFont(QFont("Arial",12))
		self.dlayout.addWidget(msg1)
		self.dlayout.addWidget(msg2)
		self.dlayout.addWidget(msg3)
		self.dlayout.addWidget(msg4)
		self.dlayout.addWidget(msg5)
		self.dlayout.addWidget(msg6)
		self.dlayout.addWidget(msg7)
		self.dlayout.addWidget(msg8)
		
		b1 = QPushButton("ok",d)
		self.dlayout.addWidget(b1)
		b1.move(620,80)
		d.setLayout(self.dlayout)
		d.setWindowTitle("Help")
		d.setWindowModality(Qt.ApplicationModal)
		b1.clicked.connect(d.close)
		d.exec_()
		
    def _batt_calib(self):
		b=QDialog()
		
		actualV1 = QLabel("Actual Voltage Input B1")
		actualV1.setFont(QFont("Arial",12))
		actualV1Edit = QLineEdit()
		actualV1Edit.setFont(QFont("Arial",12))
		actualV1Edit.setStyleSheet(self.label_style1)
		vbat1 = QLabel("Voltage Reading B1")
		vbat1.setFont(QFont("Arial",12))
		vbat1Edit = QLineEdit()
		vbat1Edit.setFont(QFont("Arial",12))
		vbat1Edit.setStyleSheet(self.label_style1)
		vgain1 = QLabel("Calibration B1")
		vgain1.setFont(QFont("Arial",12))
		vgain1Edit = QLineEdit()
		vgain1Edit.setFont(QFont("Arial",12))
		vgain1Edit.setStyleSheet(self.label_style1)
		actualV2 = QLabel("Actual Voltage Input B2")
		actualV2.setFont(QFont("Arial",12))
		actualV2Edit = QLineEdit()
		actualV2Edit.setFont(QFont("Arial",12))
		actualV2Edit.setStyleSheet(self.label_style1)
		vbat2 = QLabel("Voltage Reading B2")
		vbat2.setFont(QFont("Arial",12))
		vbat2Edit = QLineEdit()
		vbat2Edit.setFont(QFont("Arial",12))
		vbat2Edit.setStyleSheet(self.label_style1)
		vgain2 = QLabel("Calibration B2")
		vgain2.setFont(QFont("Arial",12))
		vgain2Edit = QLineEdit()
		vgain2Edit.setFont(QFont("Arial",12))
		vgain2Edit.setStyleSheet(self.label_style1)
		
		vbat = QLabel("Parallel Voltage Vbat")
		vbat.setFont(QFont("Arial",12))
		vbatEdit = QLineEdit()
		vbatEdit.setFont(QFont("Arial",12))
		vbatEdit.setStyleSheet(self.label_style1)
		batsel = QLabel("Current Battery")
		batsel.setFont(QFont("Arial",12))
		batselEdit = QLineEdit()
		batselEdit.setFont(QFont("Arial",12))
		batselEdit.setStyleSheet(self.label_style1)
		
		self.bhlayout = QHBoxLayout()
		self.blayout = QVBoxLayout()
		self.h1layout = QHBoxLayout()
		self.h2layout = QHBoxLayout()
		self.h3layout = QHBoxLayout()
		self.h4layout = QHBoxLayout()
		self.h5layout = QHBoxLayout()
		self.h6layout = QHBoxLayout()
		self.h7layout = QHBoxLayout()
		self.h8layout = QHBoxLayout()
		
		self.h1layout.addWidget(actualV1)
		self.h1layout.addWidget(actualV1Edit)
		self.h2layout.addWidget(vbat1)
		self.h2layout.addWidget(vbat1Edit)
		self.h3layout.addWidget(vgain1)
		self.h3layout.addWidget(vgain1Edit)
		
		self.h4layout.addWidget(actualV2)
		self.h4layout.addWidget(actualV2Edit)
		self.h5layout.addWidget(vbat2)
		self.h5layout.addWidget(vbat2Edit)
		self.h6layout.addWidget(vgain2)
		self.h6layout.addWidget(vgain2Edit)
		
		self.h7layout.addWidget(vbat)
		self.h7layout.addWidget(vbatEdit)
		self.h8layout.addWidget(batsel)
		self.h8layout.addWidget(batselEdit)
		
		self.blayout.addLayout(self.bhlayout)
		self.blayout.addLayout(self.h1layout)
		self.blayout.addLayout(self.h2layout)
		self.blayout.addLayout(self.h3layout)
		self.blayout.addLayout(self.h4layout)
		self.blayout.addLayout(self.h5layout)
		self.blayout.addLayout(self.h6layout)
		self.blayout.addLayout(self.h7layout)
		self.blayout.addLayout(self.h8layout)
		
		b1 = QPushButton("Refresh")
		b2 = QPushButton("Auto Calibrate B1")
		b3 = QPushButton("Manual/Trim B1")
		b4 = QPushButton("Auto Calibrate B2")
		b5 = QPushButton("Manual/Trim B2")
		b6 = QPushButton("Batt Select")
		
		self.h1layout.addWidget(b2)
		self.h3layout.addWidget(b3)
		self.h5layout.addWidget(b4)
		self.h6layout.addWidget(b5)
		self.h8layout.addWidget(b6)
		self.h8layout.addWidget(b1)
		
		
		
		b.setLayout(self.blayout)
		os.system('killall minicom')
		
		
		def read_battery():
			self.vbat1_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat1" 10 |tail -2 |head -1'%(self.tty))[1].read()
			self.vbat2_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat2" 10 |tail -2 |head -1'%(self.tty))[1].read()
			self.vgain1_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat1_s" 10 |tail -2 |head -1'%(self.tty))[1].read()
			self.vgain2_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat2_s" 10 |tail -2 |head -1'%(self.tty))[1].read()
			self.vbat_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat" 10 |tail -2 |head -1'%(self.tty))[1].read()
			self.batsel_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g batsel" 10 |tail -2 |head -1'%(self.tty))[1].read()
		
		
			b1 = self.vbat1_r.split("=")[1]
			vbat1Edit.setText(b1.split("V")[0])
			b2 = self.vbat2_r.split("=")[1]
			vbat2Edit.setText(b2.split("V")[0])
			vgain1Edit.setText(self.vgain1_r.split("=")[1])
			vgain2Edit.setText(self.vgain2_r.split("=")[1])
			vb = self.vbat_r.split("=")[1]
			vbatEdit.setText(vb.split("V")[0])
			batselEdit.setText(self.batsel_r.split("=")[1])
			
		def calibrate_b1():
			self.vbat1_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat1" 10 |tail -2 |head -1'%(self.tty))[1].read()
			vbat1Edit.setText(self.vbat1_r.split("=")[1])
			time.sleep(1)
			self.vgain1_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat1_s" 10 |tail -2 |head -1'%(self.tty))[1].read()
			vgain1Edit.setText(self.vgain1_r.split("=")[1])
			vin1 = (actualV1Edit.text())
			vbat1r = (vbat1Edit.text())
			vgain1r = (vgain1Edit.text())
			
			vin1 = float(vin1.split("V")[0])
			vbat1r = float(vbat1r.split("V")[0])
			vgain1r = float(vgain1r.split("V")[0])
			
			calib_gain1 = round((((vin1)/(vbat1r)-1)*1024)) + vgain1r
			calib_gain1 = str(calib_gain1)
			vgain1Edit.setText(calib_gain1.split(".")[0])
			
			cmd1 = ['python', 'exec_cmd.py','/dev/'+ self.tty, 'csu_pwrctrl', '-s', 'vbat1_s:'+ calib_gain1.split(".")[0], '10']
			print cmd1
			os.popen4(cmd1)
			time.sleep(3)
			self.vbat1_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat1" 10 |tail -2 |head -1'%(self.tty))[1].read()
			b1 = self.vbat1_r.split("=")[1]
			vbat1Edit.setText(b1.split("V")[0])
					
		def calibrate_b2():
			self.vbat2_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat2" 10 |tail -2 |head -1'%(self.tty))[1].read()
			vbat2Edit.setText(self.vbat2_r.split("=")[1])
			time.sleep(1)
			self.vgain2_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat2_s" 10 |tail -2 |head -1'%(self.tty))[1].read()
			vgain2Edit.setText(self.vgain2_r.split("=")[1])
			vin2 = (actualV2Edit.text())
			vbat2r = (vbat2Edit.text())
			vgain2r = (vgain2Edit.text())
			
			vin2 = float(vin2.split("V")[0])
			vbat2r = float(vbat2r.split("V")[0])
			vgain2r = float(vgain2r.split("V")[0])
			
			calib_gain2 = round((((vin2)/(vbat2r)-1)*1024)) + vgain2r
			calib_gain2 = str(calib_gain2)
			vgain2Edit.setText(calib_gain2.split(".")[0])
			
			cmd1 = ['python', 'exec_cmd.py','/dev/'+ self.tty, 'csu_pwrctrl', '-s', 'vbat2_s:'+ calib_gain2.split(".")[0], '10']
			os.popen4(cmd1)
			time.sleep(3)
			self.vbat2_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat2" 10 |tail -2 |head -1'%(self.tty))[1].read()
			b2 = self.vbat2_r.split("=")[1]
			vbat2Edit.setText(b2.split("V")[0])
			
		def trim_b1():
			calib_gain = vgain1Edit.text()
			cmd = ['python', 'exec_cmd.py','/dev/'+ self.tty, 'csu_pwrctrl', '-s', 'vbat1_s:'+ calib_gain.split(".")[0], '10']
			os.popen4(cmd)
			time.sleep(3)
			self.vbat1_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat1" 10 |tail -2 |head -1'%(self.tty))[1].read()
			b1 = self.vbat1_r.split("=")[1]
			vbat1Edit.setText(b1.split("V")[0])
			
		def trim_b2():
			calib_gain = vgain2Edit.text()
			cmd = ['python', 'exec_cmd.py','/dev/'+ self.tty, 'csu_pwrctrl', '-s', 'vbat2_s:'+ calib_gain.split(".")[0], '10']
			os.popen4(cmd)
			time.sleep(3)
			self.vbat2_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat2" 10 |tail -2 |head -1'%(self.tty))[1].read()
			b2 = self.vbat2_r.split("=")[1]
			vbat2Edit.setText(b2.split("V")[0])
			
		def bat_sel():
			batt_s = batselEdit.text()
			cmd = ['python', 'exec_cmd.py','/dev/'+ self.tty, 'csu_pwrctrl', '-s', 'batsel:'+ batt_s, '10']
			os.popen4(cmd)
			time.sleep(2)
			self.batsel_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g batsel" 10 |tail -2 |head -1'%(self.tty))[1].read()
			batselEdit.setText(self.batsel_r.split("=")[1])
		
		actualV1Edit.setText("25")
		actualV2Edit.setText("25")
		self.tty= self.tty_portEdit.text()
		
		read_battery()	
		b1.clicked.connect(read_battery)
		b2.clicked.connect(calibrate_b1)
		b3.clicked.connect(trim_b1)
		b4.clicked.connect(calibrate_b2)
		b5.clicked.connect(trim_b2)
		b6.clicked.connect(bat_sel)
		
		b.setWindowTitle("Battery Calibration")
		b.setWindowModality(Qt.ApplicationModal)
		b.exec_()
		
    def _aboutme(self):
		d = QDialog()
		self.dlayout = QVBoxLayout()
		msg1 = QLabel("CSU Restore Application v1.4")
		msg1.setFont(QFont("Arial",12))
		msg2 = QLabel("Build from : ")
		msg2.setFont(QFont("Arial",12))
		msg3 = QLabel("Python 2.7.3, PyQt4, Tmux")
		msg3.setFont(QFont("Arial",12))
		msg4 = QLabel("Not an Official Software release by Seabed, exclusive for CSU restoration only!")
		msg4.setFont(QFont("Arial",12))
		msg5 = QLabel("by rebosura_sd@yahoo.com.ph 15.05.18")
		msg5.setFont(QFont("Arial",12))
		self.dlayout.addWidget(msg1)
		self.dlayout.addWidget(msg2)
		self.dlayout.addWidget(msg3)
		self.dlayout.addWidget(msg4)
		self.dlayout.addWidget(msg5)
		
		b1 = QPushButton("ok",d)
		self.dlayout.addWidget(b1)
		b1.move(620,80)
		d.setLayout(self.dlayout)
		d.setWindowTitle("About Me")
		d.setWindowModality(Qt.ApplicationModal)
		b1.clicked.connect(d.close)
		d.exec_()
		
    def _read_info(self):
		os.system('killall minicom')
		time.sleep(2)
		self.tty= self.tty_portEdit.text()
		tty = "/dev/%s"%(self.tty)
		ser = serial.Serial(tty,9600)
		ser.write("(console)")
		ser.close()
		time.sleep(2)
		self.elid_r = os.popen4('python exec_cmd.py /dev/%s "cat /data/etc/ELID" 10 |tail -2 |head -1'%(self.tty))[1].read()
		self.elidEdit.setText(self.elid_r)
		self.housing_r = os.popen4('python exec_cmd.py /dev/%s "cat /data/etc/HOUSING" 10 |tail -2 |head -1'%(self.tty))[1].read()
		self.housingEdit.setText(self.housing_r)
		
		self.vbat1_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat1" 10 |tail -2 |head -1'%(self.tty))[1].read()
		self.vbat2_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat2" 10 |tail -2 |head -1'%(self.tty))[1].read()	
		self.imain_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g imain" 10 |tail -2 |head -1'%(self.tty))[1].read()
		self.vbat_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g vbat" 10 |tail -2 |head -1'%(self.tty))[1].read()
		self.batsel_r = os.popen4('python exec_cmd.py /dev/%s "csu_pwrctrl -g batsel" 10 |tail -2 |head -1'%(self.tty))[1].read()
		
		self.bat1Edit.setText(self.vbat1_r.split("=")[1])
		self.bat2Edit.setText(self.vbat2_r.split("=")[1])
		self.batvEdit.setText(self.vbat_r.split("=")[1])
		self.ibatEdit.setText(self.imain_r.split("=")[1])
		self.bselEdit.setText(self.batsel_r.split("=")[1])
		time.sleep(3)
		
		self.csac_r = os.popen4('python exec_cmd.py /dev/%s "sq_disciplining --telemetry" 10 >/tmp/csu.tmp'%(self.tty))[1].read()
		status_r = os.popen4('head -2 /tmp/csu.tmp | tail -1')[1].read()
		self.csac_statusEdit.setText(status_r.split(":	")[1])
		status_r = os.popen4('head -4 /tmp/csu.tmp | tail -1')[1].read()
		self.csac_serialEdit.setText(status_r.split(":	")[1])
		status_r = os.popen4('head -6 /tmp/csu.tmp | tail -1')[1].read()
		self.csac_contrastEdit.setText(status_r.split(":")[1])
		status_r = os.popen4('head -9 /tmp/csu.tmp | tail -1')[1].read()
		self.csac_heatpEdit.setText(status_r.split(":	")[1])
		
    def _find_active_tty(self):
		#os.system('ls /sys/class/tty/ |grep USB')
		self.tty = os.popen4('ls /sys/class/tty/ |grep USB |tail -1')[1].read()
		self.tty_portEdit.setText(self.tty)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = embeddedTerminal()
    main.setWindowTitle("CSU Restore v1.5                                                           Case Abyss 3                                                            SeaBed GeoSolutions")
    #main.setStyleSheet("background-color:#d7de73;")
    main.setStyleSheet("background-color:#c4c545;")
    main.setWindowIcon(QIcon('ca3.png'))
    os.system("killall tmux")
    #os.system("sudo rm /var/lib/dhcp/dhcpd.leases;sudo service isc-dhcp-server restart;rm /home/obs/.ssh/known_hosts")
    main.show()
    sys.exit(app.exec_())
