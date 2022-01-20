import datetime
from collections import defaultdict
from typing import Text

import pandas as pd
import requests
import streamlit as st

RATE_LIMIT_COUNT = 100
MAX_PAGES = 20

session = requests.Session()

@st.cache(show_spinner=False, ttl=3600.0)
def fetch(url: Text):
    r = session.get(url)
    r.raise_for_status()
    return r.json()

def main():
    st.set_page_config(page_title="Bybit Funding Rate History", page_icon="📊")
    st.title("📊 Bybit Funding Rate History")
    contract_type =  st.sidebar.selectbox("契約タイプ", ["-", "インバース無期限", "USDT無期限"])
    if contract_type == "-":
        st.write("BybitからFunding Rateを取得してグラフを表示するWebアプリです。")
        st.caption("このWebアプリは「Streamlit」ライブラリの技術デモです。🎈")

        st.header("✨ 機能", "features")
        st.write("\n".join(
            [
                "- インバース無期限 / USDT無期限 の銘柄のFRをグラフで表示できます。",
                "- 銘柄を自動で取得するので、最新の銘柄もチェックできます。",
                "- 複数の銘柄をリストから選択して比較できます。",
            ]
        ))
        st.image("images/Web キャプチャ_20-1-2022_16619_192.168.32.156.jpeg")

        st.header("使い方", "usage")
        st.write("\n".join(
            [
                "1. サイドバーから「契約タイプ」を選択してください。",
                "1. サイドバーに「シンボル名」が表示されるのでリストから銘柄を選択してください。複数選択することもできます。",
                "1. FRの時間軸を増やしたい場合は、「取得ページ数」を増やしてください。1ページごとに20件(8H x 20 = 160H)増えます。",
                "1. FRの時間軸はUTC時間です。日本時間で表示したい場合は、「JSTに変換」をチェックしてください。",
                "1. 表示が狭いと感じる場合は、右上のメニューアイコンから Settings > Wide mode をオンにしてみてください。",
            ]
        ))

        st.header("注意事項", "important")
        st.write("Bybit側の負荷軽減の為、このアプリの動作に以下の制限を設けています。")
        st.write("\n".join(
            [
                "1. このアプリが取得したFRデータと銘柄一覧は1時間サーバー上にキャッシュされます。その為、最大1時間情報が更新されません。その場合は暫く経ってからまたアクセスしてください。",
                f"1. 「取得ページ数」の最大は{MAX_PAGES}ページまでに制限しています。",
                f"1. 銘柄数 x ページ数 が{RATE_LIMIT_COUNT}ページを超える場合は、リクエストに制限を掛けて遅くしています。",
                f"1. (課題) これはキャッシュ済みのデータも加算されます。例えば110ページ中、キャッシュ済みが80ページ、未キャッシュが30ページであっても、30ページのリクエストには制限が掛かかってしまいます。",
            ]
        ))
        st.caption("\n".join(
            [
                "- このWebアプリは、本アプリのサーバーが代理でBybitのサーバーからFRを取得しています。(お使いのブラウザが取得している訳ではありません)",
                "- したがって、本アプリの利用者が増えた場合は、Bybitのサーバーの制限(HTTP 403)でFRが取得できなくなる可能性があります。",
                "- そのような場合は、本アプリの公開を終了するかもしれません。他の利用者による制限なく利用したい、またはページ数上限とレート制限を解除したい場合は、ソースコードを取得してご自身の環境でアプリを実行することをおすすめします。",
            ]
        ))
        st.write("以下のようなHTTPエラーが発生した場合は、更新したりせず暫く本アプリを利用を控えてください。")
        st.error("(例) HTTPError: 403 Client Error: FORBIDDEN for url: https:// ...")

        st.header("🎈 Streamlit")
        st.write("  \n".join(
            [
                "このWebアプリは「Streamlit」ライブラリで作成されています。なんと、100% Pythonコードです🐍。Streamlit Cloudにデプロイされ稼働しています(無料)。",
                "このようなWebアプリを作りたいと思った方は、ページ下部の「Made with Streamlit」にアクセスしてみてください！",
            ]
        ))

        st.header("💖 Author")
        st.write("要望や改善はTwitterにリプかDMを、またはGitHubリポジトリにIssueをください。")
        st.write("  \n".join(
            [
                "Twitter (Follow me 😋)",
                "https://twitter.com/MtkN1XBt",
            ]
        ))
        st.write("  \n".join(
            [
                "lit.link",
                "https://lit.link/MtkN1",
            ]
        ))
        st.write("  \n".join(
            [
                "ソースコード",
                "https://github.com/MtkN1/streamlit-bybit-fr",
            ]
        ))
    else:
        with st.spinner("シンボル取得中..."):
            data = fetch("https://api2.bybit.com/v3/private/instrument/dynamic-symbol")
        if contract_type == "インバース無期限":
            target_symbols = data["result"]["InversePerpetual"]
        elif contract_type == "USDT無期限":
            target_symbols = data["result"]["LinearPerpetual"]
        # elif contract_type == "インバース先物":
        #     target_symbols = data["result"]["InverseFutures"]
        else:
            raise ValueError(contract_type)

        symbols =  st.sidebar.multiselect("シンボル名（複数選択可）", [x["symbolName"] for x in target_symbols])
        count = st.sidebar.slider("取得ページ数（1ページ＝20件）", min_value=1, max_value=MAX_PAGES, value=5, step=1)
        to_jst = st.sidebar.checkbox("JSTに変換")

        if not symbols:
            st.write("サイドバーの「シンボル名」から銘柄を選択してください。")
        else:
            urls = []
            for symbol in symbols:
                if contract_type == "インバース無期限":
                    urls.extend([f"https://api2.bybit.com/funding-rate/list?symbol={symbol}&date=&export=false&page={i + 1}" for i in range(int(count))])
                elif contract_type == "USDT無期限":
                    urls.extend([f"https://api2.bybit.com/linear/funding-rate/list?symbol={symbol}&date=&export=false&page={i + 1}" for i in range(int(count))])
            result = []
            if len(urls) <= RATE_LIMIT_COUNT:
                session.headers["User-Agent"] = f"Streamlit/{st.__version__}"
            with st.spinner(f'FR取得中...{len(urls)}ページ {"" if len(urls) <= RATE_LIMIT_COUNT else "(レート制限あり)"}'): 
                my_bar = st.progress(0.0)
                for i, url in enumerate(urls):
                    result.append(fetch(url))
                    my_bar.progress((i + 1) / len(urls))
                my_bar.empty()
            fr_hist = defaultdict(dict)
            for data in result:
                for item in data["result"]["data"]:
                    if isinstance(item["symbol"], str):
                        s = next(filter(lambda x: x["symbolName"] == item["symbol"], target_symbols))
                    elif isinstance(item["symbol"], int):
                        s = next(filter(lambda x: x["symbol"] == item["symbol"], target_symbols))
                    else:
                        raise ValueError(item)
                    if contract_type == "インバース無期限":
                        t = item["time"][:-1]
                    elif contract_type == "USDT無期限":
                        t = item["time"]
                    if to_jst:
                        dt = datetime.datetime.fromisoformat(f"{t}+00:00").astimezone(datetime.timezone(datetime.timedelta(hours=9)))
                    else:
                        dt = datetime.datetime.fromisoformat(t)
                    fr_hist[s["symbolName"]][dt] = float(item["value"]) * 1000
            df = pd.DataFrame(fr_hist)
            st.line_chart(df)
            st.caption("DataFrame")
            st.dataframe(df)

if __name__ == "__main__":
    main()
