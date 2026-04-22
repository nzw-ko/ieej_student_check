def check_all_links():
    found_urls = []
    
    for i in range(1, 32):
        day = str(i).zfill(2)
        url = BASE_URL.format(day=day)
        
        try:
            time.sleep(0.5)
            # allow_redirects=False にすることで、別のページへ飛ばされるのを阻止します
            response = requests.head(url, allow_redirects=False, timeout=5)
            
            # ステータスコードが「200」の時だけ、そのページ自体が存在するとみなす
            # リダイレクト（301, 302）される場合は無視されます
            if response.status_code == 200:
                print(f"MATCH: {url}")
                found_urls.append(url)
            else:
                # 301や302が返ってきた場合は「まだ準備中（リダイレクト）」と判断
                print(f"Skipped ({day}): Status {response.status_code}")
                
        except Exception as e:
            print(f"Error checking {day}: {e}")

    if found_urls:
        send_email(found_urls)
