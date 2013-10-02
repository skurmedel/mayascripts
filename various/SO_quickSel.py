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

"""
If in MEL:

	python("import SO_quickSel");
	python("SO_quickSel.show_ui()");

In Python:

	import SO_quickSel
	SO_quickSel.show_ui()

"""

import pymel.core as pm

DEFAULT_SET_NAME 	= "QuickSelSet"
DEFAULT_SET 		= None

def default():
	global DEFAULT_SET
	global DEFAULT_SET_NAME

	if DEFAULT_SET is None:
		if pm.objExists(DEFAULT_SET_NAME):
			tmp = pm.PyNode(DEFAULT_SET_NAME)
			if tmp.nodeType() != "objectSet":
				raise ValueError(
					"Found object named %s but expected it to be of type objectSet." % (DEFAULT_SET_NAME,))
			DEFAULT_SET = tmp
		else:
			DEFAULT_SET = pm.sets(n=DEFAULT_SET_NAME)

	return DEFAULT_SET

def show_ui():

	curr_set = default()

	def clear_cb(*args):
		if pm.confirmBox("Clear Selection Set", "Are you sure?"):
			curr_set.clear()
		print("Cleared QuickSel.")

	def add_cb(*args):
		for i in pm.selected():
			curr_set.add(i)

	def remove_cb(*args):
		try:
			for i in pm.selected():
				curr_set.remove(i)
		except ValueError:
			# Thrown when trying to remove items not in the set.
			# Well, we don't care.
			pass

	def select_cb(*args):
		pm.select(curr_set.members())

	win = pm.window(t="QuickSel UI")
	win.setHeight(32)

	lay = pm.formLayout()

	clear_button = pm.button(label="Clear", c=clear_cb)
	add_button = pm.button(label="Add", c=add_cb)
	remove_button = pm.button(label="Remove", c=remove_cb)
	sel_button = pm.button(label="Select", c=select_cb)

	def attach_top_bottom(c):
		lay.attachForm(c, "top", 5)
		lay.attachForm(c, "bottom", 5)

	lay.attachForm(clear_button, "left", 5)
	attach_top_bottom(clear_button)

	attach_top_bottom(add_button)
	lay.attachControl(add_button, "left", 5, clear_button)

	attach_top_bottom(remove_button)
	lay.attachControl(remove_button, "left", 5, add_button)

	attach_top_bottom(sel_button)
	lay.attachControl(sel_button, "left", 5, remove_button)
	lay.attachForm(sel_button, "right", 5)

	win.show()
