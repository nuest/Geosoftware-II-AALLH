#Authors: Aysel Tandik, Anika Graupner 
import os
import sys
import cgi
from six.moves.urllib.parse import quote, unquote
from six import StringIO
from six.moves.configparser import SafeConfigParser
from pycsw.core.etree import etree
from pycsw import oaipmh, opensearch, sru
from pycsw.ogc.csw.cql import cql2fes1
from pycsw.plugins.profiles import profile as pprofile
import pycsw.plugins.outputschemas
from pycsw.core import config, log, metadata, util
from pycsw.core.formats.fmt_json import xml2dict
from pycsw.ogc.fes import fes1
import logging

LOGGER = logging.getLogger(__name__)

class Api(object):
    ''' Api server '''
    def __init__(self, server_api):
        ''' Initialize Api '''

        self.parent = server_api

    def getcapabilities(self):
        ''' Handle GetCapabilities request '''
        serviceidentification = True
        serviceprovider = True
        operationsmetadata = True
        if 'sections' in self.parent.kvp:
            serviceidentification = False
            serviceprovider = False
            operationsmetadata = False
            for section in self.parent.kvp['sections'].split(','):
                if section == 'ServiceIdentification':
                    serviceidentification = True
                if section == 'ServiceProvider':
                    serviceprovider = True
                if section == 'OperationsMetadata':
                    operationsmetadata = True

        # check extra parameters that may be def'd by profiles
        if self.parent.profiles is not None:
            for prof in self.parent.profiles['loaded'].keys():
                result = \
                self.parent.profiles['loaded'][prof].check_parameters(self.parent.kvp)
                if result is not None:
                    return self.exceptionreport(result['code'],
                    result['locator'], result['text'])

        # @updateSequence: get latest update to repository
        try:
            updatesequence = \
            util.get_time_iso2unix(self.parent.repository.query_insert())
        except:
            updatesequence = None

        node = etree.Element(util.nspath_eval('csw:Capabilities',
        self.parent.context.namespaces),
        nsmap=self.parent.context.namespaces, version='2.0.2',
        updateSequence=str(updatesequence))

        if 'updatesequence' in self.parent.kvp:
            if int(self.parent.kvp['updatesequence']) == updatesequence:
                return node
            elif int(self.parent.kvp['updatesequence']) > updatesequence:
                return self.exceptionreport('InvalidUpdateSequence',
                'updatesequence',
                'outputsequence specified (%s) is higher than server\'s \
                updatesequence (%s)' % (self.parent.kvp['updatesequence'],
                updatesequence))

        node.attrib[util.nspath_eval('xsi:schemaLocation',
        self.parent.context.namespaces)] = '%s %s/csw/2.0.2/CSW-discovery.xsd' % \
        (self.parent.context.namespaces['csw'],
         self.parent.config.get('server', 'ogc_schemas_base'))

        metadata_main = dict(self.parent.config.items('metadata:main'))

        if serviceidentification:
            LOGGER.info('Writing section ServiceIdentification')

            serviceidentification = etree.SubElement(node, \
            util.nspath_eval('ows:ServiceIdentification',
            self.parent.context.namespaces))

            etree.SubElement(serviceidentification,
            util.nspath_eval('ows:Title', self.parent.context.namespaces)).text = \
            metadata_main.get('identification_title', 'missing')

            etree.SubElement(serviceidentification,
            util.nspath_eval('ows:Abstract', self.parent.context.namespaces)).text = \
            metadata_main.get('identification_abstract', 'missing')

            keywords = etree.SubElement(serviceidentification,
            util.nspath_eval('ows:Keywords', self.parent.context.namespaces))

            for k in \
            metadata_main.get('identification_keywords').split(','):
                etree.SubElement(
                keywords, util.nspath_eval('ows:Keyword',
                self.parent.context.namespaces)).text = k

            etree.SubElement(keywords,
            util.nspath_eval('ows:Type', self.parent.context.namespaces),
            codeSpace='ISOTC211/19115').text = \
            metadata_main.get('identification_keywords_type', 'missing')

            etree.SubElement(serviceidentification,
            util.nspath_eval('ows:ServiceType', self.parent.context.namespaces),
            codeSpace='OGC').text = 'CSW'

            for stv in self.parent.context.model['parameters']['version']['values']:
                etree.SubElement(serviceidentification,
                util.nspath_eval('ows:ServiceTypeVersion',
                self.parent.context.namespaces)).text = stv

            etree.SubElement(serviceidentification,
            util.nspath_eval('ows:Fees', self.parent.context.namespaces)).text = \
            metadata_main.get('identification_fees', 'missing')

            etree.SubElement(serviceidentification,
            util.nspath_eval('ows:AccessConstraints',
            self.parent.context.namespaces)).text = \
            metadata_main.get('identification_accessconstraints', 'missing')

        if serviceprovider:
            LOGGER.info('Writing section ServiceProvider')
            serviceprovider = etree.SubElement(node,
            util.nspath_eval('ows:ServiceProvider', self.parent.context.namespaces))

            etree.SubElement(serviceprovider,
            util.nspath_eval('ows:ProviderName', self.parent.context.namespaces)).text = \
            metadata_main.get('provider_name', 'missing')

            providersite = etree.SubElement(serviceprovider,
            util.nspath_eval('ows:ProviderSite', self.parent.context.namespaces))

            providersite.attrib[util.nspath_eval('xlink:type',
            self.parent.context.namespaces)] = 'simple'

            providersite.attrib[util.nspath_eval('xlink:href',
            self.parent.context.namespaces)] = \
            metadata_main.get('provider_url', 'missing')

            servicecontact = etree.SubElement(serviceprovider,
            util.nspath_eval('ows:ServiceContact', self.parent.context.namespaces))

            etree.SubElement(servicecontact,
            util.nspath_eval('ows:IndividualName',
            self.parent.context.namespaces)).text = \
            metadata_main.get('contact_name', 'missing')

            etree.SubElement(servicecontact,
            util.nspath_eval('ows:PositionName',
            self.parent.context.namespaces)).text = \
            metadata_main.get('contact_position', 'missing')

            contactinfo = etree.SubElement(servicecontact,
            util.nspath_eval('ows:ContactInfo', self.parent.context.namespaces))

            phone = etree.SubElement(contactinfo, util.nspath_eval('ows:Phone',
            self.parent.context.namespaces))

            etree.SubElement(phone, util.nspath_eval('ows:Voice',
            self.parent.context.namespaces)).text = \
            metadata_main.get('contact_phone', 'missing')

            etree.SubElement(phone, util.nspath_eval('ows:Facsimile',
            self.parent.context.namespaces)).text = \
            metadata_main.get('contact_fax', 'missing')

            address = etree.SubElement(contactinfo,
            util.nspath_eval('ows:Address', self.parent.context.namespaces))

            etree.SubElement(address,
            util.nspath_eval('ows:DeliveryPoint',
            self.parent.context.namespaces)).text = \
            metadata_main.get('contact_address', 'missing')

            etree.SubElement(address, util.nspath_eval('ows:City',
            self.parent.context.namespaces)).text = \
            metadata_main.get('contact_city', 'missing')

            etree.SubElement(address,
            util.nspath_eval('ows:AdministrativeArea',
            self.parent.context.namespaces)).text = \
            metadata_main.get('contact_stateorprovince', 'missing')

            etree.SubElement(address,
            util.nspath_eval('ows:PostalCode',
            self.parent.context.namespaces)).text = \
            metadata_main.get('contact_postalcode', 'missing')

            etree.SubElement(address,
            util.nspath_eval('ows:Country', self.parent.context.namespaces)).text = \
            metadata_main.get('contact_country', 'missing')

            etree.SubElement(address,
            util.nspath_eval('ows:ElectronicMailAddress',
            self.parent.context.namespaces)).text = \
            metadata_main.get('contact_email', 'missing')

            url = etree.SubElement(contactinfo,
            util.nspath_eval('ows:OnlineResource', self.parent.context.namespaces))

            url.attrib[util.nspath_eval('xlink:type',
            self.parent.context.namespaces)] = 'simple'

            url.attrib[util.nspath_eval('xlink:href',
            self.parent.context.namespaces)] = \
            metadata_main.get('contact_url', 'missing')

            etree.SubElement(contactinfo,
            util.nspath_eval('ows:HoursOfService',
            self.parent.context.namespaces)).text = \
            metadata_main.get('contact_hours', 'missing')

            etree.SubElement(contactinfo,
            util.nspath_eval('ows:ContactInstructions',
            self.parent.context.namespaces)).text = \
            metadata_main.get('contact_instructions', 'missing')

            etree.SubElement(servicecontact,
            util.nspath_eval('ows:Role', self.parent.context.namespaces),
            codeSpace='ISOTC211/19115').text = \
            metadata_main.get('contact_role', 'missing')

        if operationsmetadata:
            LOGGER.info('Writing section OperationsMetadata')
            operationsmetadata = etree.SubElement(node,
            util.nspath_eval('ows:OperationsMetadata',
            self.parent.context.namespaces))

            for operation in self.parent.context.model['operations_order']:
                oper = etree.SubElement(operationsmetadata,
                util.nspath_eval('ows:Operation', self.parent.context.namespaces),
                name=operation)

                dcp = etree.SubElement(oper, util.nspath_eval('ows:DCP',
                self.parent.context.namespaces))

                http = etree.SubElement(dcp, util.nspath_eval('ows:HTTP',
                self.parent.context.namespaces))

                if self.parent.context.model['operations'][operation]['methods']['get']:
                    get = etree.SubElement(http, util.nspath_eval('ows:Get',
                    self.parent.context.namespaces))

                    get.attrib[util.nspath_eval('xlink:type',\
                    self.parent.context.namespaces)] = 'simple'

                    get.attrib[util.nspath_eval('xlink:href',\
                    self.parent.context.namespaces)] = self.parent.config.get('server', 'url')

                if self.parent.context.model['operations'][operation]['methods']['post']:
                    post = etree.SubElement(http, util.nspath_eval('ows:Post',
                    self.parent.context.namespaces))
                    post.attrib[util.nspath_eval('xlink:type',
                    self.parent.context.namespaces)] = 'simple'
                    post.attrib[util.nspath_eval('xlink:href',
                    self.parent.context.namespaces)] = \
                    self.parent.config.get('server', 'url')

                for parameter in \
                sorted(self.parent.context.model['operations'][operation]['parameters']):
                    param = etree.SubElement(oper,
                    util.nspath_eval('ows:Parameter',
                    self.parent.context.namespaces), name=parameter)

                    for val in \
                    sorted(self.parent.context.model['operations'][operation]\
                    ['parameters'][parameter]['values']):
                        etree.SubElement(param,
                        util.nspath_eval('ows:Value',
                        self.parent.context.namespaces)).text = val

                if operation == 'GetRecords':  # advertise queryables
                    for qbl in sorted(self.parent.repository.queryables.keys()):
                        if qbl != '_all':
                            param = etree.SubElement(oper,
                            util.nspath_eval('ows:Constraint',
                            self.parent.context.namespaces), name=qbl)

                            for qbl2 in sorted(self.parent.repository.queryables[qbl]):
                                etree.SubElement(param,
                                util.nspath_eval('ows:Value',
                                self.parent.context.namespaces)).text = qbl2

                    if self.parent.profiles is not None:
                        for con in sorted(self.parent.context.model[\
                        'operations']['GetRecords']['constraints'].keys()):
                            param = etree.SubElement(oper,
                            util.nspath_eval('ows:Constraint',
                            self.parent.context.namespaces), name = con)
                            for val in self.parent.context.model['operations']\
                            ['GetRecords']['constraints'][con]['values']:
                                etree.SubElement(param,
                                util.nspath_eval('ows:Value',
                                self.parent.context.namespaces)).text = val

            for parameter in sorted(self.parent.context.model['parameters'].keys()):
                param = etree.SubElement(operationsmetadata,
                util.nspath_eval('ows:Parameter', self.parent.context.namespaces),
                name=parameter)

                for val in self.parent.context.model['parameters'][parameter]['values']:
                    etree.SubElement(param, util.nspath_eval('ows:Value',
                    self.parent.context.namespaces)).text = val

            for constraint in sorted(self.parent.context.model['constraints'].keys()):
                param = etree.SubElement(operationsmetadata,
                util.nspath_eval('ows:Constraint', self.parent.context.namespaces),
                name=constraint)

                for val in self.parent.context.model['constraints'][constraint]['values']:
                    etree.SubElement(param, util.nspath_eval('ows:Value',
                    self.parent.context.namespaces)).text = val

            if self.parent.profiles is not None:
                for prof in self.parent.profiles['loaded'].keys():
                    ecnode = \
                    self.parent.profiles['loaded'][prof].get_extendedcapabilities()
                    if ecnode is not None:
                        operationsmetadata.append(ecnode)

        # always write out Filter_Capabilities
        LOGGER.info('Writing section Filter_Capabilities')
        fltcaps = etree.SubElement(node,
        util.nspath_eval('ogc:Filter_Capabilities', self.parent.context.namespaces))

        spatialcaps = etree.SubElement(fltcaps,
        util.nspath_eval('ogc:Spatial_Capabilities', self.parent.context.namespaces))

        geomops = etree.SubElement(spatialcaps,
        util.nspath_eval('ogc:GeometryOperands', self.parent.context.namespaces))

        for geomtype in \
        fes1.MODEL['GeometryOperands']['values']:
            etree.SubElement(geomops,
            util.nspath_eval('ogc:GeometryOperand',
            self.parent.context.namespaces)).text = geomtype

        spatialops = etree.SubElement(spatialcaps,
        util.nspath_eval('ogc:SpatialOperators', self.parent.context.namespaces))

        for spatial_comparison in \
        fes1.MODEL['SpatialOperators']['values']:
            etree.SubElement(spatialops,
            util.nspath_eval('ogc:SpatialOperator', self.parent.context.namespaces),
            name=spatial_comparison)

        scalarcaps = etree.SubElement(fltcaps,
        util.nspath_eval('ogc:Scalar_Capabilities', self.parent.context.namespaces))

        etree.SubElement(scalarcaps, util.nspath_eval('ogc:LogicalOperators',
        self.parent.context.namespaces))

        cmpops = etree.SubElement(scalarcaps,
        util.nspath_eval('ogc:ComparisonOperators', self.parent.context.namespaces))

        for cmpop in sorted(fes1.MODEL['ComparisonOperators'].keys()):
            etree.SubElement(cmpops,
            util.nspath_eval('ogc:ComparisonOperator',
            self.parent.context.namespaces)).text = \
            fes1.MODEL['ComparisonOperators'][cmpop]['opname']

        arithops = etree.SubElement(scalarcaps,
        util.nspath_eval('ogc:ArithmeticOperators', self.parent.context.namespaces))

        functions = etree.SubElement(arithops,
        util.nspath_eval('ogc:Functions', self.parent.context.namespaces))

        functionames = etree.SubElement(functions,
        util.nspath_eval('ogc:FunctionNames', self.parent.context.namespaces))

        for fnop in sorted(fes1.MODEL['Functions'].keys()):
            etree.SubElement(functionames,
            util.nspath_eval('ogc:FunctionName', self.parent.context.namespaces),
            nArgs=fes1.MODEL['Functions'][fnop]['args']).text = fnop

        idcaps = etree.SubElement(fltcaps,
        util.nspath_eval('ogc:Id_Capabilities', self.parent.context.namespaces))

        for idcap in fes1.MODEL['Ids']['values']:
            etree.SubElement(idcaps, util.nspath_eval('ogc:%s' % idcap,
            self.parent.context.namespaces))

        return node

    def extractmetadata(self):

        print('Metadata Extraction. kjwhfjwefjehg')
        return 'a'
        

    def getrecordbyid(self, raw=False):

        # 05.12.18, source: https://docs.python.org/3/library/sqlite3.html
        # connection to database 
        # @author: Aysel Tandik, Anika Graupner
        import sqlite3
        conn = sqlite3.connect('../../db-data/data.db')
        print(conn)
        c = conn.cursor()
        c.execute('SELECT record1 FROM similarities WHERE record1 = 1')
        print(c.fetchone())

        ''' Handle GetRecordById request '''
        # wenn kein Parameter für die ID angegeben wird, es also kein id= gibt 
        if 'id' not in self.parent.kvp:
            return self.exceptionreport('MissingParameterValue', 'id',
            'Missing id parameter')

        # wenn es id= gibt, aber keinen Wert dahinter 
        if len(self.parent.kvp['id']) < 1:
            return self.exceptionreport('InvalidParameterValue', 'id',
            'Invalid id parameter')

        # wenn es kein outputschema= gibt, ist das schema csw 
        if 'outputschema' not in self.parent.kvp:
            self.parent.kvp['outputschema'] = self.parent.context.namespaces['csw']

        # vll wenn mehrere ids angebeben werden....
        if self.parent.requesttype == 'GET':
            self.parent.kvp['id'] = self.parent.kvp['id'].split(',')

        # wenn ein falsches outputformat angegeben ist 
        if ('outputformat' in self.parent.kvp and
            self.parent.kvp['outputformat'] not in
            self.parent.context.model['operations']['GetRecordById']['parameters']
            ['outputFormat']['values']):
            return self.exceptionreport('InvalidParameterValue',
            'outputformat', 'Invalid outputformat parameter %s' %
            self.parent.kvp['outputformat'])

        # wenn ein falsches outputschema angegeben ist 
        if ('outputschema' in self.parent.kvp and self.parent.kvp['outputschema'] not in
            self.parent.context.model['operations']['GetRecordById']['parameters']
            ['outputSchema']['values']):
            return self.exceptionreport('InvalidParameterValue',
            'outputschema', 'Invalid outputschema parameter %s' %
            self.parent.kvp['outputschema'])


        if 'elementsetname' not in self.parent.kvp:
            self.parent.kvp['elementsetname'] = 'summary'
        else:
            if (self.parent.kvp['elementsetname'] not in
                self.parent.context.model['operations']['GetRecordById']['parameters']
                ['ElementSetName']['values']):
                return self.exceptionreport('InvalidParameterValue',
                'elementsetname', 'Invalid elementsetname parameter %s' %
                self.parent.kvp['elementsetname'])

        # erster knoten, kann man übernehmen 
        node = etree.Element(util.nspath_eval('csw:GetRecordByIdResponse',
        self.parent.context.namespaces), nsmap=self.parent.context.namespaces)

        # zweiter knoten, kann man übernehmen 
        node.attrib[util.nspath_eval('xsi:schemaLocation',
        self.parent.context.namespaces)] = '%s %s/csw/2.0.2/CSW-discovery.xsd' % \
        (self.parent.context.namespaces['csw'], self.parent.config.get('server', 'ogc_schemas_base'))

        # query repository
        LOGGER.info('Querying repository with ids: %s', self.parent.kvp['id'][0])
        # hier werden die ids aus dem Repository abgefragt und in results gespeichert  
        results = self.parent.repository.query_ids(self.parent.kvp['id'])

        if raw:  # GetRepositoryItem request
            LOGGER.debug('GetRepositoryItem request')
            if len(results) > 0:
                return etree.fromstring(util.getqattr(results[0],
                self.parent.context.md_core_model['mappings']['pycsw:XML']), self.parent.context.parser)

        for result in results:
            if (util.getqattr(result,
            self.parent.context.md_core_model['mappings']['pycsw:Typename']) == 'csw:Record'
            and self.parent.kvp['outputschema'] ==
            'http://www.opengis.net/cat/csw/2.0.2'):
                # serialize record inline
                node.append(self._write_record(
                result, self.parent.repository.queryables['_all']))
            elif (self.parent.kvp['outputschema'] ==
                'http://www.opengis.net/cat/csw/2.0.2'):
                # serialize into csw:Record model
                typename = None

                for prof in self.parent.profiles['loaded']:  # find source typename
                    if self.parent.profiles['loaded'][prof].typename in \
                    [util.getqattr(result, self.parent.context.md_core_model['mappings']['pycsw:Typename'])]:
                        typename = self.parent.profiles['loaded'][prof].typename
                        break

                if typename is not None:
                    util.transform_mappings(
                        self.parent.repository.queryables['_all'],
                        self.parent.context.model['typenames'][typename][
                            'mappings']['csw:Record']
                    )

                node.append(self._write_record(
                result, self.parent.repository.queryables['_all']))
            elif self.parent.kvp['outputschema'] in self.parent.outputschemas.keys():  # use outputschema serializer
                node.append(self.parent.outputschemas[self.parent.kvp['outputschema']].write_record(result, self.parent.kvp['elementsetname'], self.parent.context, self.parent.config.get('server', 'url')))
            else:  # it's a profile output
                node.append(
                self.parent.profiles['loaded'][self.parent.kvp['outputschema']].write_record(
                result, self.parent.kvp['elementsetname'],
                self.parent.kvp['outputschema'], self.parent.repository.queryables['_all']))

        if raw and len(results) == 0:
            return None

        return node

    def exceptionreport(self, code, locator, text):
        ''' Generate ExceptionReport '''
        self.parent.exception = True
        self.parent.status = 'OK'

        try:
            language = self.parent.config.get('server', 'language')
            ogc_schemas_base = self.parent.config.get('server', 'ogc_schemas_base')
        except:
            language = 'en-US'
            ogc_schemas_base = self.parent.context.ogc_schemas_base

        node = etree.Element(util.nspath_eval('ows:ExceptionReport',
        self.parent.context.namespaces), nsmap=self.parent.context.namespaces,
        version='1.2.0', language=language)

        node.attrib[util.nspath_eval('xsi:schemaLocation',
        self.parent.context.namespaces)] = \
        '%s %s/ows/1.0.0/owsExceptionReport.xsd' % \
        (self.parent.context.namespaces['ows'], ogc_schemas_base)

        exception = etree.SubElement(node, util.nspath_eval('ows:Exception',
        self.parent.context.namespaces),
        exceptionCode=code, locator=locator)

        exception_text = etree.SubElement(exception,
        util.nspath_eval('ows:ExceptionText',
        self.parent.context.namespaces))

        try:
            exception_text.text = text
        except ValueError as err:
            exception_text.text = repr(text)

        return node

