# 3gpp-downloader
A downloader for 3gpp specifications (http://www.3gpp.org/specifications/specification-numbering)

Currently very naive and not very robust :)

## Todo
* Validate user input:
  * Specification number: Try and make a request based on spec url, if not successful, inform user and allow for new input
  * Version nr choice: just validate that integer is in range
* Add option for navigating to spec. 
  * Do this by listing series, and then series number and allow user to pick from list
* Add flag for choosing download location
* Pick a better default download location
* Change date format from yyyy/mm/dd hh:ss to yyyy-mm-dd
