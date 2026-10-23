"""Offline minimal factual extraction from retained ACT countback PDFs.

Run with the bundled PDF runtime. Both table page renders were visually checked
against column names, final row and the distinction between papers/vote value.
"""
import hashlib,json,pathlib,re
import pdfplumber
ROOT=pathlib.Path(__file__).resolve().parents[1];RAW=ROOT/'content/places/raw/state'
path=RAW/'state-act-kurrajong-2026-table2.html'
page=pdfplumber.open(path).pages[0]
text=page.extract_text();header=page.extract_table()[1][1:8]
last=text.splitlines()[-1]
values=re.findall(r'-?\d+\.\d{6}',last.split("Shane RATTENBURY",1)[0])
assert len(values)==10,(values,last)
assert values[3]=='0.000000' and values[-1]=='8154.000000'
names=[' '.join(x.split()) for x in header]
assert len(names)==7 and names[3]=='Shane RATTENBURY'
papertext=pdfplumber.open(RAW/'state-act-kurrajong-2026-table1.html').pages[0].extract_text()
assert 'Number of formal papers: 10215' in papertext and 'Rebecca VASSAROTTI elected 1.' in last
out={'checked':'2026-10-17','method':'Minimal factual PDF table extraction with column headers and complete final row checked against rendered original Table 1 (papers) and Table 2 (votes).','sourceFiles':['state-act-kurrajong-2026-table1.html','state-act-kurrajong-2026-table2.html'],'sourceHashes':{f:hashlib.sha256((RAW/f).read_bytes()).hexdigest() for f in ['state-act-kurrajong-2026-table1.html','state-act-kurrajong-2026-table2.html']},'updated':'2026-06-04T12:43:00+10:00','formalBallotPapers':10215,'totalVoteValueDistributed':values[-1],'exhaustedVoteValue':values[-3],'lossByFraction':values[-2],'candidates':[{'name':name,'finalVoteValue':v,'result':'elected' if name=='Rebecca VASSAROTTI' else 'contested'} for name,v in zip(names,values[:7]) if name!='Shane RATTENBURY']}
(RAW/'state-act-kurrajong-countback-pdf-facts.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf8')
print(json.dumps(out))
