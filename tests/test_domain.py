from pipeline_domain import *
def test_window():
 w=Window(10);w.add(Sample("a",2,0));w.add(Sample("a",4,5));w.add(Sample("a",8,12));assert w.aggregate("a")==6