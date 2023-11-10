''' Exceptions module '''

class ReportNotFound(Exception):
    EXIT_CODE = 10

    def __init__(self, filepath):
        super().__init__( f'Report not found at {filepath}' )

class NoTestData(Exception):
    EXIT_CODE = 11

    def __init__(self):
        super().__init__( 'Report does not contain code coverage data' )

class ExitCode(Exception):
    EXIT_CODE = 100

    def __init__(self):
        super().__init__( 'SF APEX RUN TEST COMMAND FINSIHED' )