from realtime_pipeline import *
def test_window_aggregation():
 p=WindowOperator(10,1);p.add(Record("a",1,2));p.add(Record("a",4,4));assert p.emit(10)[("a",0)]==3
def test_late_data_is_dropped():
 p=WindowOperator(10,1);p.add(Record("a",20,1));assert p.add(Record("a",1,1)) is False
def test_invalid_window():
 import pytest
 with pytest.raises(ValueError):WindowOperator(0)
