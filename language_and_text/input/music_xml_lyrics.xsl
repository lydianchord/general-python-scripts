<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <body>
        <p>
          <xsl:apply-templates select="score-partwise/part[@id='P1']/measure/note/lyric[@number='1']"/>
        </p>
      </body>
    </html>
  </xsl:template>
  <xsl:template match="lyric">
    <xsl:value-of select="text"/>
    <xsl:if test="syllabic!='begin' and syllabic!='middle'">
      <xsl:text> </xsl:text>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
