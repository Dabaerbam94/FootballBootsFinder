import requests
from urllib.parse import quote
import streamlit as st

st.title("Football Boots Price Finder (eBay UK)")

search_query = st.text_input("Enter the product you're searching for", "football boots")
max_results = st.slider("Number of results", 5, 50, 10)

if st.button("Search"):
    if not EBAY_APP_ID or EBAY_APP_ID == 'KevinMan-Football-PRD-980a4d7cf-46471df2':
        st.error("Please configure your eBay App ID in the code.")
    else:
        sort_order = "PricePlusShippingLowest"

        url = (
            f"https://svcs.ebay.com/services/search/FindingService/v1"
            f"?OPERATION-NAME=findItemsByKeywords"
            f"&SERVICE-VERSION=1.0.0"
            f"&SECURITY-APPNAME={KevinMan-Football-PRD-980a4d7cf-46471df2}"
            f"&RESPONSE-DATA-FORMAT=JSON"
            f"&REST-PAYLOAD"
            f"&keywords={quote(search_query)}"
            f"&paginationInput.entriesPerPage={max_results}"
            f"&sortOrder={sort_order}"
            f"&GLOBAL-ID=EBAY-GB"
        )

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            items = data['findItemsByKeywordsResponse'][0]['searchResult'][0].get('item', [])

            if items:
                for item in items:
                    title = item['title'][0]
                    price = item['sellingStatus'][0]['convertedCurrentPrice'][0]['__value__']
                    link = item['viewItemURL'][0]
                    st.markdown(f"### [{title}]({link})")
                    st.write(f"**Price:** £{price}")
            else:
                st.info("No items found for your search.")
        else:
            st.error("Failed to fetch data from eBay API.")
