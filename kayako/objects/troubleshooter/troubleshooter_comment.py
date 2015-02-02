# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2014, Ravi Sharma
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Feb 13, 2014

@author: Ravi Sharma
'''

from lxml import etree

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError


class TroubleshooterComment(KayakoObject):
	'''
	Troubleshooter Category API Object.

	id                      The unique numeric identifier of the comment.
	troubleshooterstepid    The troubleshooter step ID.
	contents                The step contents.
	creatortype             The creator type. Staff: 1, User: 2.
	creatorid               The creator (staff or user) ID. Needed when creator type is Staff, optional when creator type is User.
	fullname                The creator (user) full name. Needed when creator type is User and creator id (user id) is not provided.
	email                   The creator email.
	parentcommentid         Parent comment ID (when replying to some comment).
	'''

	controller = '/Troubleshooter/Comment'

	__parameters__ = ['id', 'troubleshooterstepid', 'creatortype', 'creatorid', 'fullname', 'email', 'parentcommentid', 'ipaddress', 'dateline', 'commentstatus', 'useragent',
	                  'referrer', 'parenturl', 'contents']

	__required_add_parameters__ = ['troubleshooterstepid', 'contents', 'creatortype']
	__add_parameters__ = ['troubleshooterstepid', 'contents', 'creatortype', 'creatorid', 'fullname', 'email', 'parentcommentid']

	__required_save_parameters__ = ['troubleshooterstepid', 'contents', 'creatortype']
	__save_parameters__ = ['troubleshooterstepid', 'contents', 'creatortype', 'creatorid', 'fullname', 'email', 'parentcommentid']


	@classmethod
	def _parse_troubleshooter_comment(cls, api, troubleshooter_comment_tree):

		params = dict(
			id=cls._get_int(troubleshooter_comment_tree.find('id')),
			troubleshooterstepid=cls._get_int(troubleshooter_comment_tree.find('troubleshooterstepid')),
			creatortype=cls._get_int(troubleshooter_comment_tree.find('creatortype')),
			creatorid=cls._get_int(troubleshooter_comment_tree.find('creatorid')),
			fullname=cls._get_string(troubleshooter_comment_tree.find('fullname')),
			email=cls._get_string(troubleshooter_comment_tree.find('email')),
			ipaddress=cls._get_string(troubleshooter_comment_tree.find('ipaddress')),
			dateline=cls._get_date(troubleshooter_comment_tree.find('dateline')),
			parentcommentid=cls._get_int(troubleshooter_comment_tree.find('parentcommentid')),
			commentstatus=cls._get_int(troubleshooter_comment_tree.find('commentstatus')),
			useragent=cls._get_string(troubleshooter_comment_tree.find('useragent')),
			referrer=cls._get_string(troubleshooter_comment_tree.find('referrer')),
			parenturl=cls._get_string(troubleshooter_comment_tree.find('parenturl')),
			contents=cls._get_string(troubleshooter_comment_tree.find('contents')),
		)
		return params

	def _update_from_response(self, troubleshooter_comment_tree):

		for int_node in ['id', 'troubleshooterstepid', 'creatortype', 'creatorid', 'parentcommentid', 'commentstatus']:
			node = troubleshooter_comment_tree.find(int_node)
			if node is not None:
				setattr(self, int_node, self._get_int(node, required=False))

		for str_node in ['fullname', 'email', 'ipaddress', 'useragent', 'referrer', 'parenturl', 'contents']:
			node = troubleshooter_comment_tree.find(str_node)
			if node is not None:
				setattr(self, str_node, self._get_string(node))

		for date_node in ['dateline']:
			node = troubleshooter_comment_tree.find(date_node)
			if node is not None:
				setattr(self, date_node, self._get_date(node))

	@classmethod
	def get_all(cls, api, troubleshooterstepid):
		response = api._request('%s/ListAll/%s' % (cls.controller, troubleshooterstepid), 'GET')
		tree = etree.parse(response)
		return [TroubleshooterComment(api, **cls._parse_troubleshooter_comment(api, troubleshooter_comment_tree)) for troubleshooter_comment_tree in tree.findall('troubleshooterstepcomment')]

	@classmethod
	def get(cls, api, id):
		response = api._request('%s/%s/' % (cls.controller, id), 'GET')
		tree = etree.parse(response)
		node = tree.find('troubleshooterstepcomment')
		if node is None:
			return None
		params = cls._parse_troubleshooter_comment(api, node)
		return TroubleshooterComment(api, **params)

	def add(self):
		'''
		Add this TroubleshooterComment.
			creatorid               The creator (staff or user) ID. Needed when creator type is Staff, optional when creator type is User.
			fullname                The creator (user) full name. Needed when creator type is User and creator id (user id) is not provided.
			email                   The creator email.
			parentcommentid         Parent comment ID (when replying to some comment).

		Requires:
			troubleshooterstepid    The troubleshooter step ID.
			contents                The step contents.
			creatortype             The creator type. Staff: 1, User: 2.
		'''
		parameters = self.add_parameters

		for required_parameter in self.__required_add_parameters__:
			if required_parameter not in parameters:
				raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))

		response = self.api._request(self.controller, 'POST', **parameters)
		tree = etree.parse(response)
		node = tree.find('troubleshooterstepcomment')
		self._update_from_response(node)

	def save(self):
		response = self._save('%s/%s/' % (self.controller, self.id))
		tree = etree.parse(response)
		node = tree.find('troubleshooterstepcomment')
		self._update_from_response(node)

	def delete(self):
		self._delete('%s/%s/' % (self.controller, self.id))

	def __str__(self):
		return '<TroubleshooterComment (%s): %s>' % (self.id, self.contents)