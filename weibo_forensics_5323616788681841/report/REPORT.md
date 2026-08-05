# REPORT: Weibo digital forensics for 5323616788681841

## Conclusion (A—F)

A. **Account identity:** current public Sina account page for UID path `8345249001` displays **王澎程**, automobile-blogger verification, Hunan location, and 2025.10 join date. A 2026-07-09 post on the same Sina mirror context says “我能改名成‘王澎程’吗？”. Search-result residue for the account page contains text prefixed by **石头日谈:** and current **王澎程** entries. This supports a **high-probability rename relationship**, but the old-name-to-UID relation remains **not fully proven** because no preserved page was recovered that simultaneously exposes UID `8345249001` and old display name `石头日谈` in a first-party HTML body.

B. **Original post recovery:** the strongest recovered public evidence for `5323616788681841` is a search-result/Sina snippet for `https://www.sina.cn/news/detail/5323616788681841.html` showing the exact target wording, `http://t.cn/AX9xdpfY`, and Hunan publication location. Direct open of the Sina mirror in the browser-text tool redirected to the Sina home shell and did not expose the original body. Local `curl` collection from the container was blocked by a proxy CONNECT 403 for HTTPS targets, so raw HTML from Sina/Weibo could not be independently downloaded from the shell.

C. **Shortlink and redirect chain:** local shell attempts were made for HTTP/HTTPS, GET/HEAD, follow/no-follow, and desktop/mobile User-Agent variants. HTTPS requests were blocked by the environment proxy (`CONNECT tunnel failed, response 403`). HTTP `t.cn` body/header files were saved where the command produced files, but a complete authoritative redirect chain to a video object was not recovered in this run.

D. **Video object:** Base62 conversion confirms that Weibo decimal status `5323616788681841` maps to shortcode `R9UnAAqxH`; video-like decimal `5323616443629696` maps to `R9Un2fefu`. The candidate `fid=1034:5323616443629696` remains a **candidate fid**, not confirmed object_id/media_id, because accessible first-party JSON/HTML containing `fid`, `object_id`, `media_info`, `playback_list`, `mp4`, or `m3u8` was not recovered. No source video file was downloaded.

E. **Reposts/copies/news:** a Sina account search result for `简称老朱` preserved the same target text and shortlink at 2026-07-29 15:03. Tencent/ZAKER-style news reports from 2026-07-31 onward describe the broader “竹知了 / 1000块钱以内最好玩的玩具 / 1000万以内” controversy, but the accessible text does not prove they embedded the same target video.

F. **Earliest-source judgment:** final classification is **当前最早可复核样本 / 很早的传播节点**, not “已确认首发”. It is not proven to be the earliest bamboo-cicada content, not proven to be the original upload of the target video, and not proven to be the earliest occurrence of the broader phrase.

## Evidence inventory

| Item | URL | Captured UTC / Beijing | Local path | SHA-256 | Content | Confidence | Reviewable | Type / limitation |
|---|---|---|---|---|---|---|---|---|
| Tool-excerpt evidence log | multiple | 2026-08-05 UTC / 2026-08-05 CST | `raw/html/web_search_findings.txt` | see `evidence/hashes.sha256` | Search/open excerpts for Sina target, account page, rename clue, repost, and news | Medium | Partial | Fact/excerpt; generated from browser-search tool, not raw origin HTML |
| Query log | many site-directed searches | 2026-08-05 UTC / CST | `evidence/query_log.csv` | see hashes | Required identifiers and phrases across requested platform categories | Medium | Partial | Search log; many counts unknown due blocked/dynamic search |
| HTTP attempt log | core URLs | 2026-08-05 UTC / CST | `evidence/evidence.csv`, `raw/http/*` | see hashes | GET/HEAD, redirect-following attempts and headers/bodies where generated | Medium | Partial | Negative result; local network proxy blocked many HTTPS requests |
| Base62 script | local reproducible script | local | `scripts/weibo_base62.py` | see hashes | Converts decimal Weibo mids to shortcodes | High | Yes | Algorithmic inference, not source-page evidence |

## Confirmed facts

1. `https://www.sina.cn/media/8345249001` currently displays the account name **王澎程**, biography text, **汽车博主**, **湖南**, and “2025.10 加入”.
2. `https://www.sina.cn/news/detail/5318734828801903.html` displays **王澎程**, timestamp **26-07-09 11:44**, verification **汽车博主**, text “我能改名成‘王澎程’吗？”, and **发布于 湖南**.
3. Search-result residue for `https://www.sina.cn/news/detail/5323616788681841.html` contains the target exact text, shortlink `http://t.cn/AX9xdpfY`, and “发布于湖南”.
4. Search-result residue for `https://www.sina.cn/media/1749821214` shows `简称老朱` repost/copy-like entry containing the same target text and shortlink at **2026-07-29 15:03**.
5. Decimal `5323616788681841` converts to Base62 `R9UnAAqxH`; decimal `5323616443629696` converts to `R9Un2fefu`.

## High-probability inferences

- UID path `8345249001` belongs to the current account page for **王澎程**.
- The July 9 “能改名成王澎程吗” post and search residue mentioning **石头日谈** indicate the account likely changed its public display name from 石头日谈 to 王澎程.
- The target post likely existed on Sina/Weibo with the provided text and shortlink, but the original raw page body was not recovered in this environment.

## Unverified leads

- `fid=1034:5323616443629696` is not yet confirmed from a recovered first-party field.
- `object_id`, `media_id`, `playback_list`, `mp4`, `m3u8`, title, duration, cover, and CDN URL remain unrecovered.
- Bilibili candidates `BV1Yu3T6zEeJ` and `BV1KD3g6uE6t`, Zhihu question `2066003943059203398`, and names “木木家的猫lucky” / quoted text “涉嫌侵权，已经投诉了啊” require additional access or manual browsing beyond what the blocked shell environment and text search exposed.

## Negative and blocked results

- Local shell HTTP capture was attempted, but HTTPS requests failed with `CONNECT tunnel failed, response 403`; this prevented raw independent downloads of many Weibo/Sina/video/archive pages from the container.
- Browser-text opening of the target Sina detail URL redirected to a generic Sina shell rather than the target detail content.
- Video pages returned errors or inaccessible dynamic content in the text browser; no playable media URL was recovered.
- Archive and cache checks were scripted for Wayback, archive.today, Arquivo.pt, and URL variants, but many raw responses could not be fetched by local shell because of the same network limitation.

## Next best steps

1. Use a normal residential/mobile network or authenticated browser session to export the m.weibo.cn JSON for `5323616788681841` and any `page_info/media_info` fields.
2. Resolve `http://t.cn/AX9xdpfY` with `curl -v --location-trusted` from multiple regions/User-Agents and preserve each `Location` header.
3. Query Weibo video APIs from an authenticated session for `fid=1034:5323616443629696`, then download original `mp4`/`m3u8` without transcoding.
4. Use browser devtools HAR capture on Sina mirror/account pages and Weibo TV pages to preserve embedded JSON and JS API calls.
5. Perform reverse-image search from any recovered cover thumbnail and compare Bilibili/Zhihu/Douyin candidates by frame, audio, duration, and object identifiers.
