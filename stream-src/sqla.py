# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 19:29:06 2015

@author: Евгений
"""

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
metadata = MetaData()
f101 = Table('f101', metadata,
       Column('id', Integer, primary_key=True),
       Column('name', String),
       Column('fullname', String),
... )

>>> addresses = Table('addresses', metadata,
...   Column('id', Integer, primary_key=True),
...   Column('user_id', None, ForeignKey('users.id')),
...   Column('email_address', String, nullable=False)
...  )