import argparse

def parseArgs():

    parser = argparse.ArgumentParser()

    parser.add_argument( '-p', '--pathToReport', required=True, help='Path to report' )
    args = parser.parse_args()

    return args