"""One planned source acquisition for remaining council ballot/roster gaps.

Default is offline inventory. --acquire requests only the listed public official
seed URLs and follows their ordinary redirects with standard verified TLS. No
certificate exception, access-control bypass, repeated retry or private contacts
are used. Full source files remain local-only. Subsequent linked-table acquisition
must be explicitly added to this adapter, not ad-hoc URL guessing.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import urllib.request
import urllib.parse

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'content/places/raw'
REPORT = ROOT / 'content/places/sources/council-expansion-acquisition.json'
CHECKED = '2026-10-17'
SEEDS = [
    ('qld-2024-ballots', 'https://resultsdata.elections.qld.gov.au/2024QLGE-electorates.json', 'json'),
    ('qld-2024-results', 'https://resultsdata.elections.qld.gov.au/XMLData/publicResults_LG2024_Inala24_IpswichWest24_Final.zip', 'zip'),
    ('qld-2024-event-data', 'https://event.elections.qld.gov.au/Events/EventData?EventID=622&EventType=2', 'html'),
    ('qld-directory', 'https://www.localgovernment.qld.gov.au/for-councils/local-government-directory', 'html'),
    ('sa-2022-results', 'https://ecsa.sa.gov.au/?catid=9&id=1011%3A2022-council-elections-results-and-statistics&view=article', 'html'),
    ('sa-directory', 'https://www.lga.sa.gov.au/sa-councils/councils-listing', 'html'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--acquire', action='store_true')
    parser.add_argument('--sa-results', action='store_true', help='Use the cached verified ECSA index to acquire only candidate/contest-control and council result workbooks in one batch.')
    args = parser.parse_args()
    previous = json.loads(REPORT.read_text(encoding='utf-8')) if REPORT.exists() else None
    seeds = SEEDS
    if args.sa_results:
        # Read-only HTML inspection uses the existing system BeautifulSoup4
        # runtime. The bundled acquisition runtime needs only the standard lib.
        from html.parser import HTMLParser
        class Links(HTMLParser):
            def __init__(self):super().__init__();self.hrefs=[]
            def handle_starttag(self,tag,attrs):
                row=dict(attrs)
                if tag=='a' and row.get('href'):self.hrefs.append(row['href'])
        parsed=Links();parsed.feed((RAW/'council-expansion-sa-2022-results.html').read_text(encoding='utf-8'))
        hrefs=[h for h in parsed.hrefs if '/component/edocman/' in h and ('results-statistics' in h or any(k in h for k in ['details-of-candidates-and-elected-members','uncontested-failed-elections','vacancies-candidates-and-election-status']))]
        seeds=[('sa-2022-'+h.split('/')[3],urllib.parse.urljoin('https://ecsa.sa.gov.au/',h),'xlsx') for h in dict.fromkeys(hrefs)]
    if not args.acquire:
        print(json.dumps({'plannedSources': len(seeds), 'urls':[u for label,u,suffix in seeds]}, ensure_ascii=True, indent=2))
        return

    def request(seed):
        label, url, suffix = seed
        path = RAW / ('council-expansion-'+label+'.'+suffix)
        if path.exists():
            entry = next((r for r in (previous or {}).get('requests',[]) if r['url']==url and r.get('status')=='retained'),None)
            if entry and entry.get('sha256')==hashlib.sha256(path.read_bytes()).hexdigest():
                return entry
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'P4A public civic atlas research/1.0', 'Accept':'application/json,text/html,*/*'})
            with urllib.request.urlopen(req, timeout=55) as response:
                body, final_url = response.read(), response.url
            path.write_bytes(body)
            return {'label':label, 'url':url, 'finalUrl':final_url, 'checked':CHECKED,
                    'status':'retained', 'certificateValidation':'enabled',
                    'rawFile':path.relative_to(ROOT).as_posix(), 'sha256':hashlib.sha256(body).hexdigest(), 'bytes':len(body)}
        except Exception as exc:
            return {'label':label, 'url':url, 'checked':CHECKED, 'status':'unavailable', 'certificateValidation':'enabled', 'error':str(exc)}
    RAW.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(request, seeds))
    results += [r for r in (previous or {}).get('requests',[]) if r['url'] not in {u for label,u,suffix in seeds}]
    report = {'schemaVersion':1, 'checked':CHECKED, 'originalsLocalOnly':True,
              'method':'One planned official-source batch, standard verified TLS, no bypass or automatic retry.',
              'requests':results, 'previousRuns':((previous or {}).get('previousRuns',[])+[previous['requests']]) if previous else []}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'retained':sum(r['status']=='retained' for r in results),'requests':results},ensure_ascii=True,indent=2))


if __name__=='__main__':
    main()
