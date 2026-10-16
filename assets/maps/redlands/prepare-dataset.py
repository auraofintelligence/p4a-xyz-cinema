"""Build the dated Redland source snapshot from reviewed values and retained originals.

This is a deterministic local generator, not an automatic truth or refresh service.
Edit reviewed values and dates only after inspecting the linked primary source.
"""
from pathlib import Path
import hashlib
import json
import re
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CHECKED = "2026-10-16"
UPDATED = "2026-10-17"
SOURCES = [
    {"id":"abs-erp-2025", "title":"ABS Regional population, 2024-25", "publisher":"Australian Bureau of Statistics", "url":"https://www.abs.gov.au/statistics/people/population/regional-population/2024-25", "dataUrl":"https://www.abs.gov.au/statistics/people/population/regional-population/2024-25/32180DS0002_2024-25.xlsx", "localFile":"assets/maps/redlands/abs-regional-population-lga-2024-25.xlsx", "publishedAt":"2026-03-31", "referencePeriod":"30 June 2025", "table":"Table 3, Redland (36250)", "rights":"ABS data, Creative Commons Attribution 4.0", "licenceUrl":"https://www.abs.gov.au/website-privacy-copyright-and-disclaimer", "nextScheduledRelease":"2027-03-25"},
    {"id":"abs-census-2021", "title":"2021 Census Redland LGA QuickStats", "publisher":"Australian Bureau of Statistics", "url":"https://www.abs.gov.au/census/find-census-data/quickstats/2021/LGA36250", "referencePeriod":"2021 Census", "rights":"ABS data, Creative Commons Attribution 4.0", "licenceUrl":"https://www.abs.gov.au/website-privacy-copyright-and-disclaimer"},
    {"id":"abs-census-2026-plan", "title":"2026 Census product guide", "publisher":"Australian Bureau of Statistics", "url":"https://www.abs.gov.au/census/guide-census-data/2026-census-product-guide/latest-release", "publishedAt":"2026-07-28", "referencePeriod":"Release plan, not population results"},
    {"id":"ecq-state-boundaries", "title":"State electorate boundaries and effective dates", "publisher":"Electoral Commission of Queensland", "url":"https://www.ecq.qld.gov.au/electoral-boundaries/state-electorate-boundaries", "referencePeriod":"2017 representation boundaries and 2026 redistribution for 2028"},
    {"id":"ecq-redland-divisions", "title":"Redland City final divisional review", "publisher":"Electoral Commission of Queensland", "url":"https://www.ecq.qld.gov.au/electoral-boundaries/local-government-boundary-reviews/divisional-boundary-reviews/redland-city-council", "publishedAt":"2019-09-20", "referencePeriod":"Final divisions for 2020 election"},
    {"id":"ecq-queensland-councils", "title":"Local government area boundaries", "publisher":"Electoral Commission of Queensland", "url":"https://www.ecq.qld.gov.au/electoral-boundaries/local-government-area-boundaries", "referencePeriod":"Current council finder; 77 Queensland local government areas"},
    {"id":"aec-bowman-profile", "title":"Profile of the electoral division of Bowman", "publisher":"Australian Electoral Commission", "url":"https://www.aec.gov.au/profiles/Qld/Bowman.htm", "publishedAt":"2025-06-18", "referencePeriod":"Boundary gazetted 27 March 2018; used from 2019 election"},
    {"id":"rcc-place", "title":"About Redland City Council", "publisher":"Redland City Council", "url":"https://www.redland.qld.gov.au/About-Council", "referencePeriod":"Council area and communities"},
    {"id":"qgso-erp-2025", "title":"Population growth, regional Queensland, 2024-25", "publisher":"Queensland Government Statistician's Office", "url":"https://www.qgso.qld.gov.au/issues/3106/population-growth-regional-qld-2024-25.pdf", "publishedAt":"2026-03-31", "referencePeriod":"30 June 2025 preliminary ERP", "rights":"The State of Queensland (Queensland Treasury) 2026, CC BY 4.0", "licenceUrl":"https://creativecommons.org/licenses/by/4.0/"},
    {"id":"shapingseq-2023", "title":"Map 3: The local government areas of SEQ, ShapingSEQ 2023", "publisher":"Queensland Government, mirrored by Wikimedia Commons", "url":"https://commons.wikimedia.org/wiki/File:SEQ_LGAs.pdf", "primaryUrl":"https://www.planning.qld.gov.au/__data/assets/pdf_file/0024/86145/shapingseq-2023-Low.pdf", "referencePeriod":"2023 regional plan map; Commons upload 6 November 2025", "rights":"Queensland Government, CC BY 4.0 as recorded on the Commons source page. Source publication copyright and mapping disclaimer also apply.", "licenceUrl":"https://creativecommons.org/licenses/by/4.0/"},
    {"id":"wikipedia-redland-locator", "title":"Redland City locator in South East Queensland", "publisher":"MagpieShooter, Wikimedia Commons", "url":"https://commons.wikimedia.org/wiki/File:SEQ-Councils-Redland.png", "referencePeriod":"15 March 2008 locator, not current electoral divisions", "rights":"MagpieShooter, CC BY-SA 3.0", "licenceUrl":"https://creativecommons.org/licenses/by-sa/3.0/"},
    {"id":"wikipedia-qld-2020-map", "title":"2020 Queensland local elections map", "publisher":"LGA Map, Wikimedia Commons", "url":"https://commons.wikimedia.org/wiki/File:2020_Queensland_local_elections.jpg", "referencePeriod":"2020 historical election geography; image created 1 July 2023", "rights":"LGA Map, CC BY-SA 4.0", "licenceUrl":"https://creativecommons.org/licenses/by-sa/4.0/"},
]
for source in SOURCES:
    source["checkedAt"] = UPDATED if source["id"] in {"shapingseq-2023", "wikipedia-redland-locator", "wikipedia-qld-2020-map"} else CHECKED

