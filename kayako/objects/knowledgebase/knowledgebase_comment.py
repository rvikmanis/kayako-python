# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2014, Ravi Sharma
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Jan 31, 2014

@author: Ravi Sharma <ravi.sharma@kayako.com>
'''

from lxml import etree

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError


class KnowledgebaseComment(KayakoObject):
	'''
	Kayako Comment API Object.

	kbarticleid         The knowledgebase article ID.
	contents            The knowledgebase comment content
	creatortype         The creator type. Staff: 1, User: 2.
	creatorid           The creator (staff or user) ID. Needed when creator type is Staff, optional when creator type is User.
	fullname            The creator (user) full name. Needed when creator type is User and creator id (user id) is not provided.
	email               The creator email.
	parentcommentid     Parent comment ID (when replying to some comment).
	'''

	controller = '/Knowledgebase/Comment'

	__parameters__ = [
		'id',
		'knowledgebasearticleid',
		'kbarticleid',
		'creatortype',
		'creatorid',
		'fullname',
		'email',
		'ipaddress',
		'dateline',
		'parentcommentid',
		'commentstatus',
		'useragent',
		'referrer',
		'parenturl',
		'contents',
	]

	__required_add_parameters__ = ['knowledgebasearticleid', 'contents', 'creatortype']
	__add_parameters__ = ['knowledgebasearticleid', 'knowledgebasearticleid', 'contents', 'creatortype', 'creatorid', 'fullname', 'email', 'parentcommentid']

	@classmethod
	def _parse_knowledgebase_comment(cls, knowledgebase_comment_tree, knowledgebasearticleid):

		params = dict(
			id=cls._get_int(knowledgebase_comment_tree.find('id')),
			knowledgebasearticleid=knowledgebasearticleid,
			creatortype=cls._get_int(knowledgebase_comment_tree.find('creatortype')),
			creatorid=cls._get_int(knowledgebase_comment_tree.find('creatorid')),
			fullname=cls._get_string(knowledgebase_comment_tree.find('fullname')),
			email=cls._get_string(knowledgebase_comment_tree.find('email')),
			ipaddress=cls._get_string(knowledgebase_comment_tree.find('ipaddress')),
			dateline=cls._get_date(knowledgebase_comment_tree.find('dateline')),
			parentcommentid=cls._get_int(knowledgebase_comment_tree.find('parentcommentid')),
			commentstatus=cls._get_int(knowledgebase_comment_tree.find('commentstatus')),
			useragent=cls._get_string(knowledgebase_comment_tree.find('useragent')),
			referrer=cls._get_string(knowledgebase_comment_tree.find('referrer')),
			parenturl=cls._get_string(knowledgebase_comment_tree.find('parenturl')),
			contents=cls._get_string(knowledgebase_comment_tree.find('contents')),
		)
		return params

	def _update_from_response(self, knowledgebase_comment_tree):

		for int_attr in ['id', 'knowledgebasearticleid', 'creatortype', 'creatorid', 'commentstatus', 'useragent', 'parentcommentid']:
			attr = knowledgebase_comment_tree.get(int_attr)
			if attr is not None:
				setattr(self, int_attr, self._parse_int(attr, required=False))

		for str_attr in ['contents', 'fullname', 'email', 'ipaddress', 'referrer', 'parenturl']:
			attr = knowledgebase_comment_tree.get(str_attr)
			if attr is not None:
				setattr(self, str_attr, attr)

		for date_attr in ['dateline']:
			attr = knowledgebase_comment_tree.get(date_attr)
			if attr is not None:
				setattr(self, date_attr, self._parse_date(attr, required=False))

	@classmethod
	def get_all(cls, api, knowledgebasearticleid):
		'''
		Get all of the Comments for a article.
		Required:
			kbarticleid         The knowledgebase article ID.
		'''
		response = api._request('%s/ListAll/%s' % (cls.controller, knowledgebasearticleid), 'GET')
		tree = etree.parse(response)
		return [KnowledgebaseComment(api, **cls._parse_knowledgebase_comment(knowledgebase_comment_tree, knowledgebasearticleid)) for knowledgebase_comment_tree in tree.findall('kbarticlecomment')]

	@classmethod
	def get(cls, api, knowledgebasearticleid, id):
		try:
			response = api._request('%s/%s/' % (cls.controller, id), 'GET')
		except KayakoResponseError, error:
			if 'HTTP Error 404' in str(error):
				return None
			else:
				raise
		tree = etree.parse(response)
		node = tree.find('kbarticlecomment')
		if node is None:
			return None
		params = cls._parse_knowledgebase_comment(node, knowledgebasearticleid)
		return KnowledgebaseComment(api, **params)

	def add(self):
		'''
		Add this Comment.

		Requires:
			kbarticleid         The unique numeric identifier of the article.
			contents            The knowledgebase article comment contents
			creatortype         The creator type. Staff: 1, User: 2.
		Optional:
			creatorid           The creator (staff or user) ID. Needed when creator type is Staff, optional when creator type is User.
			fullname            The creator (user) full name. Needed when creator type is User and creator id (user id) is not provided.
			email               The creator email.
			parentcommentid     Parent comment ID (when replying to some comment).
		'''
		if self.id is not UnsetParameter:
			raise KayakoRequestError('Cannot add a pre-existing %s. Use save instead. (id: %s)' % (self.__class__.__name__, self.id))

		parameters = self.add_parameters

		for required_parameter in self.__required_add_parameters__:
			if required_parameter not in parameters:
				raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))

		response = self.api._request(self.controller, 'POST', **parameters)
		tree = etree.parse(response)
		node = tree.find('kbarticlecomment')
		self._update_from_response(node)

	def delete(self):
		if not self.id:
			raise KayakoRequestError('Cannot delete a Comment without being attached to a article. The ID of the Comment (id) has not been specified.')
		self._delete('%s/%s/' % (self.controller, self.id))

	def __str__(self):
		return '<KnowledgebaseComment (%s): %s>' % (self.id, self.contents)
