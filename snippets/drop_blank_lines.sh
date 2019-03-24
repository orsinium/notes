# remove blank lines from begining of each file with *.py extension
perl -i -p -e 's/^\n+// if $.==1; $.=0 if eof' *.py
