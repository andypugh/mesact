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

		# check for axis letter changed
		axis_list = []
		for i in range(6):
			if getattr(parent, f'{card}_axisCB_{i}').currentData():
				axis_letter = f'{getattr(parent, f"{card}_axisCB_{i}").currentData()}'
				axis_section = f'[AXIS_{axis_letter}]'
				if f'[AXIS_{axis_letter}]' not in axis_list:
					axis_list.append(axis_section)
		#print(len(axis_list))
		#print(axis_list)

		axis_keys = []
		for key in self.sections.keys():
			if key.startswith('[AXIS_'):
				axis_keys.append(key)
		#print(len(axis_keys))
		#print(axis_keys)

		for i in range(len(axis_list)):
			if axis_list[i] != axis_keys[i]:
				print(f'Replace {axis_keys[i]} with {axis_list[i]}')
				index = self.content.index(f'{axis_keys[i]}\n')
				if index:
					self.content[index] = f'{axis_list[i]}\n'
					self.get_sections()

		# check for joint removed
		current_joint_list = []
		for i in range(6):
			if getattr(parent, f'{card}_axisCB_{i}').currentData():
				current_joint_list.append(f'[JOINT_{i}]')

		last_joint_list = []
		for key in self.sections.keys():
			if key.startswith('[JOINT'):
				last_joint_list.append(key)

		if current_joint_list != last_joint_list:
			config_joints = []
			# get list of joints in config
			for key in self.sections.keys():
				if key.startswith('[JOINT'):
					config_joints.append(key)
			# remove joints not configured
			for i in range(len(config_joints)):
				if not getattr(parent, f"{card}_axisCB_{i}").currentData():
					print(f'Remove {config_joints[i]}')
					self.remove_section(config_joints[i])

		# check for axis removed
		last_axis_list = []
		for key in self.sections.keys():
			if key.startswith('[AXIS'):
				last_axis_list.append(key)
		#print(f'last {last_axis_list}')
		current_axis_list = []
		for i in range(6):
			axis = getattr(parent, f"{card}_axisCB_{i}").currentData()
			if axis:
				current_axis_list.append(f'[AXIS_{axis}]')
		#print(f'current {current_axis_list}')
		for axis in last_axis_list:
			if axis not in current_axis_list:
				print(f'Remove {axis}')
				self.remove_section(axis)

		# finally update the [AXIS_n] sections
		axes = []
		for i in range(6):
			axis = getattr(parent, f'{card}_axisCB_{i}').currentData()
			if axis and axis not in axes:
				axes.append(axis)
				self.update_key(f'AXIS_{axis}', f'MIN_LIMIT', getattr(parent, f'{card}_minLimit_{i}').text())
				self.update_key(f'AXIS_{axis}', f'MAX_LIMIT', getattr(parent, f'{card}_maxLimit_{i}').text())
				self.update_key(f'AXIS_{axis}', f'MAX_VELOCITY', getattr(parent, f'{card}_maxVelocity_{i}').text())
				self.update_key(f'AXIS_{axis}', f'MAX_ACCELERATION', getattr(parent, f'{card}_maxAccel_{i}').text())

		# update the [SPINDLE_0] section
		if parent.spindleTypeCB.currentData():
			pass

		# update the inputs section
		for i in range(32):
			self.update_key('INPUTS', f'INPUT_{i}', getattr(parent, "inputPB_" + str(i)).text())
			self.update_key('INPUTS', f'INPUT_INVERT_{i}', getattr(parent, "inputInvertCB_" + str(i)).isChecked())
			self.update_key('INPUTS', f'INPUT_SLOW_{i}', getattr(parent, "inputDebounceCB_" + str(i)).isChecked())

		# update the outputs section
		for i in range(16):
			self.update_key('OUTPUTS', f'OUTPUT_{i}', getattr(parent, "outputPB_" + str(i)).text())
			self.update_key('OUTPUTS', f'OUTPUT_INVERT_{i}', getattr(parent, "outputInvertCB_" + str(i)).isChecked())

		# update the options section
		options = [
		['OPTIONS', 'LOAD_CONFIG', f'{parent.loadConfigCB.isChecked()}'],
		['OPTIONS', 'INTRO_GRAPHIC', f'{parent.introGraphicLE.text()}'],
		['OPTIONS', 'INTRO_GRAPHIC_TIME', f'{parent.splashScreenSB.value()}'],
		['OPTIONS', 'MANUAL_TOOL_CHANGE', f'{parent.manualToolChangeCB.isChecked()}'],
		['OPTIONS', 'CUSTOM_HAL', f'{parent.customhalCB.isChecked()}'],
		['OPTIONS', 'POST_GUI_HAL', f'{parent.postguiCB.isChecked()}'],
		['OPTIONS', 'SHUTDOWN_HAL', f'{parent.shutdownCB.isChecked()}'],
		['OPTIONS', 'HALUI', f'{parent.haluiCB.isChecked()}'],
		['OPTIONS', 'PYVCP', f'{parent.pyvcpCB.isChecked()}'],
		['OPTIONS', 'GLADEVCP', f'{parent.gladevcpCB.isChecked()}'],
		['OPTIONS', 'LADDER', f'{parent.ladderGB.isChecked()}'],
		['OPTIONS', 'BACKUP', f'{parent.backupCB.isChecked()}']
		]
		for item in options:
			self.update_key(item[0], item[1], item[2])

		# update ladder options
		if parent.ladderGB.isChecked(): # check for any options
			for option in parent.ladderOptionsList:
				#print('PLC', f'{getattr(parent, option).property("item")}', f'{getattr(parent, option).value()}')
				self.update_key('PLC', f'{getattr(parent, option).property("item")}', f'{getattr(parent, option).value()}')



		'''

		task = [
		['TASK', 'TASK', 'milltask'],
		]

		self.update_key(section, key, value)

		for item in task:
			self.update_key(item[0], item[1], item[2])

		'''
		# TESTING
		self.iniFile = '/home/john/linuxcnc/configs/7i96s/test.ini'
		with open(self.iniFile, 'w') as outfile:
			outfile.write(''.join(self.content))

		parent.machinePTE.appendPlainText(f'{os.path.basename(self.iniFile)} Updated')

	def get_sections(self):
		end = len(self.content)
		for index, line in enumerate(self.content):
			if line.strip().startswith('['):
				self.sections[line.strip()] = [index, end]

		# set start and stop index for each section
		previous = ''
		for key, value in self.sections.items():
			if previous:
				self.sections[previous][1] = value[0] - 1
			previous = key
		#print(self.sections)

	def update_key(self, section, key, value):
		start = self.sections[f'[{section}]'][0]
		end = self.sections[f'[{section}]'][1]
		#if section == 'PLC':
		#	print(start, end)
		#	print(section, key, value)
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

	def replace_section(self, section):
		print(section)

	def add_section(self, section):
		axis = section[-2]
		print(f'Adding {axis} section')
		for i in range(6):
			if section in self.sections.keys():
				pass
			#if getattr(parent, f'{card}_axisCB_{i}').currentData() == axis:


	def remove_section(self, section):
		start = self.sections[section][0]
		end = self.sections[section][1]
		del self.content[start:end]





