import pymel.core as pm
import pymel.core.datatypes as dt

def command():
	pass

def attach_form(lay, control, edge_list=[], offset=0):
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

# Finds the first input for a plug, or returns None.
def get_connection(plug):
	attr = pm.PyNode(plug)
	for i in attr.inputs():
		return i

def prompt_ui():
	win = pm.window(title="Gamma Correct Attribute", width=200)
	
	layout = pm.formLayout(parent=win)
	
	shader_options = pm.optionMenu(label="Shader")
	
	attribute_options = pm.optionMenu(label="Attribute")
	
	ok_button = pm.button(label="Insert", enable=False)
	
	attach_form(layout, shader_options, ["top", "left", "right"], 5)

	attach_form(layout, attribute_options, ["left", "right"], 5)
	layout.attachControl(attribute_options, "top", 5, shader_options)

	gamma_slider = pm.floatSlider(min=0.1, max=3.0, step=0.1, value=2.2)
	gamma_lbl = pm.text(label="2.2")

	attach_form(layout, gamma_slider, ["top", "left"], 5) 
	layout.attachControl(gamma_slider, "top", 5, attribute_options)
	layout.attachControl(gamma_slider, "right", 5, gamma_lbl)

	attach_form(layout, gamma_lbl, ["right"], 5)
	layout.attachControl(gamma_lbl, "top", 5, attribute_options)

	info_lbl = pm.text(label="Select a node...")

	attach_form(layout, info_lbl, ["left", "right"], 5)
	layout.attachControl(info_lbl, "top", 5, gamma_slider)

	attach_form(layout, ok_button, ["bottom", "left", "right"], 5)
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
		command()
		win.delete()

	ok_button.setCommand(_on_insert)

	_refresh()
	win.show()

prompt_ui()