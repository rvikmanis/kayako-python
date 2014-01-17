# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Ravi Sharma
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Jan 15, 2014

@author: Ravi Sharma
'''

from lxml import etree

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError

class Category(KayakoObject):
    '''
    Knowledgebase Category API Object.
    
    title                 The title of the Category.
    categorytype          Category type. Global: 1, public: 2, private:3, inherit: 4.
    parentkbcategoryid    The parent category ID.
    displayorder          A positive integer that the helpdesk will use to sort Category when displaying them (ascending).
    articlesortorder      A article sort order. Sort inherti: 1, sort title: 2, sort rating: 3, sort creationdate: 4, sort displayorder: 5 .
    allowcomments         1 or 0 boolean that controls whether or not to Allow comments of this category.
    allowrating           1 or 0 boolean that controls whether or not to Allow rating of this category.
	ispublished           Toggle the published yes/no property using this flag.
	uservisibilitycustom  1 or 0 boolean that controls whether or not to restrict visibility of this category to particular user groups. 
	usergroupidlist		  A list of usergroup id's identifying the user groups to be assigned to this category (see usergroupidlist[]).
	staffvisibilitycustom Toggle the staff visibility custom yes/no property using this flag.
	staffgroupidlist	  The staff group ID list. Multiple values can be comma separated like 1,2,3. 
	staffid				  The creator staff ID. 
    '''

    controller = '/Knowledgebase/Category'

    __parameters__ = ['id', 'title', 'categorytype', 'parentkbcategoryid', 'displayorder', 'articlesortorder', 'allowcomments', 'allowrating', 'ispublished', 'uservisibilitycustom', 'usergroupidlist', 'staffvisibilitycustom', 'staffgroupidlist', 'staffid']

    __required_add_parameters__ = ['title', 'categorytype']
    __add_parameters__ = ['id', 'title', 'categorytype', 'parentkbcategoryid', 'displayorder', 'articlesortorder', 'allowcomments', 'allowrating', 'ispublished', 'uservisibilitycustom', 'usergroupidlist', 'staffvisibilitycustom', 'staffgroupidlist', 'staffid']

    __required_save_parameters__ = ['title', 'categorytype']
    __save_parameters__ = ['id', 'title', 'categorytype', 'parentkbcategoryid', 'displayorder', 'articlesortorder', 'allowcomments', 'allowrating', 'ispublished', 'uservisibilitycustom', 'usergroupidlist', 'staffvisibilitycustom', 'staffgroupidlist', 'staffid']


    @classmethod
    def _parse_category(cls, category_tree):
        usergroups = []
        usergroups_node = category.find('usergroupidlist')
        if usergroups_node is not None:
            for id_node in usergroups_node.findall('usergroupid'):
                id = cls._get_int(id_node)
                usergroups.append(id)
				
		staffgroups = []
        staffgroups_node = category.find('staffgroupidlist')
        if staffgroups_node is not None:
            for id_node in staffgroups_node.findall('staffgroupid'):
                id = cls._get_int(id_node)
                staffgroups.append(id)

        params = dict(
            id=cls._get_int(category_tree.find('id')),
            title=cls._get_string(category_tree.find('title')),
            categorytype=cls._get_int(category_tree.find('categorytype')),
            parentkbcategoryid=cls._get_int(category_tree.find('parentkbcategoryid'), required=False),
            displayorder=cls._get_int(category_tree.find('displayorder')),
            articlesortorder=cls._get_int(category_tree.find('articlesortorder')),
			allowcomments=cls._get_boolean(category_tree.find('allowcomments')),
			allowrating=cls._get_boolean(category_tree.find('allowrating')),
			ispublished=cls._get_boolean(category_tree.find('ispublished')),
			uservisibilitycustom=cls._get_int(category_tree.find('uservisibilitycustom')),
			usergroupidlist=usergroups,
			staffvisibilitycustom=cls._get_string(category_tree.find('staffvisibilitycustom')),
			staffgroupidlist=staffgroups,
			staffid=cls._get_int(category_tree.find('staffid')),
        )
        return params

    def _update_from_response(self, category_tree):
        usergroups_node = category_tree.find('usergroupidlist')
        if usergroups_node is not None:
            usergroups = []
            for id_node in usergroups_node.findall('usergroupid'):
                id = self._get_int(id_node)
                usergroups.append(id)
            self.usergroupidlist = usergroups

        for int_node in ['id', 'categorytype', 'parentkbcategoryid', 'displayorder', 'articlesortorder', 'uservisibilitycustom', 'staffid']:
            node = category_tree.find(int_node)
            if node is not None:
                setattr(self, int_node, self._get_int(node, required=False))

        for str_node in ['title', 'staffvisibilitycustom']:
            node = category_tree.find(str_node)
            if node is not None:
                setattr(self, str_node, self._get_string(node))

        for bool_node in ['allowcomments', 'allowrating', 'ispublished']:
            node = category_tree.find(bool_node)
            if node is not None:
                setattr(self, bool_node, self._get_boolean(node, required=False))

    @classmethod
    def get_all(cls, api, count=100, start=0):

        response = api._request('%s/ListAll/%s/%s' % (cls.controller, count, start), 'GET')
        tree = etree.parse(response)
        return [Category(api, **cls._parse_category(api, category_tree)) for category_tree in tree.findall('kbcategories')]

    @classmethod
    def get(cls, api, id):
        response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        tree = etree.parse(response)
        node = tree.find('kbcategory')
        if node is None:
            return None
        params = cls._parse_category(node)
        return Category(api, **params)

    def add(self):
        response = self._add(self.controller)
        tree = etree.parse(response)
        node = tree.find('kbcategory')
        self._update_from_response(node)

    def save(self):
        response = self._save('%s/%s/' % (self.controller, self.id))
        tree = etree.parse(response)
        node = tree.find('kbcategory')
        self._update_from_response(node)

    def delete(self):
        self._delete('%s/%s/' % (self.controller, self.id))

    def __str__(self):
        return '<Category (%s): %s>' % (self.id, self.title)