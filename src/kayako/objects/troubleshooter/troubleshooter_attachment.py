# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2014, Ravi Sharma
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Feb 14, 2014

@author: Ravi Sharma
'''

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError
from lxml import etree
import base64


class TroubleshooterAttachment(KayakoObject):
	'''
	Kayako TroubleshooterAttachment API Object.

	troubleshooterstepid        The unique numeric identifier of the step.
	filename                    The file name for the attachment
	contents                    The BASE64 encoded attachment contents
	filesize                    The uploaded file size.
	filetype                    The uploaded file type.
	dateline                    The dateline.
	'''

	controller = '/Troubleshooter/Attachment'

	__parameters__ = [
		'id',
		'troubleshooterstepid',
		'filename',
		'filesize',
		'filetype',
		'contents',
		'dateline',
	]

	__required_add_parameters__ = ['troubleshooterstepid', 'filename', 'contents']
	__add_parameters__ = ['troubleshooterstepid', 'filename', 'contents']

	@classmethod
	def _parse_troubleshooter_attachment(cls, troubleshooter_attachment_tree):

		params = dict(
			id=cls._get_int(troubleshooter_attachment_tree.find('id')),
			troubleshooterstepid=cls._get_int(troubleshooter_attachment_tree.find('troubleshooterstepid')),
			filename=cls._get_string(troubleshooter_attachment_tree.find('filename')),
			filesize=cls._get_int(troubleshooter_attachment_tree.find('filesize')),
			filetype=cls._get_string(troubleshooter_attachment_tree.find('filetype')),
			contents=cls._get_string(troubleshooter_attachment_tree.find('contents')),
			dateline=cls._get_date(troubleshooter_attachment_tree.find('dateline')),
		)
		return params

	def _update_from_response(self, troubleshooter_attachment_tree):
		for int_node in ['id', 'troubleshooterstepid', 'filesize']:
			node = troubleshooter_attachment_tree.find(int_node)
			if node is not None:
				setattr(self, int_node, self._get_int(node, required=False))

		for str_node in ['filename', 'filetype', 'contents']:
			node = troubleshooter_attachment_tree.find(str_node)
			if node is not None:
				setattr(self, str_node, self._get_string(node))

		for date_node in ['dateline']:
			node = troubleshooter_attachment_tree.find(date_node)
			if node is not None:
				setattr(self, date_node, self._get_date(node, required=False))

	@classmethod
	def get_all(cls, api, troubleshooterstepid):
		'''
		Get all of the TroubleshooterAttachments for a step.
		Required:
			troubleshooterstepid	    The troubleshooter step ID.
		'''
		response = api._request('%s/ListAll/%s' % (cls.controller, troubleshooterstepid), 'GET')
		tree = etree.parse(response)
		return [TroubleshooterAttachment(api, **cls._parse_troubleshooter_attachment(troubleshooter_attachment_tree)) for troubleshooter_attachment_tree in tree.findall('troubleshooterattachment')]

	@classmethod
	def get(cls, api, troubleshooterstepid, attachmentid):
		try:
			response = api._request('%s/%s/%s/' % (cls.controller, troubleshooterstepid, attachmentid), 'GET')
		except KayakoResponseError, error:
			if 'HTTP Error 404' in str(error):
				return None
			else:
				raise
		tree = etree.parse(response)
		node = tree.find('troubleshooterattachment')
		if node is None:
			return None
		params = cls._parse_troubleshooter_attachment(node)
		return TroubleshooterAttachment(api, **params)

	def add(self):
		'''
		Add this TroubleshooterAttachment.

		Requires:
			troubleshooterstepid	    The troubleshooter step ID.
			filename	                The uploaded file name.
			contents	                The BASE64 encoded attachment contents
		'''
		response = self._add(self.controller)
		tree = etree.parse(response)
		node = tree.find('troubleshooterattachment')
		self._update_from_response(node)

	def delete(self):
		if self.troubleshooterstepid is None or self.troubleshooterstepid is UnsetParameter:
			raise KayakoRequestError('Cannot delete a TroubleshooterAttachment without being attached to a step. The ID of the Step (troubleshooterstepid) has not been specified.')
		self._delete('%s/%s/%s/' % (self.controller, self.troubleshooterstepid, self.id))

	def get_contents(self):
		''' Return the unencoded contents of this TroubleshooterAttachment. '''
		if self.contents:
			return base64.b64decode(self.contents)

	def set_contents(self, contents):
		'''
		Set this TroubleshooterAttachment's contents to Base 64 encoded data, or set the
		contents to nothing.
		'''
		if contents:
			self.contents = base64.b64encode(contents)
		else:
			self.contents = None

	def __str__(self):
		return '<TroubleshooterAttachment (%s): %s>' % (self.id, self.filename)
