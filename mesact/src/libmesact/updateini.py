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

		# finally update the [AXIS_n] and [JOINT_n] sections
		axes = []
		for i in range(6):
			axis = getattr(parent, f'{card}_axisCB_{i}').currentData()
			if axis and axis not in axes:
				axes.append(axis)
				self.update_key(f'AXIS_{axis}', 'MIN_LIMIT', getattr(parent, f'{card}_minLimit_{i}').text())
				self.update_key(f'AXIS_{axis}', 'MAX_LIMIT', getattr(parent, f'{card}_maxLimit_{i}').text())
				self.update_key(f'AXIS_{axis}', 'MAX_VELOCITY', getattr(parent, f'{card}_maxVelocity_{i}').text())
				self.update_key(f'AXIS_{axis}', 'MAX_ACCELERATION', getattr(parent, f'{card}_maxAccel_{i}').text())

			if getattr(parent, f'{card}_axisCB_{i}').currentData():
				self.update_key(f'JOINT_{i}', 'AXIS', getattr(parent, f'{card}_axisCB_{i}').currentData())
				self.update_key(f'JOINT_{i}', 'MIN_LIMIT', getattr(parent, f'{card}_minLimit_{i}').text())
				self.update_key(f'JOINT_{i}', 'MAX_LIMIT', getattr(parent, f'{card}_maxLimit_{i}').text())
				self.update_key(f'JOINT_{i}', 'MAX_VELOCITY', getattr(parent, f'{card}_maxVelocity_{i}').text())
				self.update_key(f'JOINT_{i}', 'MAX_ACCELERATION', getattr(parent, f'{card}_maxAccel_{i}').text())
				self.update_key(f'JOINT_{i}', 'TYPE', getattr(parent, f'{card}_axisType_{i}').text())
				if getattr(parent, f'{card}_reverse_{i}').isChecked():
					self.update_key(f'JOINT_{i}', 'SCALE', f'-{getattr(parent, f"{card}_scale_{i}").text()}')
				else:
					self.update_key(f'JOINT_{i}', 'SCALE', f'{getattr(parent, f"{card}_scale_{i}").text()}')

				if parent.cardType_0 == 'step' or parent.cardType_1 == 'step': # add step and dir invert
					self.update_key(f'JOINT_{i}', 'DRIVE', getattr(parent, f'{card}_driveCB_{i}').currentText())
					self.update_key(f'JOINT_{i}', 'STEP_INVERT', getattr(parent, f'{card}_StepInvert_{i}').isChecked())
					self.update_key(f'JOINT_{i}', 'DIR_INVERT', getattr(parent, f'{card}_DirInvert_{i}').isChecked())
					self.update_key(f'JOINT_{i}', 'STEPGEN_MAX_VEL', f'{float(getattr(parent, f"{card}_maxVelocity_{i}").text()) * 1.2:.2f}')
					self.update_key(f'JOINT_{i}', 'STEPGEN_MAX_ACC', f'{float(getattr(parent, f"{card}_maxAccel_{i}").text()) * 1.2:.2f}')
					self.update_key(f'JOINT_{i}', 'DIRSETUP', getattr(parent, f'{card}_DirSetup_{i}').text())
					self.update_key(f'JOINT_{i}', 'DIRHOLD', getattr(parent, f'{card}_DirHold_{i}').text())
					self.update_key(f'JOINT_{i}', 'STEPLEN', getattr(parent, f'{card}_StepTime_{i}').text())
					self.update_key(f'JOINT_{i}', 'STEPSPACE', getattr(parent, f'{card}_StepSpace_{i}').text())

				if parent.cardType_0 == 'servo' or parent.cardType_1 == 'servo':
					self.update_key(f'JOINT_{i}', 'ENCODER_SCALE', getattr(parent, f'{card}_encoderScale_{i}').text())
					self.update_key(f'JOINT_{i}', 'ANALOG_SCALE_MAX', getattr(parent, f'{card}_analogScaleMax_{i}').text())
					self.update_key(f'JOINT_{i}', 'ANALOG_MIN_LIMIT', getattr(parent, f'{card}_analogMinLimit_{i}').text())
					self.update_key(f'JOINT_{i}', 'ANALOG_MAX_LIMIT', getattr(parent, f'{card}_analogMaxLimit_{i}').text())

				self.update_key(f'JOINT_{i}', 'FERROR', getattr(parent, f'{card}_ferror_{i}').text())
				self.update_key(f'JOINT_{i}', 'MIN_FERROR', getattr(parent, f'{card}_min_ferror_{i}').text())
				self.update_key(f'JOINT_{i}', 'DEADBAND', getattr(parent, f'{card}_deadband_{i}').text())
				self.update_key(f'JOINT_{i}', 'P', getattr(parent, f'{card}_p_{i}').text())
				self.update_key(f'JOINT_{i}', 'I', getattr(parent, f'{card}_i_{i}').text())
				self.update_key(f'JOINT_{i}', 'D', getattr(parent, f'{card}_d_{i}').text())
				self.update_key(f'JOINT_{i}', 'FF0', getattr(parent, f'{card}_ff0_{i}').text())
				self.update_key(f'JOINT_{i}', 'FF1', getattr(parent, f'{card}_ff1_{i}').text())
				self.update_key(f'JOINT_{i}', 'FF2', getattr(parent, f'{card}_ff2_{i}').text())
				self.update_key(f'JOINT_{i}', 'BIAS', getattr(parent, f'{card}_bias_{i}').text())
				self.update_key(f'JOINT_{i}', 'MAX_OUTPUT', getattr(parent, f'{card}_maxOutput_{i}').text())
				self.update_key(f'JOINT_{i}', 'MAX_ERROR', getattr(parent, f'{card}_maxError_{i}').text())
				if getattr(parent, f"{card}_home_" + str(i)).text():
					self.update_key(f'JOINT_{i}', 'HOME', getattr(parent, f"{card}_home_{i}").text())
				if getattr(parent, f"{card}_homeOffset_{i}").text():
					self.update_key(f'JOINT_{i}', 'HOME_OFFSET', getattr(parent, f"{card}_homeOffset_{i}").text())
				if getattr(parent, f"{card}_homeSearchVel_{i}").text():
					self.update_key(f'JOINT_{i}', 'HOME_SEARCH_VEL', getattr(parent, f"{card}_homeSearchVel_{i}").text())
				if getattr(parent, f"{card}_homeLatchVel_{i}").text():
					self.update_key(f'JOINT_{i}', 'HOME_LATCH_VEL', getattr(parent, f"{card}_homeLatchVel_{i}").text())
				if getattr(parent, f"{card}_homeFinalVelocity_{i}").text():
					self.update_key(f'JOINT_{i}', 'HOME_FINAL_VEL', getattr(parent, f"{card}_homeFinalVelocity_{i}").text())
				if getattr(parent, f"{card}_homeSequence_{i}").text():
					self.update_key(f'JOINT_{i}', 'HOME_SEQUENCE', getattr(parent, f"{card}_homeSequence_{i}").text())
				if getattr(parent, f"{card}_homeIgnoreLimits_{i}").isChecked():
					self.update_key(f'JOINT_{i}', 'HOME_IGNORE_LIMITS', True)
				if getattr(parent, f"{card}_homeUseIndex_{i}").isChecked():
					self.update_key(f'JOINT_{i}', 'HOME_USE_INDEX', True)
				if getattr(parent, f"{card}_homeSwitchShared_{i}").isChecked():
					self.update_key(f'JOINT_{i}', 'HOME_IS_SHARED', True)

		# update the [SPINDLE_0] section
		if parent.spindleTypeCB.currentData():
			pass

		'''
		if parent.spindleTypeCB.currentData():
			iniContents.append('\n[SPINDLE]\n')
			iniContents.append(f'SPINDLE_TYPE = {parent.spindleTypeCB.currentData()}\n')
			if parent.spindlePwmTypeCB.currentData():
				iniContents.append(f'SPINDLE_PWM_TYPE = {parent.spindlePwmTypeCB.currentData()}\n')
			if parent.spindleTypeCB.currentData() == 'analog':
				iniContents.append(f'PWM_FREQUENCY = {parent.pwmFrequencySB.value()}\n')
				iniContents.append(f'MAX_RPM = {parent.spindleMaxRpm.value()}\n')
				iniContents.append(f'MIN_RPM = {parent.spindleMinRpm.value()}\n')

			if parent.spindleFeedbackCB.currentData() == 'encoder':
				iniContents.append(f'FEEDBACK = {parent.spindleFeedbackCB.currentData()}\n')
				iniContents.append(f'P = {parent.p_s.value()}\n')
				iniContents.append(f'I = {parent.i_s.value()}\n')
				iniContents.append(f'D = {parent.d_s.value()}\n')
				iniContents.append(f'FF0 = {parent.ff0_s.value()}\n')
				iniContents.append(f'FF1 = {parent.ff1_s.value()}\n')
				iniContents.append(f'FF2 = {parent.ff2_s.value()}\n')
				iniContents.append(f'BIAS = {parent.bias_s.value()}\n')
				iniContents.append(f'DEADBAND = {parent.deadband_s.value()}\n')
				iniContents.append(f'MAX_ERROR = {parent.maxError_s.value()}\n')
				iniContents.append(f'MAX_OUTPUT = {parent.maxOutput_s.value()}\n')
				iniContents.append(f'OUTPUT_TYPE = {parent.maxOutput_s.value()}\n')
				iniContents.append(f'ENCODER_SCALE = {parent.spindleEncoderScale.value()}\n')

			if parent.spindleTypeCB.currentData()[:7] == 'stepgen':
				iniContents.append(f'DRIVE = {parent.spindleDriveCB.currentText()}\n')
				iniContents.append(f'SCALE = {parent.spindleStepScale.text()}\n')
				iniContents.append(f'STEPLEN = {parent.spindleStepTime.text()}\n')
				iniContents.append(f'STEPSPACE = {parent.spindleStepSpace.text()}\n')
				iniContents.append(f'DIRSETUP = {parent.spindleDirSetup.text()}\n')
				iniContents.append(f'DIRHOLD = {parent.spindleDirHold.text()}\n')
				iniContents.append(f'STEP_INVERT = {parent.spindleStepInvert.isChecked()}\n')
				iniContents.append(f'DIR_INVERT = {parent.spindleDirInvert.isChecked()}\n')
				iniContents.append(f'MIN_RPM = {parent.spindleMinRpm.value()}\n')
				iniContents.append(f'MAX_RPM = {parent.spindleMaxRpm.value()}\n')
				iniContents.append(f'MIN_RPS = {parent.spindleMinRps.text()}\n')
				iniContents.append(f'MAX_RPS = {parent.spindleMaxRps.text()}\n')
				iniContents.append(f'MAX_ACCEL_RPM = {parent.spindleMaxAccel.value()}\n')
				iniContents.append(f'MAX_ACCEL_RPS = {parent.spindleMaxRpss.text()}\n')

		'''


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





