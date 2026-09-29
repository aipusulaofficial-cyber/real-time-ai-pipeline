from pipeline_domain import Sample, Window
w=Window(10,max_samples=3)
for s in [Sample("a",2,1),Sample("a",4,5),Sample("b",10,6)]: w.add(s)
report={"size":len(w),"a_mean":w.aggregate("a")}; w.add(Sample("a",8,20)); report["post_eviction_size"]=len(w); report["a_mean_after_eviction"]=w.aggregate("a")
if report["a_mean"]!=3.0 or report["a_mean_after_eviction"]!=8.0: raise SystemExit(report)
print(report)