def metric(id, label, value, unit, period, source, note="", **extra):
    return dict(id=id, label=label, value=value, unit=unit, period=period,
                geography="Redland LGA (ABS code 36250)", sourceId=source,
                checkedAt=CHECKED, note=note, **extra)

INDICATORS = [
    metric("erp-2025", "Estimated residents", 172831, "people", "30 June 2025", "abs-erp-2025", "Preliminary estimate. ERP is not a Census count.", status="preliminary"),
    metric("erp-2024-revised", "Previous year's revised ERP", 169940, "people", "30 June 2024", "abs-erp-2025", "Use this revised value for comparison with the 2025 release.", status="revised"),
    metric("growth-2025", "Annual population increase", 2891, "people", "2024-25", "abs-erp-2025"),
    metric("growth-percent-2025", "Annual population growth", 1.7, "%", "2024-25", "abs-erp-2025"),
    metric("area-2025", "Statistical land area", 537.2, "sq km", "2025 LGA geography", "abs-erp-2025", "Statistical geography and electoral boundaries are different measures."),
    metric("census-population-2021", "Census usual residents", 159222, "people", "2021 Census", "abs-census-2021"),
    metric("median-age-2021", "Median age", 43, "years", "2021 Census", "abs-census-2021", queenslandValue=38),
    metric("age-65-plus-2021", "Residents aged 65 and over", 33296, "people", "2021 Census", "abs-census-2021", "Calculated by summing the five published age groups from 65-69 to 85+.", percent=20.9, derivation="9946 + 9105 + 6458 + 3988 + 3799; percent rounded to one decimal"),
    metric("dwellings-2021", "Private dwellings", 65165, "dwellings", "2021 Census", "abs-census-2021"),
    metric("household-size-2021", "Average household size", 2.6, "people", "2021 Census", "abs-census-2021"),
    metric("income-2021", "Median weekly household income", 1767, "AUD/week", "2021 Census", "abs-census-2021", "Historical Census measure, not current disposable income or living costs."),
    metric("rent-2021", "Median weekly rent", 420, "AUD/week", "2021 Census", "abs-census-2021", "Historical Census rent, not a 2026 market asking rent."),
    metric("mortgage-2021", "Median monthly mortgage repayment", 1950, "AUD/month", "2021 Census", "abs-census-2021", "Historical Census measure, not current mortgage pricing."),
    metric("lone-households-2021", "Lone person households", 21.9, "%", "2021 Census", "abs-census-2021", "Of occupied private dwellings, excluding visitor-only and unclassifiable households.", count=12889),
    metric("rented-2021", "Households renting", 22.9, "%", "2021 Census", "abs-census-2021", "Occupied private dwellings; excludes rent-free tenure."),
    metric("unpaid-carers-2021", "Provided unpaid assistance", 12.8, "%", "2021 Census", "abs-census-2021", "Residents aged 15+ assisting someone because of disability, health or age during the previous two weeks.", count=16756),
    metric("volunteers-2021", "Volunteered through an organisation", 13.5, "%", "2021 Census", "abs-census-2021", "Residents aged 15+ reporting organisational voluntary work during the previous 12 months; not a C-Hour ledger.", count=17682),
    metric("no-car-2021", "Households with no motor vehicle", 4.5, "%", "2021 Census", "abs-census-2021", "Occupied private dwellings; excludes motorcycles and heavy vehicles.", count=2654),
]

