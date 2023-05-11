import os
import json
from modules.utils.exceptions import ReportNotFound, NoTestData

def getCodeCoverageFromJSON(filepath):

    if not os.path.isfile( filepath ):
        print( f'##[error] Report not found at {filepath}' )
        raise ReportNotFound( filepath )

    with open( filepath, 'rb') as file:
        data = json.load( file )
        
    if( ( not 'result' in data ) or ( not 'coverage' in data[ 'result' ] ) or 
       ( not 'coverage' in data[ 'result' ]['coverage'] )):
        print( f'##[warning] Report does not contain code coverage data' )
        raise NoTestData()
    
    mapTestClasses = dict()
    testResultInfo = data[ 'result' ][ 'coverage' ]
    if 'coverage' in testResultInfo:
        coverageData = testResultInfo[ 'coverage' ]
        if isinstance( coverageData, list ):
            for codeCoverageItem in coverageData:
                getCoverageData( codeCoverageItem, mapTestClasses )
        else:
            getCoverageData( coverageData, mapTestClasses )

    """ if 'codeCoverageWarnings' in testResultInfo:
        codeCoverageWarning = testResultInfo[ 'codeCoverageWarnings' ]
        if isinstance( codeCoverageWarning, list ):
            for codeCoverageWarningItem in codeCoverageWarning:
                getCoverageWarning( codeCoverageWarningItem, mapTestClasses )
        else:
            getCoverageWarning( codeCoverageWarning, mapTestClasses ) """

    return mapTestClasses


def getCoverageWarning( codeCoverageWarning, mapTestClasses ):
    
    message          = codeCoverageWarning[ 'message' ]
    classWarningName = codeCoverageWarning[ 'name' ]

    if classWarningName in mapTestClasses:
        mapTestClasses[ classWarningName ][ 'WARNING' ] = message
    else:
        mapTestClasses[ classWarningName ] = dict()
        mapTestClasses[ classWarningName ][ 'WARNING' ] = message
        mapTestClasses[ classWarningName ][ 'Number of lines' ] = 'N/A'
        mapTestClasses[ classWarningName ][ 'Number of uncovered lines' ] = 'N/A'



def getCoverageData( codeCoverageItem, mapTestClasses ):
    className           = codeCoverageItem[ 'name' ]
    numLines            = codeCoverageItem[ 'totalLines' ] #
    numUncoveredLines   = int(numLines) - int(codeCoverageItem[ 'totalCovered' ]) #

    if not className in mapTestClasses:
        mapTestClasses[ className ] = dict()

    mapTestClasses[ className ][ 'Number of lines' ] = int( numLines )
    mapTestClasses[ className ][ 'Number of uncovered lines' ] = int( numUncoveredLines )

    if int( numUncoveredLines ) > 0:
        totalLines = codeCoverageItem[ 'lines' ]
        uncoveredLines = [line for line in totalLines if totalLines[line] == 0]
        mapTestClasses[ className ][ 'Lines not covered' ] = ', '.join( uncoveredLines )
     
        
def sortDictionaries(mapCoverage, mapPercent):
    # Sort the TestResult Dictionary for better view on report
    classList = [k for k, v in sorted(mapPercent.items(), key=lambda item: item[1])]
    mapData = dict()
    for className in classList:
        mapData[ className ] = mapCoverage[className]
        mapData[ className ]['Percent'] = mapPercent[className]
    return mapData