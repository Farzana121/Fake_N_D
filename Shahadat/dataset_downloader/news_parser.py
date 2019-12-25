from Scrapper.dataset_downloader.news_content_collection import SingleNewsCollector

url = "https://www.prothomalo.com/sports/article/1623715/%E0%A6%AA%E0%A7%81%E0%A6%B0%E0%A7%8B-%E0%A6%AE%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%9A%E0%A6%87-%E0%A6%96%E0%A7%87%E0%A6%B2%E0%A6%A4%E0%A7%87-%E0%A6%AA%E0%A6%BE%E0%A6%B0%E0%A6%9B%E0%A7%87%E0%A6%A8-%E0%A6%A8%E0%A6%BE-%E0%A6%B0%E0%A7%8B%E0%A6%A8%E0%A6%BE%E0%A6%B2%E0%A6%A6%E0%A7%8B?fbclid=IwAR3U7ebtBdOfAzfeWIVlU8g5P4GLBJzcO-1hjBimMCaoFXJOAEAGhBNXcto&h=AT0O-XBAHP2mgPXhG4c_UT87VR0TCY7NdiJLEFVgNTDKvnnJPRmuTA5AKMGN7lDLFa4s31ZxAk8vd43mhTeF2fnyRRYLy31jTjak00ZU0Wnb6_oeOMltt6z1mjMAc9rwwg8OTVyH2SZUg2cVI0ELxVLcvlp68fgpJYiFM3v7-exD8lEO5mbL_m7Dv-3LdVMTpne4sq6BT8ybgdyBAtMsAYyLpSy49Hxwa65QZnPYs8rFOjXLI--9jMYveWEIHMohatoNRshoDs0EaQBXJLOLNcEE9wkAtO7U6IWSte_7ncYxO7ah_3Nx-eiOkSJacEAOntvmJMmeSqI0yeai5sNYarnRqgM_9qIHOo9dpoK73kiLRPBkFk5jQf59Jw7cu3zhAWlH6dSBZFsjKBmVyxJFt9vOq0CBPHXuG32RVD2P8L0-cFkDl6GaTh6zZ6ceK6IWYCPAd7mnEGoIjYhep4WQfPEGwwVIK4xnQz4Rv3nymVmTM6SgwqMgHIAw3YuNM-shffviPvlUJYtbj0B3sMh55KCZkUu-_knoi_8JcovoFV1z87jAU_pU1UD42aKdR_29wUFCcZvJ1XM3ANgNbpAWQtWyWxOhEEUo7o5L7C3VzVZCJiRcb2LOQC_Au5Hbc5DVjUp-"

news_collector = SingleNewsCollector()
news = news_collector.collect_single_news(url)
print(news)
