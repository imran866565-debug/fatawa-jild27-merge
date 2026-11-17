#!/usr/bin/env python3
"""Merge Jild 27 tashreeh chunks into jild-27.json.

Re-runnable: reads every jild-27-chunk-*.json listed in the manifest,
merges in chunk order, validates (unique ids, page coverage, zero
empty jawab), writes jild-27.json, and updates the manifest statuses.

INPUT (verified on disk by the parent):
  13 chunk files (no splits), 64 chunk items, volume_id 33. Source
  export ~/workspace/fatawa-app/content/jild-27.json: 645 rows but
  only 642 UNIQUE pages (pp. 212, 353, 459 have TWO rows each; each
  listed once in the page union). This is the Jild 16 precedent
  (543 rows, 542 unique pages) and the Jild 26 precedent (562 rows,
  561 unique pages). Validate the merged page union against the
  source export's 642 UNIQUE pages, NOT the 645 row count. Gaps
  (3, nothing invented): pp. 210, 211, 351 — every gap listed in the
  manifest's source_gaps and in each chunk's missing_pages (Jild 17
  lesson). Validate against the chunk items' page union (642 pages),
  NOT range arithmetic.
  NOTE on p. 459: its two source rows are stored in REVERSE print
  order (verified by the coordinator from sentence flow: p. 458 ends
  "hargiz" -> second row "koi hissa is hadd mein maujood nahi..."
  -> first row "zahn mein bhi qar nahi..." -> p. 460 "yunhi
  tawassutiya mein"); the translator covered both in reading order;
  p. 459 listed once. No merge action. p. 353: two source rows
  (lesson-86 row in chunk 07, lesson-87 row in chunk 08); listed
  once in the page union. p. 212: two rows, both covered in
  masala-32 (chunk 04), listed once.

COMBINE RULES (3 cases; parts ordered by min page; pages = UNION of
all parts' pages; notes = all parts' notes; start_page = min page):
  masala 30:   4 parts -> 1, RENAME-THEN-COMBINE. Risala 83 (Maqami'
               al-Hadid) is one mas'ala, pp. 74-163 (90 pp.).
               Chunk 02 muqaddima [74-81] (sawal 7,300, jawab 0) +
               chunk 02 jawab-qawl-awwal [81-100] (sawal 0, jawab
               24,403) + chunk 02 jawab-qawl-dom-som-chaharum
               [100-104] (sawal 0, jawab 4,343) + chunk 03 masala-30
               [105-163] (sawal 0, jawab 10,161) -> ONE item
               'jild27-masala-30', pages [74-163]. Sawal = muqaddima's
               sawal (7,300). Jawab = concatenated in page order
               (24,403 + 4,343 + 10,161 = 38,907). Rename the three
               suffixed ids to 'jild27-masala-30'. Net -3.
  risala 86:   3 parts -> 1, RENAME-THEN-COMBINE. Risala 86
               (Fawz-e-Mubin), pp. 213-353 minus gap 351 = 140 pp.
               Chunk 05 risala-86-muqaddima [213-258] (sawal 0,
               jawab 85,368) + chunk 06 risala-86 [259-303] (sawal 0,
               jawab 58,438) + chunk 07 risala-86 [304-353] (sawal 0,
               jawab 21,166; pages [304-350, 352, 353] — 351 is a
               source gap) -> ONE item 'jild27-risala-86', pages
               [213-353] EXCLUDING 351 (140 unique pages, NOT 141).
               Sawal 0. Jawab = 85,368 + 58,438 + 21,166 = 164,972.
               Rename chunk 05's id to 'jild27-risala-86'. Net -2.
  risala 87 maqam-12-31: 9 parts -> 1, RENAME-THEN-COMBINE. Risala 87
               (al-Kalima al-Mulhama), pp. 399-544 (146 pp.).
               Chunk 08 risala-87-maqam-12 [399-400] (jawab 947) +
               chunk 09 risala-87 [401-450] (jawab 77,378) + chunk 10
               risala-87-maqam-25 [451-454] (jawab 5,622) + chunk 10
               risala-87-maqam-26 [455-465] (jawab 23,632) + chunk 10
               risala-87-maqam-27 [466-467] (jawab 3,915) + chunk 10
               risala-87-maqam-28 [468] (jawab 1,733) + chunk 10
               risala-87-maqam-29 [468-472] (jawab 9,704) + chunk 10
               risala-87-maqam-30 [473-500] (jawab 28,333) + chunk 11
               risala-87 [501-544] (jawab 8,848) -> ONE item
               'jild27-risala-87-maqam-12-31', pages [399-544].
               Sawal 0 (all parts). Jawab = 947 + 77,378 + 5,622 +
               23,632 + 3,915 + 1,733 + 9,704 + 28,333 + 8,848 =
               160,112. Rename ALL nine parts to
               'jild27-risala-87-maqam-12-31'. Why one item: chunk 08
               used per-maqam section ids, chunks 09/11 used the
               single id, chunk 10 used per-maqam ids again — and
               chunks 09 and 11 are each ONE flowing tashreeh passage
               (maqam-12-tail -> 25-head; maqam-30-tail + 31) that
               cannot be split at maqam boundaries without re-reading
               the source and rewriting. Per the Jild 25 masala-158
               mega-combine precedent, absorb all nine parts. Chunk
               08's muqaddima + maqam-01..11 stay SEPARATE (12 items,
               NOT part of this combine). Net -8.
After the combines: 64 - 13 = 51 items covering 642 unique pages.

RENAMES: NO applied-in-chunk print-error renames in this jild — no
printed number was contradicted by sequence. The merge must NOT
apply any renames beyond the three rename-then-combines above. Do
NOT globally normalise bare ids.

EMPTY-JAWAB RULE: after the merge, exactly ZERO empty jawabs. The
only chunk-level empty jawab is 'jild27-masala-30-muqaddima' [74-81]
(intro + question; its jawab is empty by design) and it is resolved
by the masala-30 combine. The merge must NOT flag any empty jawab.
Empty sawal after merge: exactly 19 (all by design — risala
sections or a question not printed in the source): pesh-lafz,
masala-1 (prints "sawal asl mein mazkoor nahi"), risala-86,
risala-87-muqaddima, risala-87-maqam-01..11 (11 items),
risala-87-maqam-12-31, risala-462, risala-463, khatima.

DO-NOT-COMBINES: Masala-19 does NOT exist: headings run 18 -> 20
(chunk 01, pp. 59-60). NO rename of masala-20 -> 19. Recorded in
masala-20's note in chunk 01. Do NOT invent a masala-19 item.
'jild27-masala-8-9' (chunk 01, pp. 18-20) is ONE item covering
printed masail 8 and 9 together (one continuous discussion, title
"Riwayat bil-Ma'na aur Awwal ma Khalaq Allah ki hadithen"). Stays
as one item; no merge action. Chunk 08's muqaddima + maqam-01..11
stay SEPARATE (12 items, NOT part of combine 3). Source gaps: only
210, 211, 351. PUA pages: 108 (chunk 03), 177 (chunk 04), 642
(chunk 13). Garbled/lacuna passages flagged in notes: pp. 313,
320, 333, 344, 347 (chunk 07). Flagged in notes only, never
reconstructed. Fehrist offset: in the lesson-87 region the fehrist
page numbers run ~30 pages ahead of the DB text pagination
(fehrist: maqam-26 p. 485, maqam-27 p. 497, maqam-30 p. 504; text:
pp. 455, 466, 473). Items follow the text headings, not the
fehrist. Volume closes p. 648. First item 'jild27-pesh-lafz'
[4-10], last item 'jild27-khatima' [643-648].

SORT: merged items are sorted by start_page for the final file.
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

# result id -> list of selectors, in page order.
# Selector forms:
#   ('id', sid)            — every item with this id (1 or 2 halves)
#   ('id_start', sid, sp)  — the item with this id starting at page sp
COMBINES = {
    'jild27-masala-30': [
        ('id', 'jild27-masala-30-muqaddima'),
        ('id', 'jild27-masala-30-jawab-qawl-awwal'),
        ('id', 'jild27-masala-30-jawab-qawl-dom-som-chaharum'),
        ('id', 'jild27-masala-30'),
    ],
    'jild27-risala-86': [
        ('id', 'jild27-risala-86-muqaddima'),
        ('id', 'jild27-risala-86'),
    ],
    'jild27-risala-87-maqam-12-31': [
        ('id', 'jild27-risala-87-maqam-12'),
        ('id', 'jild27-risala-87'),
        ('id', 'jild27-risala-87-maqam-25'),
        ('id', 'jild27-risala-87-maqam-26'),
        ('id', 'jild27-risala-87-maqam-27'),
        ('id', 'jild27-risala-87-maqam-28'),
        ('id', 'jild27-risala-87-maqam-29'),
        ('id', 'jild27-risala-87-maqam-30'),
    ],
}

# Sawal handling per combined id (default: sawal from the first part,
# sorted by min page). All three combines are sawal-from-first:
# masala-30's sawal comes from the muqaddima part (7,300 chars);
# the two risala combines have empty sawal on every part.
SAWAL_RULES = {}

# No merge-time renames in this volume beyond the rename-then-
# combines above (which are implemented by the COMBINES table
# itself: the combined item carries the result id). No
# applied-in-chunk renames exist in this jild. Kept empty
# deliberately.
RENAMES = {}

# No applied-in-chunk renames in this jild.
RENAMED_IN_CHUNK = []

# Expected pages for every combined item (spot-check anchors).
EXPECTED_COMBINED_PAGES = {
    'jild27-masala-30': list(range(74, 164)),
    'jild27-risala-86': [p for p in range(213, 354) if p != 351],
    'jild27-risala-87-maqam-12-31': list(range(399, 545)),
}

# Expected sawal/jawab char counts for every combined item.
# masala-30 jawab: 24,403 + 4,343 + 10,161 = 38,907
# risala-86 jawab: 85,368 + 58,438 + 21,166 = 164,972
# risala-87 maqam-12-31 jawab: 947 + 77,378 + 5,622 + 23,632 +
#   3,915 + 1,733 + 9,704 + 28,333 + 8,848 = 160,112
EXPECTED_COMBINED_TEXT = {
    'jild27-masala-30': (7300, 38907),
    'jild27-risala-86': (0, 164972),
    'jild27-risala-87-maqam-12-31': (0, 160112),
}

# Ids absorbed by the combines (must be gone after merging).
# masala-30: the three suffixed part ids (chunk 03's plain
# 'jild27-masala-30' becomes the result id, so it is not absorbed).
# risala-86: chunk 05's muqaddima id (chunks 06/07 already carry
# the result id). risala-87 maqam-12-31: maqam-12, the plain
# 'jild27-risala-87' (chunks 09 and 11), and maqam-25..30.
ABSORBED = [
    'jild27-masala-30-muqaddima',
    'jild27-masala-30-jawab-qawl-awwal',
    'jild27-masala-30-jawab-qawl-dom-som-chaharum',
    'jild27-risala-86-muqaddima',
    'jild27-risala-87-maqam-12',
    'jild27-risala-87',
    'jild27-risala-87-maqam-25',
    'jild27-risala-87-maqam-26',
    'jild27-risala-87-maqam-27',
    'jild27-risala-87-maqam-28',
    'jild27-risala-87-maqam-29',
    'jild27-risala-87-maqam-30',
]

# The only items allowed to keep an empty sawal after merging
# (all by design — risala sections or a question not printed in
# the source). 19 items.
EMPTY_SAWAL_ALLOWED = {
    'jild27-pesh-lafz',
    'jild27-masala-1',
    'jild27-risala-86',
    'jild27-risala-87-muqaddima',
    'jild27-risala-87-maqam-01',
    'jild27-risala-87-maqam-02',
    'jild27-risala-87-maqam-03',
    'jild27-risala-87-maqam-04',
    'jild27-risala-87-maqam-05',
    'jild27-risala-87-maqam-06',
    'jild27-risala-87-maqam-07',
    'jild27-risala-87-maqam-08',
    'jild27-risala-87-maqam-09',
    'jild27-risala-87-maqam-10',
    'jild27-risala-87-maqam-11',
    'jild27-risala-87-maqam-12-31',
    'jild27-risala-462',
    'jild27-risala-463',
    'jild27-khatima',
}

# After the merge, exactly ZERO empty jawabs. The only chunk-level
# empty jawab ('jild27-masala-30-muqaddima') is resolved by the
# masala-30 combine.
EMPTY_JAWAB_ALLOWED = set()

# NO masala-19 may exist anywhere in the volume (headings run 18
# -> 20; verified against ALL chunk files).
NO_MASALA_19 = 'jild27-masala-19'

# Chunk 08's muqaddima + maqam-01..11 must stay SEPARATE items
# (NOT part of combine 3), with these exact pages.
KEPT_SEPARATE = {
    'jild27-risala-87-muqaddima': [353, 354, 355, 356],
    'jild27-risala-87-maqam-01': list(range(356, 374)),
    'jild27-risala-87-maqam-02': list(range(373, 381)),
    'jild27-risala-87-maqam-03': [380, 381, 382, 383],
    'jild27-risala-87-maqam-04': [383, 384, 385, 386, 387],
    'jild27-risala-87-maqam-05': [387, 388],
    'jild27-risala-87-maqam-06': [388, 389, 390, 391],
    'jild27-risala-87-maqam-07': [391, 392],
    'jild27-risala-87-maqam-08': [392],
    'jild27-risala-87-maqam-09': [392, 393],
    'jild27-risala-87-maqam-10': [393, 394, 395, 396, 397, 398],
    'jild27-risala-87-maqam-11': [398, 399],
}


def combine_parts(result_id, parts):
    parts = sorted(parts, key=lambda it: min(it['pages']))
    first = parts[0]
    rule = SAWAL_RULES.get(result_id)
    if rule and rule[0] == 'concat':
        sawal = ''.join((parts[i].get('tashreeh_sawal', '') or '')
                        for i in rule[1])
    elif rule and rule[0] == 'from':
        sawal = parts[rule[1]].get('tashreeh_sawal', '') or ''
    else:
        sawal = first.get('tashreeh_sawal', '') or ''
    title = first.get('title') or ''
    combined = {
        'id': result_id,
        'title': title,
        'volume_id': 33,
        'pages': sorted(set().union(*[set(p['pages']) for p in parts])),
        'start_page': min(min(p['pages']) for p in parts),
        'tashreeh_sawal': sawal,
        'tashreeh_jawab': ''.join((p.get('tashreeh_jawab', '') or '') for p in parts),
        'notes': [n for p in parts for n in (p.get('notes') or [])],
    }
    return combined


def select_parts(all_items, selectors):
    """Resolve selectors to the matching items (each used at most once)."""
    parts = []
    used = set()
    for sel in selectors:
        if sel[0] == 'id':
            hits = [it for it in all_items
                    if it['id'] == sel[1] and id(it) not in used]
        elif sel[0] == 'id_start':
            hits = [it for it in all_items
                    if it['id'] == sel[1] and it['start_page'] == sel[2]
                    and id(it) not in used]
        else:
            raise ValueError(f'unknown selector {sel}')
        assert hits, f'no items matched selector {sel}'
        for it in hits:
            used.add(id(it))
        parts.extend(hits)
    return parts


def run_merge(manifest_path, base, write=False):
    manifest = json.load(open(manifest_path, encoding='utf-8'))
    all_items = []
    merged_chunks = []
    for entry in manifest['chunks']:
        nn = entry['chunk']
        if entry.get('status') == 'split-halves':
            print(f'chunk {nn}: split-halves placeholder — halves are separate entries, skipping')
            continue
        # A chunk may be one file ("file") or split halves ("files").
        file_list = entry.get('files') or [entry['file']]
        items = []
        for fname in file_list:
            path = os.path.join(base, fname)
            if not os.path.exists(path):
                print(f'chunk {nn}: {fname} not yet written')
                continue
            try:
                d = json.load(open(path, encoding='utf-8'))
            except json.JSONDecodeError as e:
                # File may still be streaming from its translator; skip it
                # for now instead of crashing the whole merge.
                print(f'chunk {nn}: {fname} not valid JSON yet ({e}) — skipping for now')
                continue
            items.extend(d['masail'])
        if not items:
            print(f'chunk {nn}: no items loaded — skipping')
            continue
        # Normalize: some translators omit start_page; derive it from pages.
        for it in items:
            if 'start_page' not in it:
                assert it.get('pages'), f'chunk {nn} item {it.get("id")} has no pages'
                it['start_page'] = it['pages'][0]
                print(f'chunk {nn}: derived start_page={it["start_page"]} for {it["id"]}')
            assert it['start_page'] == min(it['pages']), \
                f'chunk {nn} item {it["id"]}: start_page != first page'
            it['_src_file'] = file_list[0]
        all_items.extend(items)
        merged_chunks.append(nn)
        entry['status'] = 'merged'
        print(f'chunk {nn}: {len(items)} items merged')
    print(f'items before combines: {len(all_items)}')
    assert len(all_items) == 64, f'expected 64 chunk items, got {len(all_items)}'
    # COMBINE the 3 cases.
    for result_id, selectors in COMBINES.items():
        parts = select_parts(all_items, selectors)
        combined = combine_parts(result_id, parts)
        assert combined['pages'] == EXPECTED_COMBINED_PAGES[result_id], \
            f'{result_id}: pages {combined["pages"][:3]}...{combined["pages"][-3:]} ({len(combined["pages"])} pp.) != expected {EXPECTED_COMBINED_PAGES[result_id][:3]}...{EXPECTED_COMBINED_PAGES[result_id][-3:]} ({len(EXPECTED_COMBINED_PAGES[result_id])} pp.)'
        exp_sawal, exp_jawab = EXPECTED_COMBINED_TEXT[result_id]
        assert len(combined['tashreeh_sawal']) == exp_sawal, \
            f'{result_id}: sawal {len(combined["tashreeh_sawal"])} chars != expected {exp_sawal}'
        assert len(combined['tashreeh_jawab']) == exp_jawab, \
            f'{result_id}: jawab {len(combined["tashreeh_jawab"])} chars != expected {exp_jawab}'
        assert combined['tashreeh_jawab'], f'{result_id}: combined jawab is empty!'
        if exp_sawal:
            assert combined['tashreeh_sawal'], f'{result_id}: combined sawal is empty!'
        assert combined['start_page'] == min(combined['pages']), f'{result_id}: start_page != min(pages)'
        used_ids = set(id(p) for p in parts)
        all_items = [it for it in all_items if id(it) not in used_ids]
        all_items.append(combined)
        print(f'COMBINED {result_id}: {len(parts)} parts, pages {combined["pages"][0]}-{combined["pages"][-1]} '
              f'({len(combined["pages"])} pages), sawal {len(combined["tashreeh_sawal"])} chars, '
              f'jawab {len(combined["tashreeh_jawab"])} chars, notes {len(combined["notes"])}')
    # RENAMES: none to apply as a separate step (no merge-time renames
    # in this volume; the rename-then-combines are implemented by the
    # COMBINES table itself).
    for old_id, new_id in RENAMES.items():
        assert not any(it['id'] == new_id for it in all_items), \
            f'rename target {new_id} already exists!'
        hits = [it for it in all_items if it['id'] == old_id]
        assert len(hits) == 1, f'rename source {old_id}: expected exactly 1 item, found {len(hits)}'
        hits[0]['id'] = new_id
        print(f'RENAMED {old_id} -> {new_id} (pages {hits[0]["pages"][0]}-{hits[0]["pages"][-1]})')
    # Verify absorbed ids are gone.
    for sid in ABSORBED:
        assert not any(it['id'] == sid for it in all_items), \
            f'absorbed id {sid} must not exist after combining!'
    print(f'absorbed ids gone: {len(ABSORBED)}')
    # Verify applied-in-chunk renames exist (none in this jild).
    for sid in RENAMED_IN_CHUNK:
        hits = [it for it in all_items if it['id'] == sid]
        assert len(hits) == 1, f'applied-in-chunk id {sid}: expected exactly 1 item, found {len(hits)}'
    print(f'applied-in-chunk renames present: {RENAMED_IN_CHUNK}')
    # NO masala-19 may exist anywhere in the volume.
    assert not any(it['id'] == NO_MASALA_19 for it in all_items), \
        f'{NO_MASALA_19} must NOT exist (headings run 18 -> 20)'
    print(f'no {NO_MASALA_19} present (as expected)')
    # 'jild27-masala-8-9' stays as ONE item covering printed masail
    # 8 and 9 together.
    hits = [it for it in all_items if it['id'] == 'jild27-masala-8-9']
    assert len(hits) == 1, f'jild27-masala-8-9: expected exactly 1 item, found {len(hits)}'
    assert hits[0]['pages'] == [18, 19, 20], \
        f'jild27-masala-8-9: pages {hits[0]["pages"]} != [18, 19, 20]'
    print('jild27-masala-8-9 present as one item [18, 19, 20]')
    # Chunk 08's muqaddima + maqam-01..11 stay SEPARATE items with
    # their exact pages (NOT part of combine 3).
    for sid, exp_pages in KEPT_SEPARATE.items():
        hits = [it for it in all_items if it['id'] == sid]
        assert len(hits) == 1, f'{sid}: expected exactly 1 item, found {len(hits)}'
        assert hits[0]['pages'] == exp_pages, \
            f'{sid}: pages {hits[0]["pages"]} != expected {exp_pages}'
    print(f'chunk 08 muqaddima + maqam-01..11 kept separate: {len(KEPT_SEPARATE)} items')
    ids = [it['id'] for it in all_items]
    assert len(ids) == len(set(ids)), f'STILL DUPLICATE IDS: {[i for i in ids if ids.count(i) > 1]}'
    empty = [it['id'] for it in all_items if not it.get('tashreeh_jawab')]
    assert set(empty) == EMPTY_JAWAB_ALLOWED, \
        f'EMPTY JAWAB mismatch: {sorted(empty)} != {sorted(EMPTY_JAWAB_ALLOWED)}'
    print(f'empty jawab: {sorted(empty)} (expected: none)')
    empty_sawal = [it['id'] for it in all_items if not it.get('tashreeh_sawal')]
    assert set(empty_sawal) == EMPTY_SAWAL_ALLOWED, \
        f'EMPTY SAWAL mismatch: {sorted(empty_sawal)} != {sorted(EMPTY_SAWAL_ALLOWED)}'
    print(f'empty sawal (by design only): {sorted(empty_sawal)}')
    pages = set()
    for it in all_items:
        pages.update(it['pages'])
    # PRIMARY coverage check (Jild 17 lesson): validate against the
    # 642 unique pages directly, not against a range-minus-gaps
    # computation. Source gaps are only 210, 211, 351.
    assert len(pages) == 642, f'expected 642 unique pages, got {len(pages)}'
    assert min(pages) == 4 and max(pages) == 648, \
        f'page span {min(pages)}-{max(pages)} != 4-648'
    # Secondary cross-check: per-chunk page range and item count must
    # equal the manifest's values for that chunk. (This manifest uses
    # 'pages' for the [first, last] page range and 'items' for the
    # item count; combined items carry pages from several chunks, so
    # per-chunk attribution must come from the raw file, not from the
    # merged items.)
    for entry in manifest['chunks']:
        if entry['chunk'] in merged_chunks:
            d = json.load(open(os.path.join(base, entry['file']), encoding='utf-8'))
            raw_pages = set()
            for it in d['masail']:
                raw_pages.update(it['pages'])
            assert min(raw_pages) == entry['pages'][0] and max(raw_pages) == entry['pages'][1], \
                f'chunk {entry["chunk"]}: page span {min(raw_pages)}-{max(raw_pages)} != manifest {entry["pages"]}'
            assert len(d['masail']) == entry['items'], \
                f'chunk {entry["chunk"]}: {len(d["masail"])} items != manifest {entry["items"]}'
    print(f'total items: {len(all_items)} | pages covered: {len(pages)}')
    assert len(all_items) == 51, f'expected 51 items after combines, got {len(all_items)}'
    # sort by start_page for the final file
    all_items.sort(key=lambda it: it['start_page'])
    for it in all_items:
        it.pop('_src_file', None)
    if write:
        with open(os.path.join(base, 'jild-27.json'), 'w', encoding='utf-8') as f:
            json.dump({'masail': all_items}, f, ensure_ascii=False, indent=1)
        with open(os.path.join(base, 'chunks-manifest-jild27.json'), 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f'WROTE jild-27.json: {len(all_items)} items, {len(pages)} pages, chunks merged: {merged_chunks}')
    return all_items, pages, merged_chunks


def main():
    manifest_path = os.path.join(BASE, 'chunks-manifest-jild27.json')
    run_merge(manifest_path, BASE, write=True)


if __name__ == '__main__':
    main()
