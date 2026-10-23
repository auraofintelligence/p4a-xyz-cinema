"""Normalize retained TEC result fragments, NT browser facts and ACT countback."""
import hashlib,json,pathlib,re
from state_place_supplements import ROOT,RAW,CHECKED,read,slug,source

def apply(d,rows):
    from bs4 import BeautifulSoup
    registry={r['id']:r for r in rows};audit=[]
    for rec in rows:
        if not re.fullmatch(r'state-tas-lc-result-[a-z]+-20\d\d(?:-by-election)?',rec['id']):continue
        path=ROOT/rec['rawFile']
        if not path.exists():continue
        parts=rec['id'].split('-');area=parts[4];year=parts[5]
        p=next(p for p in d['places'] if p['id'].startswith('state-tas-lc-') and p['slug']==area)
        events=[e for e in p['elections'] if e['status']=='historical' and e['date'].startswith(year)]
        assert len(events)==1,(area,year,events)
        e=events[0];source(d,rows,rec['id'],'TEC '+year+' '+p['name']+' final Legislative Council result page')
        fp=registry.get(rec['id']+'-fp');candidates=[];formal=informal=None
        if fp and (ROOT/fp['rawFile']).exists():
            ss=BeautifulSoup((ROOT/fp['rawFile']).read_text(encoding='utf8'),'html.parser')
            headers=ss.select('tr')[0].select('.candidate-column-width')
            # Some official 2022 fragments omit the opening TR around TOTALS;
            # the source's explicit totals-cell class still defines the row.
            cells=ss.select('td.totals,th.totals')
            assert cells[0].get_text(strip=True)=='TOTALS'
            numbers=[int(td.get_text(strip=True).replace(',','')) for td in cells[1:]]
            assert len(numbers)==len(headers)+3
            for td,votes in zip(headers,numbers):
                name=td.select_one('.candidate-name').get_text(' ',strip=True)
                party=td.select_one('.candidate-party').get_text(' ',strip=True)
                candidates.append({'name':name,'party':party,'status':'contested','sourceUrl':rec['url'],'votes':votes,'voteMeasure':'first preferences — final official polling-place totals'})
            formal,informal,total=numbers[-3:]
            assert sum(c['votes'] for c in candidates)==formal and formal+informal==total
            source(d,rows,fp['id'],'TEC '+year+' '+p['name']+' final first-preference result table')
            p['sources'].append(fp['id'])
        else:
            text=BeautifulSoup(path.read_text(encoding='utf8'),'html.parser').get_text(' ',strip=True)
            m=re.search(r'([A-Z]+, [A-Za-z -]+)\s*\((Independent)\) elected unopposed',text)
            assert m and area=='mersey' and year=='2021',(area,year,'missing ballot table')
            candidates=[{'name':m[1],'party':m[2],'status':'elected unopposed; no ballot required','sourceUrl':rec['url']}]
        e.update(candidates=candidates,sourceUrl=rec['url'],resultsUrl=rec['url'],resultStatus='elected unopposed; no ballot required' if formal is None else 'counting completed; official final result table')
        if formal is not None:e.update(formalVotes=formal,informalVotes=informal)
        p['sources']=list(dict.fromkeys(p['sources']+[rec['id']]))
        p['coverageNotes']=[x for x in p['coverageNotes'] if 'complete historical contestant ballots remain unavailable' not in x and 'Previous periodic election candidate reconciliation' not in x]
        if not any('2021–2026 final' in x for x in p['coverageNotes']):p['coverageNotes'].append('The latest 2021–2026 final periodic ballot and available intervening by-election contestants are retained from TEC, with exact first-preference measures. Earlier 2018–2020 histories remain separately dated without complete contestant rows; future exact polling days remain unannounced.')
        audit.append({'place':p['id'],'event':e['id'],'candidates':len(candidates),'formalVotes':formal,'sourceId':fp['id'] if fp else rec['id']})
    for area,date,expected in [('nightcliff','2026-03-07',4),('mulka','2026-09-12',2)]:
        path=RAW/('state-nt-'+area+'-browser-results.json')
        if not path.exists():continue
        facts=read(path);sid='state-nt-'+area+'-2026-browser-results'
        add_extraction(d,sid,path,facts['url'],'NTEC '+area.title()+' 2026 by-election minimal rendered result table facts',facts['method'])
        p=next(p for p in d['places'] if p['jurisdiction']=='nt' and p['slug']==area)
        parties=dict(facts['parties']);candidates=[]
        for row in facts['summary']:
            if not row[0]:continue
            c={'name':row[0],'party':parties[row[1]],'votes':int(row[2].replace(',','')),'voteMeasure':'first preferences','status':'contested','sourceUrl':facts['url']}
            if row[3].strip():c.update(twoCandidatePreferredVotes=int(row[3].replace(',','')),twoCandidatePreferredMeasure='two candidate preferred — final count 3')
            if area=='nightcliff' and row[0]=='Ed SMELT' and 'elected at count 3' in facts['intro']:c['status']='elected at count 3'
            candidates.append(c)
        totals={row[0]:int(row[1].replace(',','')) for row in facts['totals'] if row[0]}
        assert len(candidates)==expected and sum(c['votes'] for c in candidates)==totals['Formal']
        assert totals['Formal']+totals['Informal']==totals['Total counted']
        eid='nt-'+area+'-by-election-2026';p['elections']=[e for e in p['elections'] if e['id']!=eid]
        p['elections'].insert(0,{'id':eid,'label':'2026 '+area.title()+' Legislative Assembly by-election','kind':'by-election','status':'historical','date':date,'dateBasis':'Official NTEC by-election timetable/result; current member independently sourced from Parliament','timezone':'Australia/Darwin','sourceUrl':facts['url'],'resultsUrl':facts['url'],'candidates':candidates,'formalVotes':totals['Formal'],'informalVotes':totals['Informal']})
        p['sources']=list(dict.fromkeys(p['sources']+[sid]));p['coverageNotes']=[x for x in p['coverageNotes'] if 'Nightcliff and Mulka' not in x]+['The 2026 '+area.title()+' by-election is separate from the 2024 general election. Official primary totals and source affiliations are retained; current office remains independently verified. '+('The source states Ed Smelt elected at count 3; TCP values remain separate from first preferences.' if area=='nightcliff' else 'The source expressly publishes no TCP count for Mulka; no TCP result or declared winner is inferred from primary votes.')]
        audit.append({'place':p['id'],'event':eid,'candidates':len(candidates),'formalVotes':totals['Formal'],'sourceId':sid})
    path=RAW/'state-act-kurrajong-2026-countback.html';extracted=RAW/'state-act-kurrajong-countback-pdf-facts.json'
    if path.exists() and extracted.exists():
        rec=source(d,rows,'state-act-kurrajong-2026-countback','Elections ACT official 2026 Kurrajong consenting countback candidate roster')
        facts=read(extracted)
        assert all(hashlib.sha256((RAW/name).read_bytes()).hexdigest()==digest for name,digest in facts['sourceHashes'].items()),'Countback PDF changed; re-extract and review'
        soup=BeautifulSoup(path.read_text(encoding='utf8'),'html.parser')
        # Only the six consenting candidate list items from the named release;
        # navigation, the outgoing member and other historical nominees excluded.
        named=[]
        for li in soup.select('li'):
            text=li.get_text(' ',strip=True);m=re.fullmatch(r'([^()]+) \(([^()]+)\)',text)
            if m and any(slug(m[1])==slug(x['name']) for x in facts['candidates']):named.append((m[1],m[2]))
        assert len(named)==6
        candidates=[]
        for name,party in named:
            v=next(x for x in facts['candidates'] if slug(x['name'])==slug(name))
            candidates.append({'name':name,'party':party,'status':v['result'],'sourceUrl':registry['state-act-kurrajong-2026-table2']['url'],'votes':float(v['finalVoteValue']),'voteValueExact':v['finalVoteValue'],'voteMeasure':'countback transferred vote value at end of count 3; not first preferences'})
        p=next(p for p in d['places'] if p['jurisdiction']=='act' and p['slug']=='kurrajong')
        event=next(e for e in p['elections'] if e['id']=='act-kurrajong-countback-2026')
        event.update(candidates=candidates,sourceUrl=rec['url'],resultsUrl=registry['state-act-kurrajong-2026-table2']['url'],dateBasis='Official countback conducted 4 June 2026; formal declaration scheduled 5 June is a separate milestone',resultUpdated=facts['updated'],formalBallotPapers=facts['formalBallotPapers'],totalVoteValueDistributed=facts['totalVoteValueDistributed'],exhaustedVoteValue=facts['exhaustedVoteValue'],lossByFraction=facts['lossByFraction'])
        for sid in ['state-act-kurrajong-2026-table1','state-act-kurrajong-2026-table2']:source(d,rows,sid,'Elections ACT 2026 Kurrajong countback scrutiny '+('ballot papers' if sid.endswith('1') else 'transferred vote values'))
        p['sources']=list(dict.fromkeys(p['sources']+[rec['id'],'state-act-kurrajong-2026-table1','state-act-kurrajong-2026-table2']))
        p['coverageNotes']=[x for x in p['coverageNotes'] if 'consenting contestant roster and transfer values require' not in x]+['All six consenting 2026 Kurrajong countback contestants retain the final count-3 transferred vote values, not 2024 first preferences. The outgoing member is not a consenting contestant. Ballot-paper counts, exhausted vote value and fraction loss remain separate source measures.']
        audit.append({'place':p['id'],'event':event['id'],'candidates':6,'measure':'final countback transferred vote values','pdfColumnAndFinalRowVisualReview':True})
    for p in d['places']:p['sources']=list(dict.fromkeys(p['sources']))
    assert len(audit)==21 and sum(x['candidates'] for x in audit)==86,'Incomplete required retained event history set'
    (ROOT/'content/places/qa/state-history-verification.json').write_text(json.dumps({'checked':CHECKED,'status':'PASS','scope':'18 TEC actual event ballots (including one unopposed election), both NTEC 2026 by-elections, ACT consenting countback/transfer values; source totals reconciled','events':audit,'candidateRecordsAdded':sum(x['candidates'] for x in audit)},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('State event histories reconciled: '+str(len(audit))+' events / '+str(sum(x['candidates'] for x in audit))+' contestant records',flush=True)

def add_extraction(d,sid,path,url,title,method):
    d['sources']=[s for s in d['sources'] if s['id']!=sid]+[{'id':sid,'title':title,'url':url,'checked':CHECKED,'rawFile':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'extractionMethod':method,'licence':'Publisher rights retained; local minimal factual browser extraction, not original HTTP HTML; names/roles/results only.'}]
