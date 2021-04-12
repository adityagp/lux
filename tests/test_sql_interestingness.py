#  Copyright 2019-2020 The Lux Authors.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from .context import lux
import pytest
import pandas as pd
import numpy as np
import psycopg2
from lux.interestingness.interestingness import interestingness


def test_interestingness_1_0_1(global_var):
    connection = psycopg2.connect("host=localhost dbname=postgres user=postgres password=lux")
    tbl = lux.LuxSQLTable()
    lux.config.set_SQL_connection(connection)
    tbl.set_SQL_table("car")

    tbl.set_intent(
        [
            lux.Clause(attribute="Origin", filter_op="=", value="USA"),
            lux.Clause(attribute="Cylinders"),
        ]
    )
    tbl._repr_html_()
    filter_score = tbl.recommendation["Filter"][0].score
    assert tbl.current_vis[0].score == 0
    assert filter_score > 0
    tbl.clear_intent()


def test_interestingness_0_1_1(global_var):
    connection = psycopg2.connect("host=localhost dbname=postgres user=postgres password=lux")
    tbl = lux.LuxSQLTable()
    lux.config.set_SQL_connection(connection)
    tbl.set_SQL_table("car")

    tbl.set_intent(
        [
            lux.Clause(attribute="Origin", filter_op="=", value="?"),
            lux.Clause(attribute="MilesPerGal"),
        ]
    )
    tbl._repr_html_()
    assert interestingness(tbl.recommendation["Current Vis"][0], tbl) != None
    assert str(tbl.recommendation["Current Vis"][0]._inferred_intent[2].value) == "USA"
    tbl.clear_intent()


def test_interestingness_1_1_1(global_var):
    connection = psycopg2.connect("host=localhost dbname=postgres user=postgres password=lux")
    tbl = lux.LuxSQLTable()
    lux.config.set_SQL_connection(connection)
    tbl.set_SQL_table("car")

    tbl.set_intent(
        [
            lux.Clause(attribute="Horsepower"),
            lux.Clause(attribute="Origin", filter_op="=", value="USA", bin_size=20),
        ]
    )
    tbl._repr_html_()
    assert interestingness(tbl.recommendation["Enhance"][0], tbl) != None

    # check for top recommended Filter graph score is not none
    assert interestingness(tbl.recommendation["Filter"][0], tbl) != None
    tbl.clear_intent()
