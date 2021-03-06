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
    st.set_page_config(page_title="Bybit Funding Rate History", page_icon="ð")
    st.title("ð Bybit Funding Rate History")
    contract_type =  st.sidebar.selectbox("å¥ç´ã¿ã¤ã", ["-", "ã¤ã³ãã¼ã¹ç¡æé", "USDTç¡æé"])
    if contract_type == "-":
        st.write("BybitããFunding Rateãåå¾ãã¦ã°ã©ããè¡¨ç¤ºããWebã¢ããªã§ãã")
        st.caption("ãã®Webã¢ããªã¯ãStreamlitãã©ã¤ãã©ãªã®æè¡ãã¢ã§ããð")

        st.header("â¨ æ©è½", "features")
        st.write("\n".join(
            [
                "- ã¤ã³ãã¼ã¹ç¡æé / USDTç¡æé ã®éæã®FRãã°ã©ãã§è¡¨ç¤ºã§ãã¾ãã",
                "- éæãèªåã§åå¾ããã®ã§ãææ°ã®éæããã§ãã¯ã§ãã¾ãã",
                "- è¤æ°ã®éæããªã¹ãããé¸æãã¦æ¯è¼ã§ãã¾ãã",
            ]
        ))
        st.image("images/Web ã­ã£ããã£_20-1-2022_16619_192.168.32.156.jpeg")

        st.header("ä½¿ãæ¹", "usage")
        st.write("\n".join(
            [
                "1. ãµã¤ããã¼ãããå¥ç´ã¿ã¤ãããé¸æãã¦ãã ããã",
                "1. ãµã¤ããã¼ã«ãã·ã³ãã«åããè¡¨ç¤ºãããã®ã§ãªã¹ãããéæãé¸æãã¦ãã ãããè¤æ°é¸æãããã¨ãã§ãã¾ãã",
                "1. FRã®æéè»¸ãå¢ããããå ´åã¯ããåå¾ãã¼ã¸æ°ããå¢ããã¦ãã ããã1ãã¼ã¸ãã¨ã«20ä»¶(8H x 20 = 160H)å¢ãã¾ãã",
                "1. FRã®æéè»¸ã¯UTCæéã§ããæ¥æ¬æéã§è¡¨ç¤ºãããå ´åã¯ããJSTã«å¤æãããã§ãã¯ãã¦ãã ããã",
                "1. è¡¨ç¤ºãç­ãã¨æããå ´åã¯ãå³ä¸ã®ã¡ãã¥ã¼ã¢ã¤ã³ã³ãã Settings > Wide mode ããªã³ã«ãã¦ã¿ã¦ãã ããã",
            ]
        ))

        st.header("æ³¨æäºé ", "important")
        st.write("Bybitå´ã®è² è·è»½æ¸ã®çºããã®ã¢ããªã®åä½ã«ä»¥ä¸ã®å¶éãè¨­ãã¦ãã¾ãã")
        st.write("\n".join(
            [
                "1. ãã®ã¢ããªãåå¾ããFRãã¼ã¿ã¨éæä¸è¦§ã¯1æéãµã¼ãã¼ä¸ã«ã­ã£ãã·ã¥ããã¾ãããã®çºãæå¤§1æéæå ±ãæ´æ°ããã¾ããããã®å ´åã¯æ«ãçµã£ã¦ããã¾ãã¢ã¯ã»ã¹ãã¦ãã ããã",
                f"1. ãåå¾ãã¼ã¸æ°ãã®æå¤§ã¯{MAX_PAGES}ãã¼ã¸ã¾ã§ã«å¶éãã¦ãã¾ãã",
                f"1. éææ° x ãã¼ã¸æ° ã{RATE_LIMIT_COUNT}ãã¼ã¸ãè¶ããå ´åã¯ããªã¯ã¨ã¹ãã«å¶éãæãã¦éããã¦ãã¾ãã",
                f"1. (èª²é¡) ããã¯ã­ã£ãã·ã¥æ¸ã¿ã®ãã¼ã¿ãå ç®ããã¾ããä¾ãã°110ãã¼ã¸ä¸­ãã­ã£ãã·ã¥æ¸ã¿ã80ãã¼ã¸ãæªã­ã£ãã·ã¥ã30ãã¼ã¸ã§ãã£ã¦ãã30ãã¼ã¸ã®ãªã¯ã¨ã¹ãã«ã¯å¶éãæããã£ã¦ãã¾ãã¾ãã",
            ]
        ))
        st.caption("\n".join(
            [
                "- ãã®Webã¢ããªã¯ãæ¬ã¢ããªã®ãµã¼ãã¼ãä»£çã§Bybitã®ãµã¼ãã¼ããFRãåå¾ãã¦ãã¾ãã(ãä½¿ãã®ãã©ã¦ã¶ãåå¾ãã¦ããè¨³ã§ã¯ããã¾ãã)",
                "- ãããã£ã¦ãæ¬ã¢ããªã®å©ç¨èãå¢ããå ´åã¯ãBybitã®ãµã¼ãã¼ã®å¶é(HTTP 403)ã§FRãåå¾ã§ããªããªãå¯è½æ§ãããã¾ãã",
                "- ãã®ãããªå ´åã¯ãæ¬ã¢ããªã®å¬éãçµäºããããããã¾ãããä»ã®å©ç¨èã«ããå¶éãªãå©ç¨ããããã¾ãã¯ãã¼ã¸æ°ä¸éã¨ã¬ã¼ãå¶éãè§£é¤ãããå ´åã¯ãã½ã¼ã¹ã³ã¼ããåå¾ãã¦ãèªèº«ã®ç°å¢ã§ã¢ããªãå®è¡ãããã¨ããããããã¾ãã",
            ]
        ))
        st.write("ä»¥ä¸ã®ãããªHTTPã¨ã©ã¼ãçºçããå ´åã¯ãæ´æ°ãããããæ«ãæ¬ã¢ããªãå©ç¨ãæ§ãã¦ãã ããã")
        st.error("(ä¾) HTTPError: 403 Client Error: FORBIDDEN for url: https:// ...")

        st.header("ð Streamlit")
        st.write("  \n".join(
            [
                "ãã®Webã¢ããªã¯ãStreamlitãã©ã¤ãã©ãªã§ä½æããã¦ãã¾ãããªãã¨ã100% Pythonã³ã¼ãã§ãðãStreamlit Cloudã«ããã­ã¤ããç¨¼åãã¦ãã¾ã(ç¡æ)ã",
                "ãã®ãããªWebã¢ããªãä½ãããã¨æã£ãæ¹ã¯ããã¼ã¸ä¸é¨ã®ãMade with Streamlitãã«ã¢ã¯ã»ã¹ãã¦ã¿ã¦ãã ããï¼",
            ]
        ))

        st.header("ð Author")
        st.write("è¦æãæ¹åã¯Twitterã«ãªããDMããã¾ãã¯GitHubãªãã¸ããªã«Issueããã ããã")
        st.write("  \n".join(
            [
                "Twitter (Follow me ð)",
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
                "ã½ã¼ã¹ã³ã¼ã",
                "https://github.com/MtkN1/streamlit-bybit-fr",
            ]
        ))
    else:
        with st.spinner("ã·ã³ãã«åå¾ä¸­..."):
            data = fetch("https://api2.bybit.com/v3/private/instrument/dynamic-symbol")
        if contract_type == "ã¤ã³ãã¼ã¹ç¡æé":
            target_symbols = data["result"]["InversePerpetual"]
        elif contract_type == "USDTç¡æé":
            target_symbols = data["result"]["LinearPerpetual"]
        # elif contract_type == "ã¤ã³ãã¼ã¹åç©":
        #     target_symbols = data["result"]["InverseFutures"]
        else:
            raise ValueError(contract_type)

        symbols =  st.sidebar.multiselect("ã·ã³ãã«åï¼è¤æ°é¸æå¯ï¼", [x["symbolName"] for x in target_symbols])
        count = st.sidebar.slider("åå¾ãã¼ã¸æ°ï¼1ãã¼ã¸ï¼20ä»¶ï¼", min_value=1, max_value=MAX_PAGES, value=5, step=1)
        to_jst = st.sidebar.checkbox("JSTã«å¤æ")

        if not symbols:
            st.write("ãµã¤ããã¼ã®ãã·ã³ãã«åãããéæãé¸æãã¦ãã ããã")
        else:
            urls = []
            for symbol in symbols:
                if contract_type == "ã¤ã³ãã¼ã¹ç¡æé":
                    urls.extend([f"https://api2.bybit.com/funding-rate/list?symbol={symbol}&date=&export=false&page={i + 1}" for i in range(int(count))])
                elif contract_type == "USDTç¡æé":
                    urls.extend([f"https://api2.bybit.com/linear/funding-rate/list?symbol={symbol}&date=&export=false&page={i + 1}" for i in range(int(count))])
            result = []
            if len(urls) <= RATE_LIMIT_COUNT:
                session.headers["User-Agent"] = f"Streamlit/{st.__version__}"
            with st.spinner(f'FRåå¾ä¸­...{len(urls)}ãã¼ã¸ {"" if len(urls) <= RATE_LIMIT_COUNT else "(ã¬ã¼ãå¶éãã)"}'): 
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
                    if contract_type == "ã¤ã³ãã¼ã¹ç¡æé":
                        t = item["time"][:-1]
                    elif contract_type == "USDTç¡æé":
                        t = item["time"]
                    if to_jst:
                        dt = datetime.datetime.fromisoformat(f"{t}+00:00").astimezone(datetime.timezone(datetime.timedelta(hours=9)))
                    else:
                        dt = datetime.datetime.fromisoformat(t)
                    fr_hist[s["symbolName"]][dt] = float(item["value"]) * 100
            df = pd.DataFrame(fr_hist)
            st.line_chart(df)
            st.caption("DataFrame")
            st.dataframe(df.sort_index(ascending=False))

if __name__ == "__main__":
    main()
