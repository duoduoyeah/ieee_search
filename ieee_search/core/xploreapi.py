# modify by: Shiyuan Li
# Original code from: https://gist.github.com/paulosevero/10a82c44b86f166f546f1e462d79b63c


import math
import requests

from urllib.parse import quote
from urllib.request import urlopen

import xml.etree.ElementTree as ET
import json

class XPLORE:
    endPoint = "http://ieeexploreapi.ieee.org/api/v1/search/articles"
    openAccessEndPoint = "http://ieeexploreapi.ieee.org/api/v1/search/document/"    

    def __init__(self, apiKey):
    	# API key
        self.apiKey = apiKey

    	# flag that some search criteria has been provided
        self.queryProvided = False

        # flag for Open Access, which changes endpoint in use and limits results to just Open Access
        self.usingOpenAccess = False

        # flag that article number has been provided, which overrides all other search criteria
        self.usingArticleNumber = False

        # flag that a boolean method is in use
        self.usingBoolean = False

        # flag that a facet is in use
        self.usingFacet = False

        # flag that a facet has been applied, in the event that multiple facets are passed
        self.facetApplied = False 

        # data type for results; default is json (other option is xml)
        self.outputType = 'json'

        # data format for results; default is raw (returned string); other option is object
        self.outputDataFormat = 'raw'

        # default of 25 results returned
        self.resultSetMax = 25

        # maximum of 200 results returned
        self.resultSetMaxCap = 200

        # records returned default to position 1 in result set
        self.startRecord = 1

        # default sort order is ascending; could also be 'desc' for descending
        self.sortOrder = 'asc'

        # field name that is being used for sorting
        self.sortField = 'article_title'

        # array of permitted search fields for searchField() method
        self.allowedSearchFields = ['abstract', 'affiliation', 'article_number', 'article_title', 'author', 'boolean_text', 'content_type', 'd-au', 'd-pubtype', 'd-publisher', 'd-year', 'doi', 'end_year', 'facet', 'index_terms', 'isbn', 'issn', 'is_number', 'meta_data', 'open_access', 'publication_number', 'publication_title', 'publication_year', 'publisher', 'querytext', 'start_year', 'thesaurus_terms']

        # dictionary of all search parameters in use and their values
        self.parameters = {}

        # dictionary of all filters in use and their values
        self.filters = {}

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


    def __ne__(self, other):
        return not self.__eq__(other)


    def dataType(self, outputType):

        outputType = outputType.strip().lower()
        self.outputType = outputType


    def setDataFormat(self, outputDataFormat: str):
        """
        available options: raw, object
        """
        outputDataFormat = outputDataFormat.strip().lower()
        self.outputDataFormat = outputDataFormat


    def startingResult(self, start):

        self.startRecord = math.ceil(start) if (start > 0) else 1


    def maximumResults(self, maximum):

        self.resultSetMax = math.ceil(maximum) if (maximum > 0) else 25
        if self.resultSetMax > self.resultSetMaxCap:
            self.resultSetMax = self.resultSetMaxCap


    def resultsFilter(self, filterParam, value):

        filterParam = filterParam.strip().lower()
        value = value.strip()

        if len(value) > 0:
            self.filters[filterParam] = value
            self.queryProvided = True

            if (filterParam == 'content_type' and value == 'Standards'):
                self.resultsSorting('publication_year', 'asc')


    def resultsSorting(self, field, order):

        field = field.strip().lower()
        order = order.strip()
        self.sortField = field
        self.sortOrder = order


    def searchField(self, field, value):

        field = field.strip().lower()
        if field in self.allowedSearchFields:
            self.addParameter(field, value)
        else:
            print("Searches against field " + field + " are not supported")


    def abstractText(self, value):

        self.addParameter('abstract', value)


    def affiliationText(self, value):

        self.addParameter('affiliation', value)


    def articleNumber(self, value):

        self.addParameter('article_number', value)


    def articleTitle(self, value):

        self.addParameter('article_title', value)


    def authorText(self, value):

        self.addParameter('author', value)


    def authorFacetText(self, value):

        self.addParameter('d-au', value)


    def booleanText(self, value):

        self.addParameter('boolean_text', value)


    def contentTypeFacetText(self, value):

        self.addParameter('d-pubtype', value)


    def doi(self, value):

        self.addParameter('doi', value)


    def facetText(self, value):

        self.addParameter('facet', value)


    def indexTerms(self, value):

        self.addParameter('index_terms', value)


    def isbn(self, value):

        self.addParameter('isbn', value)


    def issn(self, value):

        self.addParameter('issn', value)


    def issueNumber(self, value):

        self.addParameter('is_number', value)


    def metaDataText(self, value):

        self.addParameter('meta_data', value)


    def publicationFacetText(self, value):

        self.addParameter('d-year', value)


    def publisherFacetText(self, value):

        self.addParameter('d-publisher', value)


    def publicationTitle(self, value):

        self.addParameter('publication_title', value)


    def publicationYear(self, value):

        self.addParameter('publication_year', value)


    def queryText(self, value):

        self.addParameter('querytext', value)


    def thesaurusTerms(self, value):

        self.addParameter('thesaurus_terms', value)


    def addParameter(self, parameter, value):
      
        value = value.strip()

        if (len(value) > 0):

            self.parameters[parameter]= value
        
            self.queryProvided = True

            if (parameter == 'article_number'):
                self.usingArticleNumber = True

            if (parameter == 'boolean_text'):
                self.usingBoolean = True

            if (parameter == 'facet' or parameter == 'd-au' or parameter == 'd-year' or parameter == 'd-pubtype' or parameter == 'd-publisher'):
                self.usingFacet = True


    def openAccess(self, article):
      
        self.usingOpenAccess = True
        self.queryProvided = True
        self.articleNumber(article)


    def callAPI(self, debugModeOff=True):
        # if using open access, build open access query
        if self.usingOpenAccess is True:
            str = self.buildOpenAccessQuery()
        else:
            str = self.buildQuery()

        if debugModeOff is False:
            return str
        elif self.queryProvided is False:
                print("No search criteria provided")
        
        data = self.queryAPI(str)
        formattedData = self.formatData(data)
        return formattedData


    def buildOpenAccessQuery(self) -> str:

        url = self.openAccessEndPoint;
        url += str(self.parameters['article_number']) + '/fulltext'
        url += '?apikey=' + str(self.apiKey)
        url += '&format=' + str(self.outputType)

        return url


    def buildQuery(self):

        url = self.endPoint;

        url += '?apikey=' + str(self.apiKey)
        url += '&format=' + str(self.outputType)
        url += '&max_records=' + str(self.resultSetMax)
        url += '&start_record=' + str(self.startRecord)
        url += '&sort_order=' + str(self.sortOrder)
        url += '&sort_field=' + str(self.sortField)

        if (self.usingArticleNumber):
            url += '&article_number=' + str(self.parameters['article_number'])

        elif (self.usingBoolean):
             url += '&querytext=(' + quote(self.parameters['boolean_text']) + ')'

        else:
            for key in self.parameters:

                if (self.usingFacet and self.facetApplied is False):
                    url += '&querytext=' + quote(self.parameters[key]) + '&facet=' + key
                    self.facetApplied = True

                else:
                    url += '&' + key + '=' + quote(self.parameters[key])


        for key in self.filters:
            url += '&' + key + '=' + str(self.filters[key])
 
        return url


    def queryAPI(self, url):
        content = urlopen(url).read()

        return content


    def formatData(self, data):

        if self.outputDataFormat == 'raw':
            return data

        elif self.outputDataFormat == 'object':
            
            if self.outputType == 'xml':
                obj = ET.ElementTree(ET.fromstring(data))
                return obj

            else:
                obj = json.loads(data) 
                return obj

        else:
            return data
