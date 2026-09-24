import os
import sys
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SCREENS = [
    {
        "id": "903771441b7346819d9bbea7602aaece",
        "title": "paimana_ai_logo",
        "screenshot_url": "https://lh3.googleusercontent.com/aida/AEtjO1VdS0syX5CoLfxuqhoJrr0tnSVxvTErdir1MpyeimvBzTLlYL47NwaaupSvY94iTRPL3SErhpomqfCURRIfSayDwUafMy7XTeIJd5mSlCl2dxAuY-iRztg5-4PagKXdT52LMml6E0zItJp90KrA1MHI86QxliDiW_BItEgaQjM2ShobAuv91YhOoFSLhZ0Y_1XNwEoHAwNm0hHmKp3U7qO-1epNuiUFPIqq46mBM2DvW4I-6NBujV-WRxc",
        "html_url": None
    },
    {
        "id": "574d64bc2d834f45a45017acacf38bfd",
        "title": "model_comparison_v1",
        "screenshot_url": "https://lh3.googleusercontent.com/aida/AEtjO1Wr3dWNKsxQM87MREUWDoPXzMmqf5_6ggLNuX2V5MserZF8hH7N3nnDyhCzMVspP0QGplzsq1-dA528sHmZhlNxa49fZQVoIlHb3tBwChrKQko12b_xKj88f9CIcc348myiVLNISwbj7o8_gNlWNDQ27QK4gi-zXodats_7R8RyZawJ0Zu4ozR1XlQiC_p42LAZc1NSUSM4rCdeFokv3H7FmcmJgXkYTSr3ZV0c2nZWSFNAgpK6heo8pmU",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzAwMDY1OWRmNGY4ZmE0NzkwMDMwMTE0Yzk1MjhjM2FlEgsSBxDJu9-3pBkYAZIBIwoKcHJvamVjdF9pZBIVQhMyNDM5MjUyNTY2NjA3MzIwOTIx&filename=&opi=89354086"
    },
    {
        "id": "86cfc4b1388f4c2580b2c419f22f3e65",
        "title": "portfolio_overview_v2",
        "screenshot_url": "https://lh3.googleusercontent.com/aida/AEtjO1VLgViSVfuKULUyTYa0NzZDbqFzVs3tD1Xo-vf-t-uUgs3nZnfZ5AKoZdPKeIH91Ql1rcJyNF8kaoPzQyyoUDbQHD4wgzhLvjkfRJdwsRrQh83qiSD1ObJf1t94pOOYaOk8PbWZABSJfXC5sCBHggyaTHskgno4hi7inDXt-yffd1mMktRXKa0HVs5r0yR9WOmJagkpaeXGSzZiI4ouHEBiFMNP1WfDlqY7QI1W2_lArIzI5qqhJs9x300",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzAwMDY1OWRmNGZkNmZlOTcwMzM4NGIyM2NlMjQ3YjNlEgsSBxDJu9-3pBkYAZIBIwoKcHJvamVjdF9pZBIVQhMyNDM5MjUyNTY2NjA3MzIwOTIx&filename=&opi=89354086"
    },
    {
        "id": "6966d8f00c6e4bf98d87bef5d4370cdb",
        "title": "project_explorer_v2",
        "screenshot_url": "https://lh3.googleusercontent.com/aida/AEtjO1VuzXXK8_kQt7AR2wqxqPZO2OUwrp5b8Fws111kGBFs6v1BU-O4pf5UJaze2PxE7iZTkTbmkjAQtPOBef9XXSnaUysQp1BFCMjTeQNImc3ov0B91ka28eaa0e6hDpn51alvzyubqzMtgcEmNYAsHyMLdLFq3vuIxnR23NRj2l1xyWyRBP_s990qZO9Uj7C87LeMLz2D4-2SnI9UViUAgu-_AuO8F2ASKYBQTZMygfjKcf3BvX5Qz1IZMKY",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzAwMDY1OWRmNGZhZmQ5ODgwNzNhYzk4ZWYwMzkyN2YzEgsSBxDJu9-3pBkYAZIBIwoKcHJvamVjdF9pZBIVQhMyNDM5MjUyNTY2NjA3MzIwOTIx&filename=&opi=89354086"
    },
    {
        "id": "b48d8b6dfb44453b96a82e29683754a1",
        "title": "project_detail_view_v2",
        "screenshot_url": "https://lh3.googleusercontent.com/aida/AEtjO1V72C5zcytp1MGmtgqZvGPqOHm_A1poJkpr-DzDaerFWHIJlhzcWk0e2oM5ngQpfdsy4ucu15VyTaTHy-AuE8KLyhJQccFmQvS5CiZYnbuxxrq1CeOc9Wq7JgfW0zBpGyJeBnhg77OABMvj3yd7Th43Ude4Z0h40klEzGdMHYFqxSn0Vh68xKAH4m2Tttl0BkZMMACVxL2CmOtYRhWoECz4tuQbmPmKc5tUP799vxa9OkEzDX7ThJe86GI",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzAwMDY1OWRmNGZiYWVkZWQwN2M0ZWU1ZWZlMTc0ZGYwEgsSBxDJu9-3pBkYAZIBIwoKcHJvamVjdF9pZBIVQhMyNDM5MjUyNTY2NjA3MzIwOTIx&filename=&opi=89354086"
    },
    {
        "id": "f6381b95bdff40b18157e4b5ad410cee",
        "title": "early_warning_alerts_v2",
        "screenshot_url": "https://lh3.googleusercontent.com/aida/AEtjO1Ujn81oPovl4HdxyBBZGiLsrEFbdY8k0sKRrT38dyQpjY-CVs4cXStt9w7IOHp4ueptMAeT5ZlrPlnQ3hQsMfnnVCtV_W6KUUVR9ndi2tsCyY0FFqODMwWxW8M50CX9N-KD2CZxxYW9t2E0xvXD_rPTB2wdW0Ywqho-mV6ZdfsILVXHRK3CLJjOX9ldfchIodbjtxT28G9s2uHflw34QoWchkaRj48Y-pltntelHYwl8ijCiIBqUzn9Dg",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzAwMDY1OWRmNGZjY2M3NjEwMzMyY2UwNDBlMjhkNGY3EgsSBxDJu9-3pBkYAZIBIwoKcHJvamVjdF9pZBIVQhMyNDM5MjUyNTY2NjA3MzIwOTIx&filename=&opi=89354086"
    },
    {
        "id": "f8144a4631a044daba12a264a62d712c",
        "title": "model_comparison_v2",
        "screenshot_url": "https://lh3.googleusercontent.com/aida/AEtjO1W9B3csANeELoeW-r99wQKw-YJiVo0ZlG18cVD775Unjz5f23HGTc2wSFQg5SEGnUWizpcH-u4egFymssF0zkOSP9XZ0Ed1XI_cA80oqgY-sysTblpoa65MHI4IGl00yrI-uliOwDrhc7x3U9jWYML_NksNs-w4AWqZVUdtzEgbLWaUxSqUp6L5Q7ZxFnZOVJWzs8id2WcolpjGyZgqZ-gA4kAI7T2SWJVG9qZb5DW6s77PpjIkQUhh0d4",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzAwMDY1OWRmNGZhNmM5MDAwMzM4NGIyM2NlMjQ3YjNlEgsSBxDJu9-3pBkYAZIBIwoKcHJvamVjdF9pZBIVQhMyNDM5MjUyNTY2NjA3MzIwOTIx&filename=&opi=89354086"
    }
]

