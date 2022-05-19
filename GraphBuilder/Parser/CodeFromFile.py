import json
import os
from pathlib import Path
import re
from GraphBuilder.Parser.CodeWrapper import CodeWrapper
from GraphBuilder.Parser.MapCreator import MapCreator
from GraphBuilder.Parser.CodeParser import codeParser
from GraphBuilder.Parser.json_functions import read_json_file, save_json_to_file

non_working_files = ["module-info", "TestNotesText", "TestRichTextRun", "TestNameIdChunks", "PAPAbstractType",
                     "TAPAbstractType", "PPDrawing", "HSLFFill", "HemfGraphics", "DrawPaint", "ExtSSTRecord",
                     "SelectionRecord", "FeatRecord", "MergeCellsRecord", "ColorGradientFormatting",
                     "IconMultiStateFormatting"
                     "ChartTitleFormatRecord", "ChartFRTInfoRecord", "ExtRst", "PageItemRecord", "EmbeddedExtractor",
                     "Frequency", "ForkedEvaluator", "ChunkedCipherOutputStream", "StandardEncryptor",
                     "POIFSDocumentPath", "PackagePart", "PackageRelationshipCollection", "PackageRelationshipTypes"
                                                                                          "PackagingURIHelper",
                     "ContentTypes", "PackageNamespaces", "ZipPackage", "OPCPackage", "PackagePartCollection",
                     "UnmarshallContext", "POIXMLFactory", "POIXMLDocument", "POIXMLDocumentPart",
                     "POIXMLExtractorFactory", "XWPFRelation", "XWPFDocument", "XSSFRelation", "XSSFWorkbook"
                                                                                               "SignatureConfig",
                     "OOXMLSignatureFacet", "XAdESSignatureFacet", "RelationshipTransformService", "XDGFRelation",
                     "XSLFSlide", "XSLFRelation", "XSLFGraphicFrame", "XSLFPictureShape", "XSLFSimpleShape",
                     "MergePresentations", "BarChartDem", "TestPageSettingsBlock", "TestHSSFEventFactory"
                                                                                   "TestHSSFSheetUpdateArrayFormulas",
                     "TestHSSFSheet", "TestDateFormatConverter", "TestPropertySorter", "TestEscherContainerRecord",
                     "TestSignatureInfo", "XSLFSimpleShape", "IconMultiStateFormatting", "ChartTitleFormatRecord",
                     "PackageRelationshipTypes", "PackagingURIHelper", "POIXMLRelation", "XSSFWorkbook",
                     "SignatureConfig", "TestSlide", "TestPackage", "TestPackageThumbnail", "TestListParts",
                     "TestContentTypeManager", "TestOPCComplianceCoreProperties", "TestXWPFTableCell",
                     "TestXSSFImportFromXML", "TestXSSFDataValidationConstraint", "TestXSSFDrawing", "TestXSLFNotes",
                     "TestXSLFSlide", "TestXSLFPictureShape", "BarChartDemo", "TestHSSFEventFactory",
                     "TestHSSFSheetUpdateArrayFormulas", "TestXSLFChart", "XMLSlideShow"]

class CodeFromFile:
    def __init__(self, file_path, name, output_path):
        self.file_path = file_path
        self.directory = os.fsencode(self.file_path)
        self.name = name
        self.output_path = output_path
        self.full_code_text = ""
        self.code_parser = codeParser()

        self.concat_files()
        self.connect_between_classes()

    def concat_files(self):
        pathlist = Path(self.file_path).glob('**/*.java')
        for path in pathlist:
            path_in_str = str(path)
            if path_in_str.split('/')[-1].split('.')[0] in non_working_files:
                continue
            with open(path_in_str, "r", errors="ignore") as f:
                self.full_code_text += f.read()
                self.full_code_text = re.sub("package(.*?);", '', self.full_code_text)
                self.full_code_text = re.sub("import(.*?);", '', self.full_code_text)
                self.create_parse_and_map()

    def create_parse_and_map(self):
        current_query = CodeWrapper(self.name, self.name)
        mapped_code = self.code_parser.parse_post(self.full_code_text, current_query)
        map_code = MapCreator(mapped_code)
        task_dict = map_code.create_dictionary(current_query)

        interfaces = set()
        for e in task_dict['edges']:
            if e['type']=='implements': interfaces.add(e['to'])
        for v in task_dict['vertices']:
            if v['key'] in interfaces: v['type']='interface'

        with open(self.output_path, 'w') as fp:
            json.dump(task_dict, fp)


    def test_new_file(self):
        pathlist = Path(self.file_path).glob('**/*.java')
        for path in pathlist:
            # because path is object not string
            path_in_str = str(path)
            print(path_in_str)
            self.full_code_text = ""
            with open(path_in_str, "r") as f:
                print(path_in_str.split('/')[-1].split('.')[0])
                self.full_code_text += f.read()
                self.full_code_text = re.sub("package(.*?);", '', self.full_code_text)
                self.full_code_text = re.sub("import(.*?);", '', self.full_code_text)

            current_query = CodeWrapper(self.name, self.name)
            mapped_code = self.code_parser.parse_post(self.full_code_text, current_query)

    def connect_between_classes(self):
        data = read_json_file(self.output_path)
        map = {}
        vertices = data["vertices"]
        new_edges = []

        for v in vertices:
            name = v["name"]
            key = v["key"]
            type = v["type"]
            if type == "class":
                map[name] = key

        for v in vertices:
            key = v["key"]
            attributes_types = set()
            if "attributes" in v:
                attributes = v["attributes"]
                for attr in attributes:
                    obj = attr.split(' ')[0]
                    if obj in map.keys():
                        new_edge = {}
                        to = map[obj]
                        new_edge["type"] = "contains"
                        new_edge["from"] = key
                        new_edge["to"] = to
                        if not to in attributes_types:
                            attributes_types.add(to)
                            new_edges.append(new_edge)

        edges = data["edges"]
        edges = self.removeUnusedEdges(edges)
        edges = edges + new_edges
        new_json = {}
        new_json["vertices"] = vertices
        new_json["edges"] = edges
        save_json_to_file(new_json, self.output_path)
        return new_json

    def removeUnusedEdges(self,edges):
        interfaces=set()
        new_edges = []
        for e in edges:
            if(e["from"]==0): continue
            new_edges.append(e)
        return new_edges


def main():
    c = CodeFromFile('../src1', '', '../ron.json')

if __name__ == '__main__':
    main()