# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2014, Ravi Sharma
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Feb 6, 2014

@creatorid: Ravi Sharma
'''

from lxml import etree

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError


class NewsComment(KayakoObject):
	'''
	News Comment API Object.

	id                    The unique numeric identifier of the news comment.
	newsitemid            The unique numeric identifier of the news item.
	creatortype           The creator type. Staff: 1, User: 2.
	creatorid             The creator (staff or user) ID. Needed when creator type is Staff, optional when creator type is User.
	fullname              The creator (user) full name. Needed when creator type is User and creator id (user id) is not provided.
	email                 The creator email.
	parentcommentid       Parent comment ID (when replying to some comment).
	commentstatus         The comment status 1 Pending for approval, 2 Approved, 3 Marked as spam.
	useragent             The creator useragent.
	referrer              The referrer.
	parenturl             The parent URL.
	contents              The comment content.
	'''

	controller = '/News/Comment'

	__parameters__ = ['id', 'newsitemid', 'creatortype', 'email', 'creatorid', 'fullname', 'parentcommentid', 'commentstatus', 'useragent', 'referrer', 'parenturl', 'contents', 'dateline', 'ipaddress']

	__required_add_parameters__ = ['newsitemid', 'contents', 'creatortype']
	__add_parameters__ = ['newsitemid', 'contents', 'creatortype', 'creatorid', 'fullname', 'email', 'parentcommentid']

	__required_save_parameters__ = ['newsitemid', 'contents', 'creatortype']
	__save_parameters__ = ['newsitemid', 'contents', 'creatortype', 'creatorid', 'fullname', 'email', 'parentcommentid']

	@classmethod
	def _parse_news_comment(cls, api, news_comment_tree):

		params = dict(
			id=cls._get_int(news_comment_tree.find('id')),
			newsitemid=cls._get_int(news_comment_tree.find('newsitemid')),
			creatortype=cls._get_int(news_comment_tree.find('creatortype')),
			email=cls._get_string(news_comment_tree.find('email')),
			creatorid=cls._get_int(news_comment_tree.find('creatorid')),
			fullname=cls._get_string(news_comment_tree.find('fullname')),
			ipaddress=cls._get_string(news_comment_tree.find('ipaddress')),
			dateline=cls._get_date(news_comment_tree.find('dateline')),
			parentcommentid=cls._get_int(news_comment_tree.find('parentcommentid')),
			commentstatus=cls._get_int(news_comment_tree.find('commentstatus')),
			useragent=cls._get_string(news_comment_tree.find('useragent')),
			referrer=cls._get_string(news_comment_tree.find('referrer')),
			parenturl=cls._get_string(news_comment_tree.find('parenturl')),
			contents=cls._get_string(news_comment_tree.find('contents')),
		)
		return params


	def _update_from_response(self, news_comment_tree):

		for int_node in ['id', 'newsitemid', 'parentcommentid', 'creatortype', 'creatorid', 'commentstatus']:
			node = news_comment_tree.find(int_node)
			if node is not None:
				setattr(self, int_node, self._get_int(node, required=False))

		for str_node in ['email', 'fullname', 'ipaddress', 'useragent', 'referrer', 'parenturl', 'contents']:
			node = news_comment_tree.find(str_node)
			if node is not None:
				setattr(self, str_node, self._get_string(node))

	@classmethod
	def get_all(cls, api, newsitemid):
		response = api._request('%s/ListAll/%s' % (cls.controller, newsitemid), 'GET')
		tree = etree.parse(response)
		return [NewsComment(api, **cls._parse_news_comment(api, news_comment_tree)) for news_comment_tree in tree.findall('newsitemcomment')]


	@classmethod
	def get(cls, api, id):
		response = api._request('%s/%s' % (cls.controller, id), 'GET')
		tree = etree.parse(response)
		node = tree.find('newsitemcomment')
		if node is None:
			return None
		params = cls._parse_news_comment(api, node)
		return NewsComment(api, **params)

	def add(self):
		parameters = self.add_parameters

		for required_parameter in self.__required_add_parameters__:
			if required_parameter not in parameters:
				raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))

		response = self.api._request(self.controller, 'POST', **parameters)
		tree = etree.parse(response)
		node = tree.find('newsitemcomment')
		self._update_from_response(node)

	def save(self):
		response = self._save('%s/%s/' % (self.controller, self.id))
		tree = etree.parse(response)
		node = tree.find('newsitemcomment')
		self._update_from_response(node)


	def delete(self):
		self._delete('%s/%s/' % (self.controller, self.id))


	def __str__(self):
		return '<NewsComment (%s): %s>' % (self.id, self.contents)