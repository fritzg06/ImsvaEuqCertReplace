# Declare Variables
varOutputEUQPKCS12 = "OutputEUQCert.p12"
varOutputKeystore = "OutputKeystore"
varPassphrase = "password"
# SED Variables
varOriginal1="keystoreFile=\"sslkey/.keystore\""
varNew1="keystoreFile=\"sslkey/" +varOutputKeystore +"\""
varOriginal2="keystorePass=\"trendimsva\""
varNew2="keystorePass=\"" +varPassphrase +"\""
# Steps
print "\n##########"
print "# STEP 1 #"
print "##########"
varCertFile=raw_input("Enter the certificate filename: ")
varKeyFile=raw_input("Enter the private key filename: ")
print "\nThe Certificate file is", varCertFile
print "\nThe Private Key file is", varKeyFile
import os
print "\n##########"
print "# STEP 2 #"
print "##########"
print "\nDoing command...: openssl pkcs12 -export -out", varOutputEUQPKCS12, " -inkey ", varKeyFile, " -in ", varCertFile
cmdstring1="openssl pkcs12 -export "  +"-inkey " +varKeyFile +" -in " +varCertFile +" -out " +varOutputEUQPKCS12
os.system(cmdstring1)
print "\nChecking the PKCS12 Certificate...: /opt/trend/imss/UI/javaJRE/bin/keytool -list -keystore", varOutputEUQPKCS12, "-storetype pkcs12"
cmdstring2="/opt/trend/imss/UI/javaJRE/bin/keytool -list -storetype pkcs12 -keystore " +varOutputEUQPKCS12
os.system(cmdstring2)
print "\n##########"
print "# STEP 3 #"
print "##########"
print "\nImporting certificate to keystore...: /opt/trend/imss/UI/javaJRE/bin/keytool -importkeystore -srckeystore ", varOutputEUQPKCS12, " -srcstoretype pkcs12 -srcalias 1 -destkeystore", varOutputKeystore, " -deststoretype jks -destalias tomcat"
cmdstring3="/opt/trend/imss/UI/javaJRE/bin/keytool -srcstoretype pkcs12 -srcalias 1 -deststoretype jks -destalias tomcat -importkeystore -srckeystore " +varOutputEUQPKCS12 +" -destkeystore " +varOutputKeystore
os.system(cmdstring3)
print "\nThe following files are created:"
cmdstring4="ls -l | grep -Ei \"" +varOutputEUQPKCS12 +"|" +varOutputKeystore +"\""
os.system(cmdstring4)
print "\n##########"
print "# STEP 4 #"
print "##########"
print "\nCopying the generated keystore to /opt/trend/imss/UI/tomcat/sslkey/ directory"
cmdstring5="cp " +varOutputKeystore +" /opt/trend/imss/UI/tomcat/sslkey/" +varOutputKeystore
os.system(cmdstring5)
print "\nDoing command...: ls /opt/trend/imss/UI/tomcat/sslkey/"
cmdstring6="ls -l /opt/trend/imss/UI/tomcat/sslkey/"
os.system(cmdstring6)
print "\n##########"
print "# STEP 5 #"
print "##########"
print "\nBacking up /opt/trend/imss/UI/euqUI/conf/server.xml"
cmdstring7="cp /opt/trend/imss/UI/euqUI/conf/server.xml server.xml.bak.original"
os.system(cmdstring7)
print "\nDisplaying the backup xml file..."
cmdstring8="ls -l server.xml.bak.original"
os.system(cmdstring8)
print "\nUpdating /opt/trend/imss/UI/euqUI/conf/server.xml"
import fileinput
for line in fileinput.input("/opt/trend/imss/UI/euqUI/conf/server.xml", inplace=True):
    # inside this loop the STDOUT will be redirected to the file
    # the comma after each print statement is needed to avoid double line breaks
    print line.replace(varOriginal1, varNew1).replace(varOriginal2, varNew2),
print "\nRestarting EUQ Service...: S99EUQ restart"
cmdstring9="S99EUQ restart"
os.system(cmdstring9)
print "\nCOMPLETED!!! Please refresh EUQ Console!"