MAPS = []
for id, title, filename in [
    ("oodgeroo", "Oodgeroo: current representation boundary", "oodgeroo-2017"),
    ("capalaba", "Capalaba: current representation boundary", "capalaba-2017"),
    ("redlands-state", "Redlands state district: current representation boundary", "redlands-state-2017"),
    ("springwood", "Springwood: current representation boundary", "springwood-2017"),
]:
    info = json.loads((HERE / (filename + ".pdf.commons.json")).read_text(encoding="utf-8-sig"))
    credit = info["extmetadata"]["Credit"]["value"]
    primary = re.search(r'href="([^"]+)"', credit)
    width, height = Image.open(HERE / (filename + ".png")).size
    MAPS.append(dict(id=id, title=title, image="assets/maps/redlands/"+filename+".png",
        pdf="assets/maps/redlands/"+filename+".pdf", sourceUrl=primary.group(1) if primary else info["descriptionurl"],
        mirrorUrl=info["descriptionurl"], downloadedFrom=info["url"].split("?")[0], edition="2017 electoral boundaries",
        sourceId="ecq-state-boundaries", retrievedAt=CHECKED, width=width, height=height,
        attribution="Electoral Commission Queensland 2017; State of Queensland (Department of Natural Resources and Mines) 2015; map drawn by Spatial Vision. Source PDF mirrored by Wikimedia Commons.",
        rights="Creative Commons Attribution 4.0", licenceUrl="https://creativecommons.org/licenses/by/4.0/",
        transformation="Full first page rendered to PNG at 2200 pixels on its longest side. No geometry redrawn or relabelled.",
        limits="Current parliamentary representation and any state by-election use the 2017 boundaries. The June 2026 redistribution applies at the next state general election in October 2028. Printed roads and background are historical.",
        sha256=hashlib.sha256((HERE / (filename + ".pdf")).read_bytes()).hexdigest()))

width, height = Image.open(HERE / "bowman-2018.png").size
MAPS.append(dict(id="bowman", title="Bowman federal electoral division", image="assets/maps/redlands/bowman-2018.png",
    pdf="assets/maps/redlands/bowman-2018.pdf", sourceUrl="https://www.aec.gov.au/profiles/Qld/Bowman.htm",
    downloadedFrom="https://www.aec.gov.au/Electorates/Redistributions/2017/qld/final-report/files/maps-a4/2017-aec-qld-a4-bowman.pdf",
    edition="March 2018; first used at the 2019 federal election", sourceId="aec-bowman-profile", retrievedAt=CHECKED,
    width=width, height=height, attribution="Commonwealth of Australia 2018; State of Queensland 2018. Compiled by Spatial Vision for the Australian Electoral Commission, with credited source data retained on the map.",
    rights="AEC website material is generally CC BY 4.0, subject to the AEC copyright exceptions and third-party rights. Original map credits and Commonwealth Coat of Arms retained for identification.",
    licenceUrl="https://aec.gov.au/footer/Copyright.htm",
    transformation="Full first page rendered to PNG at 2200 pixels on its longest side. No geometry redrawn or relabelled.",
    limits="AEC profile describes Bowman as parts of Redland and Brisbane councils. The map's council reference layer is 2016. Do not assert exact council equivalence or infer overlap percentages from this image.",
    sha256=hashlib.sha256((HERE / "bowman-2018.pdf").read_bytes()).hexdigest()))

