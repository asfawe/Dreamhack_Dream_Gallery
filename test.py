url = " http://example.com/?url=file:///etc/passwd%00/flag.txt"

if url.startswith("file://") or "flag" in url:
    print("hello")
