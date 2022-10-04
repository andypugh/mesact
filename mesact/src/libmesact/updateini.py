import os
from datetime import datetime

class updateini:
	def __init__(self):
		super().__init__()
		self.sections = {}
		self.iniFile = ''

	def update(self, parent, iniFile):
		self.iniFile = iniFile
		with open(self.iniFile,'r') as file:
			self.content = file.readlines()
		self.get_sections()
		if self.content[0].startswith('# This file'):
			self.content[0] = ('# This file was updated with the Mesa Configuration'
				f'Tool on {datetime.now().strftime("%b %d %Y %H:%M:%S")}\n')

		mesa = [
		['MESA', 'VERSION', f'{parent.version}'],
		['MESA', 'BOARD', f'{parent.boardCB.currentData()}'],
		['MESA', 'FIRMWARE', f'{parent.firmwareCB.currentText()}'],
		['MESA', 'CARD_0', f'{parent.daughterCB_0.currentData()}'],
		['MESA', 'CARD_1', f'{parent.daughterCB_1.currentData()}']
		]
		for item in mesa:
			self.update_key(item[0], item[1], item[2])

		emc = [
		['EMC', 'VERSION', f'{parent.emcVersion}'],
		['EMC', 'MACHINE', f'{parent.configName.text()}'],
		['EMC', 'DEBUG', f'{parent.debugCB.currentData()}']
		]
		for item in emc:
			self.update_key(item[0], item[1], item[2])

		if parent.boardType == 'eth':
			hm2 = [
			['HM2',  'DRIVER', f'hm2_eth'],
			['HM2',  'IPADDRESS', f'{parent.ipAddressCB.currentText()}']
			]
		else:
			self.delete_key('HM2', 'IPADDRESS')
		if parent.boardType == 'pci':
			hm2 = ['HM2',  'DRIVER', 'hm2_pci']
		hm2.append(['HM2',  'STEPGENS', f'{parent.stepgensCB.currentData()}'])
		hm2.append(['HM2',  'PWMGENS', f'{parent.pwmgensCB.currentData()}'])
		hm2.append(['HM2',  'ENCODERS', f'{parent.encodersCB.currentData()}'])
		for item in hm2:
			self.update_key(item[0], item[1], item[2])

		display = [
		['DISPLAY', 'DISPLAY', f'{parent.guiCB.itemData(parent.guiCB.currentIndex())}'],
		['DISPLAY', 'PROGRAM_PREFIX', f'{os.path.expanduser("~/linuxcnc/nc_files")}'],
		['DISPLAY', 'POSITION_OFFSET', f'{parent.positionOffsetCB.currentData()}'],
		['DISPLAY', 'POSITION_FEEDBACK', f'{parent.positionFeedbackCB.currentData()}'],
		['DISPLAY', 'MAX_FEED_OVERRIDE', f'{parent.maxFeedOverrideSB.value()}'],
		['DISPLAY', 'CYCLE_TIME', '0.1'],
		['DISPLAY', 'INTRO_GRAPHIC', f'{parent.introGraphicLE.text()}'],
		['DISPLAY', 'INTRO_TIME', f'{parent.splashScreenSB.value()}'],
		['DISPLAY', 'OPEN_FILE', f'""']
		]
		if parent.editorCB.currentData():
			display.append(['DISPLAY', 'EDITOR', f'{parent.editorCB.currentData()}'])
		else:
			self.delete_key('DISPLAY', 'EDITOR')
		if set('XYZUVW')&set(parent.coordinatesLB.text()):
			display.append(['DISPLAY', 'MIN_LINEAR_VELOCITY', f'{parent.minLinJogVelDSB.value()}'])
			display.append(['DISPLAY', 'DEFAULT_LINEAR_VELOCITY', f'{parent.defLinJogVelDSB.value()}'])
			display.append(['DISPLAY', 'MAX_LINEAR_VELOCITY', f'{parent.maxLinJogVelDSB.value()}'])
		else:
			self.delete_key('DISPLAY', 'MIN_LINEAR_VELOCITY')
			self.delete_key('DISPLAY', 'DEFAULT_LINEAR_VELOCITY')
			self.delete_key('DISPLAY', 'MAX_LINEAR_VELOCITY')
		if set('ABC')&set(parent.coordinatesLB.text()):
			display.append(['DISPLAY', 'MIN_ANGULAR_VELOCITY', f'{parent.minAngJogVelDSB.value()}'])
			display.append(['DISPLAY', 'DEFAULT_ANGULAR_VELOCITY', f'{parent.defAngJogVelDSB.value()}'])
			display.append(['DISPLAY', 'MAX_ANGULAR_VELOCITY', f'{parent.maxAngJogVelDSB.value()}'])
		else:
			self.delete_key('DISPLAY', 'MIN_ANGULAR_VELOCITY')
			self.delete_key('DISPLAY', 'DEFAULT_ANGULAR_VELOCITY')
			self.delete_key('DISPLAY', 'MAX_ANGULAR_VELOCITY')
		if parent.pyvcpCB.isChecked():
			display.append(['DISPLAY', 'PYVCP', f'{parent.configNameUnderscored}.xml'])
		else:
			self.delete_key('DISPLAY', 'PYVCP')
		if parent.frontToolLatheCB.isChecked():
			display.append(['DISPLAY', 'LATHE', '1'])
		else:
			self.delete_key('DISPLAY', 'LATHE')
		if parent.frontToolLatheCB.isChecked():
			display.append(['DISPLAY', 'BACK_TOOL_LATHE', '1'])
		else:
			self.delete_key('DISPLAY', 'BACK_TOOL_LATHE')
		for item in display:
			self.update_key(item[0], item[1], item[2])

		if len(set(parent.coordinatesLB.text())) == len(parent.coordinatesLB.text()): # 1 joint for each axis
			kins = [['KINS', 'KINEMATICS', f'trivkins coordinates={parent.coordinatesLB.text()}']]
		else: # more than one joint per axis
			kins = [['KINS', 'KINEMATICS', f'trivkins coordinates={parent.coordinatesLB.text()} kinstype=BOTH']]
		kins.append(['KINS', 'JOINTS', f'{len(parent.coordinatesLB.text())}'])
		for item in kins:
			self.update_key(item[0], item[1], item[2])

		emcio = [
		['EMCIO', 'EMCIO', 'iov2'],
		['EMCIO', 'CYCLE_TIME', '0.100'],
		['EMCIO', 'TOOL_TABLE', 'tool.tbl']
		]
		for item in emcio:
			self.update_key(item[0], item[1], item[2])

		rs274ngc = [
		['RS274NGC', 'PARAMETER_FILE', f'{parent.configNameUnderscored}.var'],
		['RS274NGC', 'SUBROUTINE_PATH', f'{os.path.expanduser("~/linuxcnc/subroutines")}']
		]

		for item in rs274ngc:
			self.update_key(item[0], item[1], item[2])

		emcmot = [
		['EMCMOT', 'EMCMOT', 'motmod'],
		['EMCMOT', 'COMM_TIMEOUT', '1.0'],
		['EMCMOT', 'SERVO_PERIOD', f'{parent.servoPeriodSB.value()}']
		]

		for item in emcmot:
			self.update_key(item[0], item[1], item[2])

		task = [
		['TASK', 'TASK', 'milltask'],
		['TASK', 'CYCLE_TIME', '0.010']
		]

		for item in task:
			self.update_key(item[0], item[1], item[2])

		traj = [
		['TRAJ', 'COORDINATES', f'{parent.coordinatesLB.text()}'],
		['TRAJ', 'LINEAR_UNITS', f'{parent.linearUnitsCB.currentData()}'],
		['TRAJ', 'ANGULAR_UNITS', 'degree'],
		['TRAJ', 'MAX_LINEAR_VELOCITY', f'{parent.trajMaxLinVelDSB.value()}'],
		]
		if parent.noforcehomingCB.isChecked():
			traj.append(['TRAJ','NO_FORCE_HOMING', '0'])
		else:
			traj.append(['TRAJ','NO_FORCE_HOMING', '1'])

		for item in traj:
			self.update_key(item[0], item[1], item[2])

		hal = [
		['HAL', 'HALFILE', f'filelist.hal'],
		]
		if parent.postguiCB.isChecked():
			hal.append('HAL', 'POSTGUI_HALFILE', 'postgui.hal')
		if parent.shutdownCB.isChecked():
			hal.append('HAL', 'SHUTDOWN', 'shutdown.hal')

		hal.append(['HAL', 'HALUI', 'halui'])

		for item in hal:
			self.update_key(item[0], item[1], item[2])

		# [AXIS_]

		if parent.cardTabs.isTabEnabled(0):
			card = 'c0'
		elif parent.cardTabs.isTabEnabled(1):
			card = 'c1'

		# see if all axis sections exist
		axes = ['X', 'Y', 'Z', 'A', 'B', 'C', 'U', 'V', 'W']
		for i in range(6):
			if getattr(parent, f'{card}_axisCB_{i}').currentData():
				axis_letter = f'{getattr(parent, f"{card}_axisCB_{i}").currentData()}'
				axis_section = f'[AXIS_{axis_letter}]'
				if axis_section in self.sections.keys():
					if axis_letter in axes:
						axes.remove(axis_letter)
					print(f'Section: {axis_section} [JOINT_{i}] exists')
				else:
					print(f'Section: {axis_section} missing')

		for axis in axes:
			if f'[AXIS_{axis}]' in self.sections.keys():
				print(f'[AXIS_{axis}] needs to be removed')
				self.remove_section(f'[AXIS_{axis}]')
			#else:
			#	print(f'[AXIS_{axis}] not in ini file')


		#print(axes)

		'''
		axes = []
		for i in range(6):
			if getattr(parent, f'{card}_axisCB_{i}').currentData():
				axes.append([getattr(parent, f'{card}_axisCB_{i}').currentData(), i])

		#print(axes)
		#print(set(parent.coordinatesLB.text()))


		# build the axes
		axes = []
		axis_n = []
		for i in range(6):
			axis = getattr(parent, f'{card}_axisCB_{i}').currentData()
			if axis and axis not in axes:
				axes.append(axis)

		axis_n = [
		['', '', f''],
		]

		for item in axis_:
			self.update_key(item[0], item[1], item[2])




				#jointTab = getattr(parent, f'{card}_axisCB_{i}')
				iniContents.append(f'\n[AXIS_{axis}]\n')
				#print(getattr(parent, f'{card}_minLimit_{i}').text())

				iniContents.append(f'MIN_LIMIT = {getattr(parent, f"{card}_minLimit_{i}").text()}\n')
				iniContents.append(f'MAX_LIMIT = {getattr(parent, f"{card}_maxLimit_{i}").text()}\n')
				iniContents.append(f'MAX_VELOCITY = {getattr(parent, f"{card}_maxVelocity_{i}").text()}\n')
				iniContents.append(f'MAX_ACCELERATION = {getattr(parent, f"{card}_maxAccel_{i}").text()}\n')


		display = [
		['', '', f''],
		]

		for item in traj:
			self.update_key(item[0], item[1], item[2])

		iniContents.append('HALUI = halui\n')

		# build the [HALUI] section
		iniContents.append('\n[HALUI]\n')
		'''
		# TESTING
		iniFile = '/home/john/linuxcnc/configs/7i96s/test.ini'
		with open(self.iniFile, 'w') as outfile:
			outfile.write(''.join(self.content))

		parent.machinePTE.appendPlainText(f'{os.path.basename(iniFile)} Updated')

	def get_sections(self):
		for index, line in enumerate(self.content):
			if line.strip().startswith('['):
				self.sections[line.strip()] = [index, 0]

		# set start and stop index for each section
		previous = ''
		for key, value in self.sections.items():
			if previous:
				self.sections[previous][1] = value[0] - 2
			previous = key
		#print(self.sections)

	def update_key(self, section, key, value):
		start = self.sections[f'[{section}]'][0]
		end = self.sections[f'[{section}]'][1]
		found = False
		for item in self.content[start:end]:
			if item.startswith(key):
				index = self.content.index(item)
				self.content[index] = f'{key} = {value}\n'
				found = True
		if not found:
			self.content.insert(end, f'{key} = {value}\n')
			self.get_sections() # update section start/end

	def delete_key(self, section, key):
		start = self.sections[f'[{section}]'][0]
		end = self.sections[f'[{section}]'][1]
		for item in self.content[start:end]:
			if item.startswith(key):
				index = self.content.index(item)
				del self.content[index]
				self.get_sections() # update section start/end

	def add_section(self):
		pass

	def remove_section(self, section):
		print(f'Removing {section}')
		print(self.sections[section])




