#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Formal
# ======
#
# Copyright 2013 Rob Britton
# Copyright 2015-2019 Heiko 'riot' Weinen <riot@c-base.org> and others.
#
# This file has been changed and this notice has been added in
# accordance to the Apache License
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Changes notice
==============

This file has been changed by the Hackerfleet Community and this notice has
been added in accordance to the Apache License 2.0

"""

import unittest

import formal

from datetime import datetime, timedelta
from time import sleep
from copy import deepcopy


class TestCreating(unittest.TestCase):
    def setUp(self):
        """Set up the test scaffolding"""
        self.schema = {
            "name": "Country",
            "id": "#Country",
            "properties": {
                "name": {"type": "string"},
                "abbreviation": {"type": "string"},
                "languages": {"type": ["array", "null"], "items": {"type": "string"}},
            },
            "additionalProperties": False,
        }

        # Connect to formal_test - hopefully it doesn't exist
        formal.connect("formal_test")
        self.Country = formal.model_factory(self.schema)

        # Drop all the data in it
        self.Country.collection().delete_many({})

        # Create some defaults
        self.Country({"name": "Sweden", "abbreviation": "SE", "languages": ["swedish"]})
        self.Country(
            {
                "name": "United States of America",
                "abbreviation": "US",
                "languages": ["english"],
            }
        )

    def testNormalCreate(self):
        """ Test with doing things the Mongo way """

        canada = self.Country(
            {"name": "Canada", "abbreviation": "CA", "languages": ["english", "french"]}
        )

        canada.save()

        self.assertEqual("Canada", canada.name)
        self.assertEqual("CA", canada.abbreviation)
        self.assertEqual(2, len(canada.languages))
        self.assertTrue("english" in canada.languages)
        self.assertTrue("french" in canada.languages)

    def testHistoryCreate(self):
        canada = self.Country(
            {"name": "Canada", "abbreviation": "CA"}
        )

        canada._history = True
        canada.save()
        canada_id = canada._fields["_id"]

        history_collection = canada.history_collection

        assert history_collection is not None

        history = history_collection().find_one({'id': canada_id})
        assert history is not None

        assert isinstance(history['t'], datetime)
        assert isinstance(history['c'], str)
        assert history['id'] == canada_id

        canada.languages = ["french"]
        canada.save()

        canada.languages.append("english")
        canada.save()

        for history in history_collection().find({'id': canada_id}):

            assert isinstance(history['t'], datetime)
            assert isinstance(history['c'], str)
            assert history['id'] == canada_id

    def testHistoryRecreate(self):
        canada = self.Country(
            {"name": "Canada", "abbreviation": "CA"}
        )

        begin = datetime.now()

        canada._history = True
        canada.save()

        canada.languages = ['english']
        canada.save()
        sleep(0.2)

        canada.languages.append('french')
        canada.save()
        sleep(0.2)

        rebuilt_canada = canada.get_historical(begin, datetime.now())

        fields = deepcopy(canada._fields)
        del fields['_id']

        assert rebuilt_canada == fields
