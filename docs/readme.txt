xsltproc --nonet --stringparam html.stylesheet style.css /usr/share/docbook-xsl/xhtml/chunk.xsl GaussSum.xml 

The first line of GaussSum.xml needs to be changed to either:
/usr/share/docbook-xml42/docbookx.dtd (laptop)	
or
/usr/share/xml/docbook/4.2/docbookx.dtd