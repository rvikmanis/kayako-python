# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the GNU General Public License (GPL)
#-----------------------------------------------------------------------------
'''
Created on May 10, 2011

@author: evan
'''

from kayako.test import KayakoAPITest

class TestTicketNote(KayakoAPITest):

    def test_get_all(self):
        from kayako.objects import Department, Ticket, TicketNote

        api = self.api

        depts = api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        ticket = api.create(Ticket)
        ticket.subject = 'DELETE_ME'
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = dept.id
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1
        ticket.userid = 1
        ticket.ownerstaffid = 1
        ticket.type = 'default'
        ticket.add()

        ticket_note = api.create(TicketNote)
        ticket_note.ticketid = ticket.id
        ticket_note.subject = 'test_post'
        ticket_note.contents = 'testing a post'
        ticket_note.staffid = 1
        ticket_note.add()

        result = self.api.get_all(TicketNote, ticket.id)
        assert isinstance(result, list)
        assert result

        ticket = api.get(Ticket, ticket.id)
        assert ticket.notes[0].ticketid == ticket.id

        assert 'TicketNote ' in str(ticket.notes[0])

        ticket.delete()


    def test_add_missing_ticketid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketNote

        ticket_note = self.api.create(TicketNote)

        ticket_note.ticketid = 1
        ticket_note.staffid = 1

        self.assertRaises(KayakoRequestError, ticket_note.add)

    def test_add_missing_contents(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketNote

        ticket_note = self.api.create(TicketNote)

        ticket_note.contents = 'this is just a test'
        ticket_note.staffid = 1

        self.assertRaises(KayakoRequestError, ticket_note.add)

    def test_add_missing_staffid_and_fullname(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketNote

        ticket_note = self.api.create(TicketNote)

        ticket_note.contents = 'this is just a test'

        self.assertRaises(KayakoRequestError, ticket_note.add)

    def test_add_both_staffid_and_fullname(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketNote

        ticket_note = self.api.create(TicketNote)

        ticket_note.ticketid = 1
        ticket_note.contents = 'this is just a test'
        ticket_note.staffid = 1
        ticket_note.fullname = 'test name'

        self.assertRaises(KayakoRequestError, ticket_note.add)