width, height = Image.open(HERE / "seq-lgas-2023.png").size
MAPS.insert(0, dict(id="seq-councils", title="South East Queensland councils: ShapingSEQ 2023", image="assets/maps/redlands/seq-lgas-2023.png",
    pdf="assets/maps/redlands/seq-lgas-2023.pdf", sourceUrl="https://commons.wikimedia.org/wiki/File:SEQ_LGAs.pdf",
    primaryUrl="https://www.planning.qld.gov.au/__data/assets/pdf_file/0024/86145/shapingseq-2023-Low.pdf",
    downloadedFrom="https://upload.wikimedia.org/wikipedia/commons/1/1c/SEQ_LGAs.pdf", edition="ShapingSEQ 2023, Map 3; Commons upload November 2025",
    sourceId="shapingseq-2023", retrievedAt=UPDATED, width=width, height=height,
    attribution="Queensland Government, ShapingSEQ 2023 Map 3; source PDF mirrored on Wikimedia Commons by NimbleNumbat.",
    rights="Creative Commons Attribution 4.0, as recorded on the Commons description page; original publication copyright and mapping disclaimer apply.", licenceUrl="https://creativecommons.org/licenses/by/4.0/",
    transformation="Full source PDF first page rendered to PNG at 2200 pixels on its longest side. No boundaries redrawn.",
    limits="South East Queensland regional-plan context, not all 77 Queensland councils. Toowoomba is labelled urban extent. Does not show council electoral divisions or a precise address lookup.",
    sha256=hashlib.sha256((HERE / "seq-lgas-2023.pdf").read_bytes()).hexdigest()))

# Crop the authentic source rendition for a useful closer context view. This is
# a rectangular document crop, not a newly generated or traced boundary map.
Image.open(HERE / "seq-lgas-2023.png").crop((850, 850, 1510, 1820)).save(HERE / "redland-context-shapingseq-2023.png")
context = dict(MAPS[0])
context.update(id="redland-context", title="Redland and neighbours: detail from the 2023 regional-plan map",
    image="assets/maps/redlands/redland-context-shapingseq-2023.png", width=660, height=970,
    transformation="Rectangular detail cropped from the 1556 by 2200 pixel full-page source rendition, box [850,850,1510,1820]. No boundaries, labels or colours changed.",
    limits="Regional context only. Some neighbouring labels are outside this crop; the full source map is supplied. Does not depict precise coastal water jurisdictions or the ten council divisions.")
MAPS.insert(1, context)

for id, title, filename, source, edition, attribution, rights, licence, limits in [
    ("redland-locator-historical", "Redland locator: historical 2008 outline", "redland-wikipedia-locator-2008.png", "wikipedia-redland-locator", "15 March 2008", "MagpieShooter, Wikimedia Commons", "Creative Commons Attribution-ShareAlike 3.0", "https://creativecommons.org/licenses/by-sa/3.0/", "Historic orientation image. Neighbouring council geography predates later de-amalgamations. Not current divisions or an authoritative boundary lookup."),
    ("queensland-councils-historical", "Queensland councils: historical 2020 election map", "queensland-local-elections-2020.jpg", "wikipedia-qld-2020-map", "2020 election; image created July 2023", "LGA Map, Wikimedia Commons", "Creative Commons Attribution-ShareAlike 4.0", "https://creativecommons.org/licenses/by-sa/4.0/", "Historical election map with political colours. These colours must not be presented as current representation or current election results. Use the ECQ finder for current council boundaries."),
]:
    info = json.loads((HERE / (filename + ".commons.json")).read_text(encoding="utf-8-sig"))
    width, height = Image.open(HERE / filename).size
    MAPS.append(dict(id=id, title=title, image="assets/maps/redlands/"+filename, sourceId=source,
        sourceUrl=info["descriptionurl"], downloadedFrom=info["url"].split("?")[0], edition=edition,
        retrievedAt=UPDATED, width=width, height=height, attribution=attribution, rights=rights,
        licenceUrl=licence, transformation="Original raster image retained unmodified.", limits=limits,
        status="historical-reference", sha256=hashlib.sha256((HERE / filename).read_bytes()).hexdigest()))

