# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2014, Ravi Sharma
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Feb 12, 2014

@author: Ravi Sharma
'''

from lxml import etree

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError


class TroubleshooterStep(KayakoObject):
	'''
	Troubleshooter Step API Object.

	id                      The unique numeric identifier of the step.
	categoryid              The unique numeric identifier of the category.
	subject                 The step subject.
	contents                The step contents.
	staffid                 The staff ID.
	displayorder            The display order.
	allowcomments           Allow comments. 0 or 1.
	enableticketredirection Enable ticket redirection.
	redirectdepartmentid    The redirect department ID.
	tickettypeid            The ticket type ID.
	ticketpriorityid        The ticket priority ID.
	ticketsubject           The ticket subject.
	stepstatus              The step status. Published: 1, Draft: 2
	parentstepidlist        Parent steps. multiple values comma separated like 1,2,3.
	'''

	controller = '/Troubleshooter/Step'

	__parameters__ = ['id', 'categoryid', 'staffid', 'staffname', 'subject', 'edited', 'editedstaffid', 'editedstaffname', 'displayorder', 'allowcomments', 'hasattachments',
	                  'attachments', 'parentsteps', 'childsteps', 'redirecttickets', 'ticketsubject', 'redirectdepartmentid', 'tickettypeid', 'priorityid', 'contents', 'enableticketredirection',
	                  'ticketpriorityid', 'stepstatus', 'parentstepidlist']

	__required_add_parameters__ = ['categoryid', 'subject', 'contents', 'staffid']
	__add_parameters__ = ['categoryid', 'subject', 'contents', 'staffid', 'displayorder', 'allowcomments', 'enableticketredirection', 'redirectdepartmentid', 'tickettypeid', 'ticketpriorityid',
	                      'ticketsubject', 'stepstatus', 'parentstepidlist']

	__required_save_parameters__ = ['categoryid', 'subject', 'contents', 'staffid']
	__save_parameters__ = ['categoryid', 'subject', 'contents', 'staffid', 'displayorder', 'allowcomments', 'enableticketredirection', 'redirectdepartmentid', 'tickettypeid', 'ticketpriorityid',
	                       'ticketsubject', 'stepstatus', 'parentstepidlist']

	@classmethod
	def _parse_troubleshooter_step(cls, api, troubleshooter_step_tree):

		attachmentlist = []
		attachmentlist_node = troubleshooter_step_tree.find('attachments')
		if attachmentlist_node is not None:
			for id_node in attachmentlist_node.findall('attachment'):
				id = cls._get_int(id_node)
				attachmentlist.append(id)

		parentsteplist = []
		parentsteplist_node = troubleshooter_step_tree.find('staffgroupidlist')
		if parentsteplist_node is not None:
			for id_node in parentsteplist_node.findall('staffgroupidlist'):
				id = cls._get_int(id_node)
				parentsteplist.append(id)

		childsteplist = []
		childsteplist_node = troubleshooter_step_tree.find('staffgroupidlist')
		if childsteplist_node is not None:
			for id_node in childsteplist_node.findall('staffgroupidlist'):
				id = cls._get_int(id_node)
				childsteplist.append(id)

		params = dict(
			id=cls._get_int(troubleshooter_step_tree.find('id')),
			categoryid=cls._get_int(troubleshooter_step_tree.find('categoryid')),
			staffid=cls._get_int(troubleshooter_step_tree.find('staffid')),
			staffname=cls._get_string(troubleshooter_step_tree.find('staffname')),
			subject=cls._get_string(troubleshooter_step_tree.find('subject')),
			edited=cls._get_boolean(troubleshooter_step_tree.find('edited')),
			editedstaffid=cls._get_int(troubleshooter_step_tree.find('editedstaffid')),
			displayorder=cls._get_int(troubleshooter_step_tree.find('displayorder')),
			allowcomments=cls._get_int(troubleshooter_step_tree.find('allowcomments')),
			hasattachments=cls._get_boolean(troubleshooter_step_tree.find('hasattachments')),
			attachments=attachmentlist,
			parentsteps=parentsteplist,
			childsteps=childsteplist,
			redirecttickets=cls._get_boolean(troubleshooter_step_tree.find('redirecttickets')),
			ticketsubject=cls._get_string(troubleshooter_step_tree.find('ticketsubject')),
			redirectdepartmentid=cls._get_boolean(troubleshooter_step_tree.find('redirectdepartmentid')),
			tickettypeid=cls._get_int(troubleshooter_step_tree.find('tickettypeid')),
			priorityid=cls._get_int(troubleshooter_step_tree.find('priorityid')),
			contents=cls._get_string(troubleshooter_step_tree.find('contents')),
		)
		return params

	def _update_from_response(self, troubleshooter_step_tree):

		for int_node in ['id', 'categoryid', 'staffid', 'editedstaffid', 'displayorder', 'allowcomments', 'tickettypeid', 'priorityid']:
			node = troubleshooter_step_tree.find(int_node)
			if node is not None:
				setattr(self, int_node, self._get_int(node, required=False))

		for str_node in ['staffname', 'subject', 'ticketsubject', 'redirectdepartmentid', 'contents']:
			node = troubleshooter_step_tree.find(str_node)
			if node is not None:
				setattr(self, str_node, self._get_string(node))

		for bool_node in ['edited', 'hasattachments', 'redirecttickets', 'redirectdepartmentid']:
			node = troubleshooter_step_tree.find(bool_node)
			if node is not None:
				setattr(self, bool_node, self._get_boolean(node, required=False))

	@classmethod
	def get_all(cls, api):
		response = api._request('%s/' % (cls.controller), 'GET')
		tree = etree.parse(response)
		return [TroubleshooterStep(api, **cls._parse_troubleshooter_step(api, troubleshooter_step_tree)) for troubleshooter_step_tree in tree.findall('troubleshooterstep')]

	@classmethod
	def get(cls, api, id):
		response = api._request('%s/%s/' % (cls.controller, id), 'GET')
		tree = etree.parse(response)
		node = tree.find('troubleshooterstep')
		if node is None:
			return None
		params = cls._parse_troubleshooter_step(api, node)
		return TroubleshooterStep(api, **params)

	def add(self):
		'''
		Add this TroubleshooterStep.
			displayorder            The display order.
			allowcomments           Allow comments. 0 or 1.
			enableticketredirection Enable ticket redirection.
			redirectdepartmentid    The redirect department ID.
			tickettypeid            The ticket type ID.
			ticketpriorityid        The ticket priority ID.
			ticketsubject           The ticket subject.
			stepstatus              The step status. Published: 1, Draft: 2
			parentstepidlist        Parent steps. multiple values comma separated like 1,2,3.

		Requires:
			id                      The unique numeric identifier of the step.
			categoryid              The unique numeric identifier of the category.
			subject                 The step subject.
			contents                The step contents.
			staffid                 The staff ID.
		'''
		parameters = self.add_parameters

		for required_parameter in self.__required_add_parameters__:
			if required_parameter not in parameters:
				raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))

		response = self.api._request(self.controller, 'POST', **parameters)
		tree = etree.parse(response)
		node = tree.find('troubleshooterstep')
		self._update_from_response(node)

	def save(self):
		response = self._save('%s/%s/' % (self.controller, self.id))
		tree = etree.parse(response)
		node = tree.find('troubleshooterstep')
		self._update_from_response(node)

	def delete(self):
		self._delete('%s/%s/' % (self.controller, self.id))

	def __str__(self):
		return '<TroubleshooterStep (%s): %s>' % (self.id, self.subject)