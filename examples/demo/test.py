from omibio.bio import AnalysisResult, SeqInterval

res = AnalysisResult([SeqInterval(1, 9, "ACTG", seq_id="test")])
print(res.to_dict())
