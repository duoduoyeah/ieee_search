from ieee_search.core.xploreapi import XPLORE
import os
from dotenv import load_dotenv

load_dotenv()

query = XPLORE(os.getenv('IEEE_API_KEY'))

query.setDataFormat('object')

query.abstractText('query')
data = query.callAPI()
print(data)