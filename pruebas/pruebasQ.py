#! /usr/bin/env python

import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),'..','q/bin'))
from qtextasdata import QTextAsData,QInputParams

# Create an instance of q. Default input parameters can be provided here if needed
q = QTextAsData()

# execute a query, using specific input parameters
r = q.execute('select * from /etc/passwd',QInputParams(delimiter=':'))

# Get the result status (ok/error). In case of error, r.error will contain a QError instance with the error information
r.status
#'ok'

# Get the number of rows returned
len(r.data)
#37

# Show an example row. Each row is a tuple of typed field values
r.data[0]
#(u'root', u'x', 0, 0, u'root', u'/root', u'/bin/bash')

# Show warnings if any. Each warning will be of type QWarning
r.warnings
#[]

# Explore the result metadata
r.metadata
#QMetadata<table_count=1,output_column_name_list=[u'c1', u'c2', u'c3', u'c4', u'c5', u'c6', u'c7'],data_load_count=1

# Get the list of output columns
r.metadata.output_column_name_list
#[u'c1', u'c2', u'c3', u'c4', u'c5', u'c6', u'c7']

# Get information about the data loadings that have taken place for this query to happen
r.metadata.data_loads
#[DataLoad<'/etc/passwd' at 1416781622.56 (took 0.002 seconds)>]

# Get table structure information. You can see the column names of the table, and the column types, along with the original filename. Materialized filenames list can be accessed as well if needed
r.metadata.table_structures
#[QTableStructure<filenames_str=/etc/passwd,materialized_file_count=1,column_names=['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7'],column_types=['text', 'text', 'int', 'int', 'text', 'text', 'text']>]

#Note that one data loading has taken place. Now, if we still use the same `QTextAsData` instance and run queries on the same files, no additional data loading will take place:
r2 = q.execute('select c1 from /etc/passwd',QInputParams(delimiter=':'))

# Get the status again
r2.status
#'ok'

# See the data returned (first row only)
r2.data[0]
#(u'root',)

# See the data loading information. Note that no data loadings have been done for this query
r.metadata.data_loads
#[]

# Any query running using the instance `q` and somehow using the `/etc/passwd` file will run immediately without requiring to load the data again. This is extremely useful for large files obviously, for cases where there are lots of queries that need to run against the same file, and for consistency of results. The command line interface of q has been extended to support this as well, by allowing multiple queries on the same command line - E.g. `q "select ..." "select ..." "select ..." ...`

# In addition, the API supports preloading of files before executing queries. Use the `load_data` or the `load_data_from_string` methods:

# Load the file using specific input parameters
q.load_data('my_file',QInputParams(delimiter='\t',skip_header=True,input_encoding='utf-16'))

# Execute a query using this file:
r3 = q.execute('select c5 from my_file where c1 > 1000')

# Note that the result indicates that no data loads have been performed
r3.metadata.data_loads
#[]

# unload() can be used in order to erase the already-loaded files.
q.unload()

# Now execute another query with my_file
r4 = q.execute('select c5 from my_file where c1 > 2000')

# One data loading has been performed due to this query
r4.metadata.data_loads
#[DataLoad<'my_file' at 1416781831.16 (took 0.001 seconds)>]

# Using a different instance of QTextAsData would also cause a separate data load. However, please note that in that case, both copies would reside in memory independently.
q2 = QTextAsData()
# q2.execute('select ... from my_file')

# Except for execute(), there is another method called analyze(), which will provide a response containing the metadata related to analyzing the query and the file they use.
r5 = q.analyze('select * from my_file')

# r5 is a standard response like above, except that it won't contain data (it will be None), so r5.status, r5.error, r5.metadata and r5.warnings will be filled with relevant data.

### NEW - stdin behavior has been generalized into providing a function which gets a table name and returns a file object. See [BRANCH-generic-injected-streams.markdown)(This) for more information.

# The following is deprecated and will be modified soon after the API will be finalized:

# In order to provide access to stdin, the execute command provides two parameters: `stdin_filename` and `stdin_file`. These two allow injecting a stream of data to queries.
# Deprecated r6 = q.execute('select * from my_stdin_file',stdin_filename='my_stdin_file',stdin_file=sys.stdin)

# Deprecated r7 = q.execute('select * from my_stdin_file',stdin_filename='my_stdin_file',stdin_file=file('mmmm','rb'))