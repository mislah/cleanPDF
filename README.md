# cleanPDF
PDFs prepared for presentation purposes often contains multiple pages with same content repeated inorder to present as a slideshow with each transition has some minor changes. These PDFs are great for presentation purposes but hard for someone who have to scroll through it. This program removes all repeating pages and create a new pdf without any repeating pages, Thus increases the readability and compressing the PDF file. The program also preserves all bookmarks.

## How it works
The Program groups all pages with same label (secondary page number) and keeps the final pages of each of those groups, hence the program only works on those PDFs with repeating pages has same page labels(most of the presentation PDFs has same labels for repeating pages). It keeps a record of all bookmarks and trace the changes in page numbers to add them back while creating the new PDF. 
