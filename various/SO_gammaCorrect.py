# Copyright (c) 2012, Simon Otter
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SIMON OTTER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import pymel.core as pm
import pymel.core.datatypes as dt

SRGB=2.2

def correct(plug, gamma=SRGB):
	"""Corrects plug for gamma. Note that the gamma entered
	is the one to correct for, so the actual value is 1/SRGB,
	the inverse of the gamma parameter.

	plug must point to a float3 attribute. If the plug is already
	connected, this command will insert the node as an intermediary.
	"""
	
	attr = pm.PyNode(plug)
	node = attr.plugNode()

	# Make sure it's not zero or something stupid.
	gammaVal = 1 / float(gamma)

	if not attr:
		raise ValueError("No %s attribute found on %s." % (attr, node))

	if attr.type() != "float3":
		raise ValueError("%s does not point to a float3 attribute." % plug)

	gcNode = pm.createNode("gammaCorrect")
	gcNode.gamma.set([gammaVal] * 3)

	firstInput = get_connection(plug)
	if firstInput:
		print(firstInput)
		firstInput >> gcNode.value
		gcNode.outValue >> attr
	else:
		value = attr.get()
		gcNode.value.set(value)

		gcNode.outValue >> attr


def _attach_form(lay, control, edge_list=[], offset=0):
	for e in edge_list:
		lay.attachForm(control, e, offset)

# List all the materials in the scene.
def list_materials():
	return pm.ls(mat=True)

# typ = "*" returns all attributes, regardless of type.
def list_attributes(node, typ="*"):
	results = []

	for a in pm.listAttr(node, w=True, c=True):
		try:
			a_type = pm.getAttr("%s.%s" % (node, a), type=True)
			if a_type == typ or typ == "*":
				results.append(a)
		except Exception, e:
			# Swallow this error, it is thrown by Maya for some plugs.
			pass

	return results


def get_connection(plug):
	"""Finds the first input for a plug, or returns None."""

	attr = pm.PyNode(plug)
	for i in attr.inputs(p=True):
		return i

def prompt_ui():
	"""Displays the Gamma Correction UI."""

	win = pm.window(title="Gamma Correct Attribute", width=200)
	
	layout = pm.formLayout(parent=win)
	
	shader_options = pm.optionMenu(label="Shader")
	
	attribute_options = pm.optionMenu(label="Attribute")
	
	ok_button = pm.button(label="Insert", enable=False)
	
	_attach_form(layout, shader_options, ["top", "left", "right"], 5)

	_attach_form(layout, attribute_options, ["left", "right"], 5)
	layout.attachControl(attribute_options, "top", 5, shader_options)

	gamma_slider = pm.floatSlider(min=0.1, max=3.0, step=0.1, value=2.2)
	gamma_lbl = pm.text(label="2.2")

	_attach_form(layout, gamma_slider, ["top", "left"], 5) 
	layout.attachControl(gamma_slider, "top", 5, attribute_options)
	layout.attachControl(gamma_slider, "right", 5, gamma_lbl)

	_attach_form(layout, gamma_lbl, ["right"], 5)
	layout.attachControl(gamma_lbl, "top", 5, attribute_options)

	info_lbl = pm.text(label="Select a node...")

	_attach_form(layout, info_lbl, ["left", "right"], 5)
	layout.attachControl(info_lbl, "top", 5, gamma_slider)

	_attach_form(layout, ok_button, ["bottom", "left", "right"], 5)
	layout.attachControl(ok_button, "top", 5, info_lbl)

	# CALLBACKS.

	def _refresh():		
		shader_options.clear()
		for m in list_materials():
			pm.uitypes.MenuItem(label=m, p=shader_options)

	def _on_shader_changed(*args):
		if len(args) == 0:
			return

		ok_button.setEnable(True)

		attribute_options.clear()
		# Select all "color" attributes.
		for a in list_attributes(args[0], typ="float3"):
			pm.uitypes.MenuItem(label=a, p=attribute_options)

	shader_options.changeCommand(_on_shader_changed)

	def _on_attribute_changed(*args):
		node = shader_options.getValue()

		info_lbl.setLabel("%s's input is: %s" % (args[0], get_connection(node + "." + args[0])))

	attribute_options.changeCommand(_on_attribute_changed)

	def _gamma_on_change(*args):
		gamma_lbl.setLabel("%.2f" % gamma_slider.getValue())

	gamma_slider.dragCommand(_gamma_on_change)

	def _on_insert(*args):
		correct("%s.%s" % (shader_options.getValue(), attribute_options.getValue()), gamma=gamma_slider.getValue())
		win.delete()

	ok_button.setCommand(_on_insert)

	_refresh()
	win.show()

prompt_ui()