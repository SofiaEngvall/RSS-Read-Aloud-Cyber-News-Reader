# rss-feeds.py - RSS feed list for rss-read-aloud.py
# version 1.0
# by Sofia Engvall - FixIt42, 2025-05-31, 2026-11-05

### RSS feeds - Please tell me if you have more feeds to add something is incorrect or missing so I can fix it!
### The list was refined and formatted with the help of AI so please tell me errors I missed, like a bad description.
### Format: (name, description, category, feed_url, site_url, status, rating)
### Status: "{overall_status} | link={link_quality} | content={content_type} | desc={desc_quality}"
#("title", "type", "under which header", "rss url", "url", "ok | link=direct | content=full_html | desc=full", 5),


rss_feeds = [


    ("Red Siege Blog", "cyber blog", "blog", "http://redsiege.com/blog/feed", "http://redsiege.com/blog", "ok | link=direct | content=full_html | desc=full", 5),


    # =====================
    # 🚨 Time-Critical Alerts
    # =====================
    ("Krebs on Security", "Investigative security journalism", "alerts", "https://krebsonsecurity.com/feed/", "https://krebsonsecurity.com", "ok | link=direct | content=full_html | desc=partial", 10),
    #("SANS Internet Storm Center", "Daily threat intelligence", "alerts", "https://isc.sans.edu/rssfeed_full.xml", "https://isc.sans.edu", "ok | link=direct | content=rss_only | desc=full", 9),
    ("The Hacker News", "Breaking cybersecurity news", "alerts", "https://feeds.feedburner.com/TheHackersNews?format=xml", "https://thehackernews.com", "ok | link=redirects | content=full_html | desc=partial", 9),
#    ("Dark Reading", "Urgent security news", "alerts", "https://www.darkreading.com/rss.xml", "https://www.darkreading.com", "playwright | link=direct | content=anti_scraping | desc=partial", 9),
    ("BleepingComputer", "Ransomware tracking", "alerts", "https://www.bleepingcomputer.com/feed/", "https://www.bleepingcomputer.com", "ok | link=direct | content=full_html | desc=full", 8),
    ##("Threatpost", "Vulnerability disclosures", "alerts", "https://threatpost.com/feed/", "https://threatpost.com", "outdated | link=direct | content=full_html | desc=partial", 8),
    ("CyberScoop", "Policy and breach alerts", "alerts", "https://www.cyberscoop.com/feed/", "https://www.cyberscoop.com", "ok | link=direct | content=full_html | desc=partial", 7),
    ("NCSC News", "UK National Cyber Security Centre alerts", "alerts", "https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml", "https://www.ncsc.gov.uk/news", "playwright | link=direct | content=js_required | desc=full", 5),

    # =====================
    # 📰 General News
    # =====================
    ("Help Net Security", "Security news", "news", "https://www.helpnetsecurity.com/feed/", "https://www.helpnetsecurity.com", "ok | link=direct | content=full_html | desc=partial", 7),
    ("Schneier on Security", "Security policy analysis", "news", "https://www.schneier.com/feed/atom/", "https://www.schneier.com", "ok | link=direct | content=full_html | desc=partial", 9),
    #***FIX***("SecurityWeek", "Enterprise security news", "news", "https://www.securityweek.com/rss", "https://www.securityweek.com", "playwright | link=direct 403 | content=full_html | desc=partial", 7),
    ("ZDNet Security", "Technology security news", "news", "https://www.zdnet.com/topic/security/rss.xml", "https://www.zdnet.com/security/", "ok | link=direct | content=full_html | desc=partial", 7),
    ("Infosecurity Magazine", "Cybersecurity news", "news", "https://www.infosecurity-magazine.com/rss/news/", "https://www.infosecurity-magazine.com", "ok | link=direct | content=full_html | desc=partial", 7),
    ("Secure Annex", "", "", "https://secureannex.com/blog/rss.xml", "https://secureannex.com", "playwright | link=direct | content=full_html | desc=partial", 5),

    # =====================
    # 🔥 Advanced Threat Intel
    # =====================
    ("Citizen Lab", "Spyware and disinformation research", "threat_intel", "https://citizenlab.ca/feed/", "https://citizenlab.ca", "ok | link=direct | content=full_html | desc=full", 10),
    ("Project Zero", "Zero-day vulnerability research", "threat_intel", "http://googleprojectzero.blogspot.com/feeds/posts/default", "https://googleprojectzero.blogspot.com", "ok | link=direct | content=full_html | desc=full", 10),
    ("Mandiant Blog", "APT group analysis", "threat_intel", "https://www.mandiant.com/resources/blog/rss.xml", "https://www.mandiant.com/resources/blog", "ok | link=direct | content=full_html | desc=full", 9),
    ("Talos Intel", "Threat reports from Cisco", "threat_intel", "https://blog.talosintelligence.com/feeds/posts/default", "https://blog.talosintelligence.com", "ok | link=direct | content=full_html | desc=full", 9),
    ("Kaspersky Securelist", "Malware deep dives", "threat_intel", "https://securelist.com/feed/", "https://securelist.com", "ok | link=direct | content=full_html | desc=full", 8),
    ("Unit42 (Palo Alto)", "Threat intelligence", "threat_intel", "https://unit42.paloaltonetworks.com/feed/", "https://unit42.paloaltonetworks.com", "ok | link=direct | content=full_html | desc=full", 8),
    ("WeLiveSecurity", "Malware trends from ESET", "threat_intel", "https://feeds.feedburner.com/eset/blog", "https://www.welivesecurity.com", "ok | link=direct | content=full_html | desc=full", 8),
    ("FireEye Threat Research", "APT analysis", "threat_intel", "https://www.fireeye.com/blog/threat-research/_jcr_content.feed", "https://www.fireeye.com/blog/threat-research", "ok | link=direct | content=full_html | desc=full", 8),
    ("Check Point Research", "Emerging threats", "threat_intel", "https://research.checkpoint.com/feed/", "https://research.checkpoint.com/", "ok | link=direct | content=full_html | desc=full", 8),
    ("Recorded Future", "Threat intelligence platform", "threat_intel", "https://www.recordedfuture.com/feed", "https://www.recordedfuture.com", "ok | link=direct | content=full_html | desc=partial", 7),
    ("PT SWARM", "APT research", "threat_intel", "https://swarm.ptsecurity.com/feed/", "https://swarm.ptsecurity.com", "empty? | link=direct | content=full_html | desc=full", 7),
    ("Keen Security Lab (Tencent)", "Advanced vulnerability research", "threat_intel", "https://little-canada.org/feeds/output/tencent-keenlabs.rss", "https://keenlab.tencent.com/en/", "outdated | link=direct | content=full_html | desc=full", 7),

    # =====================
    # 🛠️ Exploit Development
    # =====================
    ("PortSwigger Research", "Web application exploits", "exploit_dev", "https://portswigger.net/research/rss", "https://portswigger.net/research", "ok | link=direct | content=full_html | desc=full", 9),
    ("Project Zero Bug Tracker", "Zero-day exploit database", "exploit_dev", "https://little-canada.org/feeds/output/projectzero-bugs.rss", "https://bugs.chromium.org/p/project-zero", "ok | link=direct | content=full_html | desc=none", 9),
    ##("STÖK's Blog", "Bug bounty techniques", "exploit_dev", "https://stokfredrik.com/rss.xml", "https://stokfredrik.com", "404 | link=direct | content=full_html | desc=full", 8),
    ##("Diary of a Reverse-Engineer", "Reverse engineering techniques", "exploit_dev", "https://doar-e.github.io/feeds/rss.xml", "https://doar-e.github.io/", "outdated 2023 | link=direct | content=full_html | desc=full", 8),
    ("Hexacorn", "Malware analysis tricks", "exploit_dev", "https://www.hexacorn.com/blog/feed/", "https://www.hexacorn.com", "ok | link=direct | content=full_html | desc=full", 7),
    ("Doyensec's Blog", "Application security", "exploit_dev", "https://blog.doyensec.com/atom.xml", "https://blog.doyensec.com/", "ok | link=direct | content=full_html | desc=full", 7),
    ##("Access Vector", "Vulnerability research", "exploit_dev", "https://accessvector.net/rss.xml", "https://accessvector.net/", "ok 2024 | link=direct | content=full_html | desc=full", 7),
    ("RET2 Systems Blog", "Exploit development", "exploit_dev", "https://blog.ret2.io/feed.xml", "https://blog.ret2.io/", "ok | link=direct | content=full_html | desc=full", 7),
    ##("Gamozo Labs Blog", "Low-level exploitation", "exploit_dev", "https://gamozolabs.github.io/feed.xml", "https://gamozolabs.github.io/", "old 2021 | link=direct | content=full_html | desc=full", 7),

    # =====================
    # 🔴 Red Team & Offensive
    # =====================
    ("SpecterOps Blog", "Active Directory security", "red_team", "https://posts.specterops.io/feed", "https://posts.specterops.io", "ok | link=direct | content=full_html | desc=full", 9),
    ("MDSec ActiveBreach", "Red team tradecraft", "red_team", "https://www.mdsec.co.uk/feed/", "https://www.mdsec.co.uk", "ok | link=direct | content=full_html | desc=full", 9),
    ("Synacktiv | Publications", "Advanced exploitation", "red_team", "https://little-canada.org/feeds/output/synacktiv-publications.rss", "https://www.synacktiv.com/en/publications", "ok | link=direct | content=full_html | desc=full", 8),
    ("Rhino Security Labs", "Cloud red teaming", "red_team", "https://rhinosecuritylabs.com/feed/", "https://rhinosecuritylabs.com/", "ok | link=direct | content=full_html | desc=full", 7),
    ("Elttam", "Red team research", "red_team", "https://little-canada.org/feeds/output/elttam.rss", "https://www.elttam.com/blog/", "empty | link=direct | content=full_html | desc=full", 7),

    # =====================
    # general tech news
    ("Ars Technica Information Technology", "IT News", "news", "https://feeds.arstechnica.com/arstechnica/technology-lab", "https://arstechnica.com", "ok | link=direct | content=full_html | desc=partial", 0),

    #to test
    ("Toms Hardware", "", "", "https://secureannex.com/blog/rss.xml", "https://www.tomshardware.com", "ok | link=direct | content=full_html | desc=partial", 5),
    # =====================

    # =====================
    # 🧠 Deep Dives & Education
    # =====================
    ("The DFIR Report", "Incident response case studies", "education", "https://thedfirreport.com/feed/", "https://thedfirreport.com", "ok | link=direct | content=full_html | desc=full", 8),
    ("Lenny Zeltser's Blog", "Malware analysis guides", "education", "https://zeltser.com/feed/", "https://zeltser.com", "ok | link=direct | content=full_html | desc=full", 7),
    ("Windows Internals Blog", "OS security deep dives", "education", "https://windows-internals.com/feed/", "https://windows-internals.com", "ok | link=direct | content=full_html | desc=full", 7),
    #***FIX***("Troy Hunt", "Security tutorials", "education", "https://www.troyhunt.com/rss/", "https://www.troyhunt.com", "ok | link=direct | content=full_html | desc=full", 8),
    ("Trenchant", "Advanced research", "education", "http://little-canada.org/feeds/output/trenchant.rss", "https://trenchant.io/", "ok | link=direct | content=full_html | desc=full", 7),

    # =====================
    # 🎙️ Podcasts
    # =====================
    ("Darknet Diaries", "True cybercrime stories", "podcast", "https://feeds.megaphone.fm/darknetdiaries", "https://darknetdiaries.com", "ok | link=audio | content=episode_page | desc=full", 9),
    ("Risky Business Podcast", "Weekly news roundup", "news", "https://risky.biz/feeds/risky-business/", "https://risky.biz", "ok | link=audio | content=episode_page | desc=full", 9),
    ("Risky Business Podcast", "Weekly news analysis", "podcast", "https://risky.biz/feeds/risky-business/", "https://risky.biz", "ok | link=episode_page | content=show_notes | desc=full", 9),
    #***FIX***("Security Now (TWIT)", "Deep-dive security podcast", "podcast", "https://feeds.twit.tv/sn.xml", "https://twit.tv/shows/security-now", "ok | link=audio | content=episode_page | desc=full", 8),
    ("Graham Cluley", "Security podcast", "podcast", "https://grahamcluley.com/feed/", "https://grahamcluley.com", "ok | link=direct | content=full_html | desc=full", 7),
]
# New rss feeds? google results
# https://www.wired.com/feed/category/security/latest/rss
# https://malpedia.caad.fkie.fraunhofer.de/feeds/rss/latest
# https://gist.github.com/eddiez9/5547081c9df4238d4c47a0e5730ef274
