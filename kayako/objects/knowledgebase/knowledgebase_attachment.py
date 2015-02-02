# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2014, Ravi Sharma
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Jan 30, 2014

@author: Ravi Sharma <ravi.sharma@kayako.com>
'''

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError
from lxml import etree
import base64


class KnowledgebaseAttachment(KayakoObject):
	'''
    Kayako Knowledgebase Attachment API Object.

    id           The unique numeric identifier of the attachment.
    kbarticleid  The unique numeric identifier of the article.
    filename     The file name for the attachment
    contents     The BASE64 encoded attachment contents
    filesize
    filetype
    dateline
    '''

	controller = '/Knowledgebase/Attachment'

	__parameters__ = ['id', 'kbarticleid', 'filename', 'filesize', 'filetype', 'dateline', 'contents']

	__required_add_parameters__ = ['kbarticleid', 'filename', 'contents']
	__add_parameters__ = ['id', 'kbarticleid', 'filename', 'filesize', 'filetype', 'dateline', 'contents']

	__required_save_parameters__ = ['kbarticleid', 'filename', 'contents']
	__save_parameters__ = ['id', 'kbarticleid', 'filename', 'filesize', 'filetype', 'dateline', 'contents']

	@classmethod
	def _parse_knowledgebase_attachment(cls, knowledgebase_attachment_tree):

		params = dict(
			id=cls._get_int(knowledgebase_attachment_tree.find('id')),
			kbarticleid=cls._get_int(knowledgebase_attachment_tree.find('kbarticleid')),
			filename=cls._get_string(knowledgebase_attachment_tree.find('filename')),
			filesize=cls._get_int(knowledgebase_attachment_tree.find('filesize')),
			filetype=cls._get_string(knowledgebase_attachment_tree.find('filetype')),
			contents=cls._get_string(knowledgebase_attachment_tree.find('contents')),
			dateline=cls._get_date(knowledgebase_attachment_tree.find('dateline')),
		)
		return params

	def _update_from_response(self, knowledgebase_attachment_tree):
		for int_node in ['id', 'kbarticleid', 'filesize']:
			node = knowledgebase_attachment_tree.find(int_node)
			if node is not None:
				setattr(self, int_node, self._get_int(node, required=False))

		for str_node in ['filename', 'filetype', 'contents']:
			node = knowledgebase_attachment_tree.find(str_node)
			if node is not None:
				setattr(self, str_node, self._get_string(node))

		for date_node in ['dateline']:
			node = knowledgebase_attachment_tree.find(date_node)
			if node is not None:
				setattr(self, date_node, self._get_date(node, required=False))

	@classmethod
	def get_all(cls, api, kbarticleid):
		'''
		Get all of the Attachments for article.
		Required:
		kbarticleid     The unique numeric identifier of the .
		'''
		response = api._request('%s/ListAll/%s' % (cls.controller, kbarticleid), 'GET')
		tree = etree.parse(response)
		return [KnowledgebaseAttachment(api, **cls._parse_knowledgebase_attachment(knowledgebase_attachment_tree)) for knowledgebase_attachment_tree in tree.findall('kbattachment')]

	@classmethod
	def get(cls, api, kbarticleid, attachmentid):
		try:
			response = api._request('%s/%s/%s/' % (cls.controller, kbarticleid, attachmentid), 'GET')
		except KayakoResponseError, error:
			if 'HTTP Error 404' in str(error):
				return None
			else:
				raise
		tree = etree.parse(response)
		node = tree.find('kbattachment')
		if node is None:
			return None
		params = cls._parse_knowledgebase_attachment(node)
		return KnowledgebaseAttachment(api, **params)

	def add(self):
		'''
		Add this Attachment.

		Requires:
			kbarticleid  The unique numeric identifier of the article.
			filename     The file name for the attachment
			contents     The BASE64 encoded attachment contents
		'''
		response = self._add(self.controller)
		tree = etree.parse(response)
		node = tree.find('kbattachment')
		self._update_from_response(node)

	def delete(self):
		if self.kbarticleid is None or self.kbarticleid is UnsetParameter:
			raise KayakoRequestError('Cannot delete a Attachment without being attached to a . The ID of the  (kbarticleid) has not been specified.')
		self._delete('%s/%s/%s/' % (self.controller, self.kbarticleid, self.id))

	def get_contents(self):
		''' Return the unencoded contents of this Attachment. '''
		if self.contents:
			return base64.b64decode(self.contents)

	def set_contents(self, contents):
		'''
		Set this Attachment's contents to Base 64 encoded data, or set the
		contents to nothing.
		'''
		if contents:
			self.contents = base64.b64encode(contents)
		else:
			self.contents = None

	def __str__(self):
		return '<KnowledgebaseAttachment (%s): %s>' % (self.id, self.filename)
