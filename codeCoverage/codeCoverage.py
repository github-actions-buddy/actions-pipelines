import os
import sys
import __main__
from jinja2 import Environment, FileSystemLoader
from modules.utils.utilities import getCodeCoverageFromJSON, sortDictionaries
from modules.utils.argparser import parseArgs
from modules.utils.exceptions import ReportNotFound, NoTestData

PWD = os.path.dirname(os.path.realpath(__main__.__file__))

def main():
    args = parseArgs()

    try:
        mapCoverage = getCodeCoverageFromJSON(args.pathToReport)

        mapPercent = dict()
        for className in mapCoverage:
            numLines            = mapCoverage[className]['Number of lines']
            numUncoveredLines   = mapCoverage[className]['Number of uncovered lines']
            getPercent(className, numLines, numUncoveredLines, mapPercent)
        
        mapData = sortDictionaries(mapCoverage, mapPercent)
        generateReport(mapData)
    except ReportNotFound as reportNotFoundException:
        sys.exit( reportNotFoundException.EXIT_CODE )
    except NoTestData as noTestDataException:
        sys.exit( noTestDataException.EXIT_CODE )

def getPercent(className, numLocations, numLocationsNotCovered, mapPercents):
    if numLocations == 'N/A':
        percent = 0
    elif numLocations == 0:
        percent = 100
    else:
        percent = 100 - ((numLocationsNotCovered * 100)//(numLocations))
    mapPercents[className] = percent


def generateReport(mapData):
    file_loader = FileSystemLoader(f'{PWD}/templates')
    env         = Environment(loader=file_loader)

    template    = env.get_template('codeCoverageTemplate.html')
    output      = template.render(mapData=mapData)

    with open('report-code-coverage.html', 'w', encoding='utf-8') as reportFile:
        reportFile.write(output)


if __name__=='__main__':
    main()