def download_all():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "stitch_assets"))
    img_dir = os.path.join(base_dir, "images")
    html_dir = os.path.join(base_dir, "html")
    
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)

    headers = {'User-Agent': 'Mozilla/5.0'}

    print("=" * 60)
    print("DOWNLOADING STITCH SCREEN ASSETS & CODE")
    print("=" * 60)

    for screen in SCREENS:
        sid = screen["id"]
        title = screen["title"]
        
        # 1. Download Screenshot Image
        if screen["screenshot_url"]:
            img_path = os.path.join(img_dir, f"{title}_{sid}.png")
            print(f"Downloading image: {title} ({sid})...")
            try:
                req = urllib.request.Request(screen["screenshot_url"], headers=headers)
                with urllib.request.urlopen(req) as resp, open(img_path, 'wb') as out_f:
                    out_f.write(resp.read())
                print(f"  ✓ Saved image to: {img_path}")
            except Exception as e:
                print(f"  ✗ Failed to download image {sid}: {e}")

        # 2. Download HTML Code
        if screen["html_url"]:
            html_path = os.path.join(html_dir, f"{title}_{sid}.html")
            print(f"Downloading HTML: {title} ({sid})...")
            try:
                req = urllib.request.Request(screen["html_url"], headers=headers)
                with urllib.request.urlopen(req) as resp, open(html_path, 'wb') as out_f:
                    out_f.write(resp.read())
                print(f"  ✓ Saved HTML to: {html_path}")
            except Exception as e:
                print(f"  ✗ Failed to download HTML {sid}: {e}")

    print("=" * 60)
    print("All Stitch assets downloaded successfully!")
    print(f"Directory: {base_dir}")
    print("=" * 60)

if __name__ == "__main__":
    download_all()
