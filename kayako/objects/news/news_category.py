# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2014, Ravi Sharma
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Feb 03, 2014

@author: Ravi Sharma
'''

from lxml import etree

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError


class NewsCategory(KayakoObject):
	'''
	News Category API Object.

	id                      The unique numeric identifier of the category.
	title                   The title of the Category.
	newsitemcount           The total news items.
	visibilitytype          The visibility type. public or private.
	'''

	controller = '/News/Category'

	__parameters__ = ['id', 'title', 'newsitemcount', 'visibilitytype']

	__required_add_parameters__ = ['title', 'visibilitytype']
	__add_parameters__ = ['id', 'title', 'newsitemcount', 'visibilitytype']

	__required_save_parameters__ = ['title', 'visibilitytype']
	__save_parameters__ = ['id', 'title', 'newsitemcount', 'visibilitytype']


	@classmethod
	def _parse_news_category(cls, api, news_category_tree):

		params = dict(
			id=cls._get_int(news_category_tree.find('id')),
			title=cls._get_string(news_category_tree.find('title')),
			newsitemcount=cls._get_int(news_category_tree.find('newsitemcount')),
			visibilitytype=cls._get_string(news_category_tree.find('visibilitytype')),
		)
		return params

	def _update_from_response(self, news_category_tree):

		for int_node in ['id', 'newsitemcount']:
			node = news_category_tree.find(int_node)
			if node is not None:
				setattr(self, int_node, self._get_int(node, required=False))

		for str_node in ['title', 'visibilitytype']:
			node = news_category_tree.find(str_node)
			if node is not None:
				setattr(self, str_node, self._get_string(node))

	@classmethod
	def get_all(cls, api, count=100, start=0):
		response = api._request('%s/ListAll/%s/%s/' % (cls.controller, count, start), 'GET')
		tree = etree.parse(response)
		return [NewsCategory(api, **cls._parse_news_category(api, news_category_tree)) for news_category_tree in tree.findall('newscategory')]

	@classmethod
	def get(cls, api, id):
		response = api._request('%s/%s/' % (cls.controller, id), 'GET')
		tree = etree.parse(response)
		node = tree.find('newscategory')
		if node is None:
			return None
		params = cls._parse_news_category(api, node)
		return NewsCategory(api, **params)

	def add(self):
		'''
		Add this NewsCategory.

		Requires:
			title           The category title.
			visibilitytype  The visibility type. public or private.
		'''
		response = self._add(self.controller)
		tree = etree.parse(response)
		node = tree.find('newscategory')
		self._update_from_response(node)

	def save(self):
		response = self._save('%s/%s/' % (self.controller, self.id))
		tree = etree.parse(response)
		node = tree.find('newscategory')
		self._update_from_response(node)

	def delete(self):
		self._delete('%s/%s/' % (self.controller, self.id))

	def __str__(self):
		return '<NewsCategory (%s): %s>' % (self.id, self.title)