width, height = Image.open(HERE / "redland-divisions-2019.png").size
MAPS.insert(0, dict(id="redland-divisions", title="Redland City: official final electoral divisions",
    image="assets/maps/redlands/redland-divisions-2019.png", pdf="assets/maps/redlands/redland-divisions-2019.pdf",
    sourceId="ecq-redland-divisions",
    sourceUrl="https://www.ecq.qld.gov.au/electoral-boundaries/local-government-boundary-reviews/divisional-boundary-reviews/redland-city-council",
    downloadedFrom="https://www.ecq.qld.gov.au/_resource/documents/pdf/electoral-boundaries/local-government-boundary-reviews/divisional-boundary-reviews/redland-city-local-government-area/Redland-Final-Overview.pdf",
    edition="2019 final determination, published 20 September 2019, for the 2020 election",
    retrievedAt=UPDATED, width=width, height=height,
    attribution="The State of Queensland - 2019 (Department of Natural Resources, Mines and Energy); Electoral Commission of Queensland 2019. Creative Commons (CC BY).",
    rights="Creative Commons Attribution (CC BY), as printed on the source map. The version is not specified on this page; source-specific rights are retained.",
    licenceUrl="https://www.ecq.qld.gov.au/_resource/documents/pdf/electoral-boundaries/local-government-boundary-reviews/divisional-boundary-reviews/redland-city-local-government-area/Redland-Final-Overview.pdf",
    transformation="Original ECQ PDF retained. Full first page rendered to PNG at 2200 pixels on its longest side; no boundaries, labels, legend or attribution redrawn.",
    limits="Shows the final ten divisions and outer council boundary from the 2019 review. Printed elector counts and current/projected quota deviations belong to that historical review, not 2026 enrolment. The source describes the map as a guide; use ECQ's current address finder for an exact address.",
    sha256=hashlib.sha256((HERE / "redland-divisions-2019.pdf").read_bytes()).hexdigest()))

data = {
    "schemaVersion":"1.0", "id":"qld-redland", "name":"Redland City", "slug":"redland", "state":"qld", "absLgaCode":"36250",
    "createdAt":CHECKED, "updatedAt":UPDATED, "checkedAt":CHECKED,
    "snapshotStatus":"Reviewed static snapshot. Different sources have different reference dates.",
    "censusStatus":{"latestPublishedLocalCensus":2021, "nextCensusYear":2026, "firstRelease":"June 2027", "secondRelease":"October 2027", "thirdRelease":"Early to mid-2028", "sourceId":"abs-census-2026-plan", "note":"2026 results are not available in this snapshot. A 2027 product preview may use reshaped 2021 data and must not be labelled 2026 Census results."},
    "boundaryNotes":[
        "Redland City council, its ten electoral divisions, state districts and federal divisions are different geographies.",
        "The 2017 state boundaries remain in use for current representation and any by-election until the October 2028 state general election; new boundaries were set in June 2026.",
        "Current state districts relevant to the council include Capalaba, Oodgeroo, Redlands and Springwood. Exact addresses must be checked with ECQ.",
        "No calculated area, resident or elector overlap percentage is asserted. Coastal water boundaries, land area, ABS mesh-block approximations and different editions can produce different totals.",
        "Electoral boundaries do not define or settle Country, Traditional Owner rights or cultural authority."
    ],
    "indicators":INDICATORS, "maps":MAPS, "sources":SOURCES,
    "changeLog":[{"date":CHECKED,"change":"Initial Redland local example: retained authentic map PDFs, PNG renditions, 2025 ERP and explicitly dated 2021 Census indicators. No by-election announcement or candidate intention inferred."}, {"date":UPDATED,"change":"Added the authentic ECQ 2019 final council division map, retrieved through a public browser download after direct downloads were blocked. Also added Wikimedia's authentic ShapingSEQ 2023 regional map, a declared rectangular detail and clearly historical locator references. Historical enrolment labels remain explicitly dated."}],
    "refreshTriggers":[
        {"trigger":"ABS Regional population release or revision", "expected":"2027-03-25", "sourceId":"abs-erp-2025", "action":"Recheck the release schedule; replace ERP and matching revised prior-year values together. Record the release and reference dates."},
        {"trigger":"2026 Census releases", "expected":"From June 2027", "sourceId":"abs-census-2026-plan", "action":"Replace indicators only when matching geography and definitions are released. Keep historical values and do not relabel old prices as current."},
        {"trigger":"ECQ or AEC redistribution, gazette or boundary correction", "expected":"On official publication", "sourceId":"ecq-state-boundaries", "action":"Separate gazetted future boundaries from boundaries used by current representatives and any by-election. Retain original map, edition, credits and changed-date record."},
        {"trigger":"By-election notice or confirmed vacancy", "expected":"Conditional; no date assumed", "action":"Check the official ECQ event and current law before updating any status, countdown or nomination record."}
    ]
}
(REPO / "content/councils/redland.json").write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
print("Wrote content/councils/redland.json:", len(INDICATORS), "indicators;", len(MAPS), "maps")
